"""
4H RL staking optimization.

Evaluates whether stable-baselines3 PPO agent learns Kelly-aware staking policy
that improves bankroll growth Sharpe vs flat-stake baseline.

Substrate-pragmatic minimum-viable: synthetic per-race Kelly-aware environment;
PPO policy trained for limited timesteps; report final-state bankroll multiplier
vs flat-stake reference. Tier 2 EXECUTION trains at production scope.
"""

import argparse
import json

import boto3
import numpy as np
import pandas as pd
import psycopg2

try:
    import gymnasium as gym
    from gymnasium import spaces
    from stable_baselines3 import PPO
    SB3_AVAILABLE = True
except ImportError:
    SB3_AVAILABLE = False


DB_SECRET_ARN = 'arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials'


def get_db_conn():
    sm_client = boto3.client('secretsmanager', region_name='us-east-1')
    secret = json.loads(sm_client.get_secret_value(SecretId=DB_SECRET_ARN)['SecretString'])
    return psycopg2.connect(
        host=secret['host'], port=secret['port'],
        dbname=secret['dbname'], user=secret['username'], password=secret['password'],
    )


def load_betting_substrate(window_start, window_end):
    """Pull Hybrid C top-1 pick + actuals + payout for staking env."""
    conn = get_db_conn()
    df = pd.read_sql("""
        WITH top1 AS (
            SELECT hp.race_id, hp.horse_id, hp.hybrid_c_win_probability,
                   ROW_NUMBER() OVER (PARTITION BY hp.race_id ORDER BY hp.hybrid_c_win_probability DESC) AS rk
            FROM hybrid_c_predictions hp
            JOIN races r ON r.race_id = hp.race_id
            WHERE hp.ensemble_version = 'option_c_hybrid_ensemble_20260515'
              AND r.race_date BETWEEN %s AND %s
        )
        SELECT t1.race_id::text AS race_id,
               t1.hybrid_c_win_probability AS p,
               (res.finish_position = 1)::int AS is_winner,
               COALESCE(res.win_payout, 0.0) AS win_payout
        FROM top1 t1
        JOIN entries e ON e.race_id = t1.race_id AND e.horse_id::text = t1.horse_id
        LEFT JOIN results res ON res.race_id = t1.race_id AND res.horse_id = e.horse_id
        WHERE t1.rk = 1
        ORDER BY t1.race_id
    """, conn, params=[window_start, window_end])
    conn.close()
    return df


class StakingEnv(gym.Env):
    """One step per race: observe (p), action = stake fraction [0, 0.25]; reward = bankroll Δ."""

    def __init__(self, df):
        super().__init__()
        self.df = df.reset_index(drop=True)
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32)
        self.action_space = spaces.Box(low=0.0, high=0.25, shape=(1,), dtype=np.float32)
        self.bankroll = 100.0
        self.idx = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.bankroll = 100.0
        self.idx = 0
        return np.array([self.df.iloc[0]['p']], dtype=np.float32), {}

    def step(self, action):
        stake_frac = float(np.clip(action[0], 0.0, 0.25))
        stake = self.bankroll * stake_frac
        row = self.df.iloc[self.idx]
        if row['is_winner'] == 1:
            payout_multiplier = (row['win_payout'] / 2.0) if row['win_payout'] > 0 else 1.0
            gain = stake * payout_multiplier - stake
        else:
            gain = -stake
        self.bankroll += gain
        reward = gain / 100.0  # Normalize
        self.idx += 1
        done = self.idx >= len(self.df)
        obs = np.array([self.df.iloc[self.idx]['p']], dtype=np.float32) if not done else np.array([0.0], dtype=np.float32)
        return obs, reward, done, False, {}


def evaluate(window_start, window_end, output_path, timesteps=1000):
    if not SB3_AVAILABLE:
        result = {'verdict': 'substrate-investigation-required', 'error': 'stable_baselines3 / gymnasium not importable'}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    df = load_betting_substrate(window_start, window_end)
    df = df.dropna(subset=['is_winner']).reset_index(drop=True)
    print(f"Staking substrate: {len(df)} races")
    if len(df) < 50:
        result = {'verdict': 'substrate-thin', 'n_races': len(df)}
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        return result

    # Train PPO
    env = StakingEnv(df)
    model = PPO('MlpPolicy', env, verbose=0, learning_rate=1e-3, n_steps=128, batch_size=32)
    model.learn(total_timesteps=timesteps, progress_bar=False)

    # Final bankroll under RL policy
    obs, _ = env.reset()
    done = False
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, _, done, _, _ = env.step(action)
    rl_bankroll = env.bankroll

    # Flat-stake baseline: 5% per race
    bankroll_flat = 100.0
    for _, row in df.iterrows():
        stake = bankroll_flat * 0.05
        if row['is_winner'] == 1 and row['win_payout'] > 0:
            bankroll_flat += stake * ((row['win_payout'] / 2.0) - 1)
        else:
            bankroll_flat -= stake

    delta_pct = (rl_bankroll - bankroll_flat) / 100.0 * 100  # pp vs starting bankroll

    if delta_pct > 5:
        verdict = 'substrate-validated production candidate (RL > flat-stake)'
    elif abs(delta_pct) < 2:
        verdict = 'null (no RL improvement)'
    else:
        verdict = 'substrate-investigation-required'

    result = {
        'verdict': verdict,
        'rl_final_bankroll': float(rl_bankroll),
        'flat_stake_final_bankroll': float(bankroll_flat),
        'delta_pp_vs_initial': float(delta_pct),
        'n_races': len(df),
        'timesteps': timesteps,
    }
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Verdict: {verdict}; RL={rl_bankroll:.2f} flat={bankroll_flat:.2f}")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--window-start', default='2026-05-02')
    parser.add_argument('--window-end', default='2026-05-17')
    parser.add_argument('--timesteps', type=int, default=1000)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    evaluate(args.window_start, args.window_end, args.output, args.timesteps)


if __name__ == '__main__':
    main()
