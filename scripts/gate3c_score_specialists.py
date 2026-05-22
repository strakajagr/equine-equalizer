"""Score the 35 specialist predictions for top-K containment on the OOS window."""
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import boto3
import numpy as np
import pandas as pd

# Predictions CSV from Fargate
PREDS = '/tmp/gate3c_specialist_predictions.csv'
START = '2026-05-02'
END = '2026-05-17'


def lambda_query(sql):
    cli = boto3.client('lambda', region_name='us-east-1')
    resp = cli.invoke(FunctionName='equine-ingestion',
                      Payload=json.dumps({'action': 'raw_query', 'sql': sql}).encode(),
                      InvocationType='RequestResponse')
    body = json.loads(resp['Payload'].read())
    if isinstance(body, dict) and body.get('statusCode') != 200:
        raise RuntimeError(f"Lambda error: {body}")
    return json.loads(body['body'])['rows']


def field_bucket(n):
    if n <= 6: return '≤6'
    if n <= 8: return '7-8'
    if n <= 10: return '9-10'
    return '11+'


def main():
    df = pd.read_csv(PREDS)
    df['race_date'] = pd.to_datetime(df['race_date'])

    # Winners
    wins = pd.DataFrame(lambda_query(f"""
        SELECT t.track_code, r.race_date, r.race_number,
               res.horse_id::text AS winner_horse_id
        FROM results res
        JOIN races r USING(race_id)
        JOIN tracks t ON t.track_id = r.track_id
        WHERE res.finish_position = 1
          AND r.race_date BETWEEN '{START}' AND '{END}'
    """))
    wins['race_date'] = pd.to_datetime(wins['race_date'])
    wins['race_number'] = wins['race_number'].astype(int)
    wins = wins.drop_duplicates(['track_code', 'race_date', 'race_number'])
    win_map = {}
    for _, w in wins.iterrows():
        win_map[(w['track_code'], pd.Timestamp(w['race_date']), int(w['race_number']))] = \
            str(w['winner_horse_id'])

    model_cols = [c for c in df.columns if c.startswith('m__')]
    results = {}
    print(f"Scoring {len(model_cols)} specialist models on {len(df):,} OOS rows")

    for col in model_cols:
        name = col[3:]  # strip m__
        sub = df.dropna(subset=[col]).copy()
        if len(sub) == 0:
            continue
        n_races = 0
        overall = defaultdict(int)
        by_field = defaultdict(lambda: defaultdict(int))
        for (tc, rd, rn), grp in sub.groupby(['track_code', 'race_date', 'race_number']):
            key = (tc, pd.Timestamp(rd), int(rn))
            winner = win_map.get(key)
            if winner is None:
                continue
            fs = len(grp)
            bucket = field_bucket(fs)
            ranked = list(grp.sort_values(col, ascending=False)['horse_id'].astype(str))
            n_races += 1
            by_field[bucket]['n_races'] += 1
            for k in (1, 2, 3, 4, 5):
                hit = int(winner in ranked[:k])
                overall[f'top{k}'] += hit
                by_field[bucket][f'top{k}'] += hit
        if n_races == 0:
            continue
        r = {'n_races': n_races}
        for k in (1, 2, 3, 4, 5):
            r[f'top{k}_pct'] = 100.0 * overall[f'top{k}'] / n_races
        r['by_field'] = {}
        for b in ['≤6', '7-8', '9-10', '11+']:
            if b in by_field:
                nb = by_field[b]['n_races']
                r['by_field'][b] = {'n_races': nb}
                for k in (1, 2, 3, 4, 5):
                    r['by_field'][b][f'top{k}_pct'] = 100.0 * by_field[b][f'top{k}'] / nb
        results[name] = r

    # Print sorted by top-4
    print("\n" + "=" * 110)
    print("§2 — SPECIALIST MODELS, TOP-K CONTAINMENT (sorted by top-4)")
    print("=" * 110)
    print(f"{'model':<32}{'n':>5}{'top1':>9}{'top2':>9}{'top3':>9}{'top4':>9}{'top5':>9}")
    print("-" * 80)
    for name, r in sorted(results.items(), key=lambda kv: -kv[1]['top4_pct']):
        print(f"{name:<32}{r['n_races']:>5}"
              f"{r['top1_pct']:>8.1f}%{r['top2_pct']:>8.1f}%{r['top3_pct']:>8.1f}%"
              f"{r['top4_pct']:>8.1f}%{r['top5_pct']:>8.1f}%")

    print("\nBy field size, top-4 only (top 10 models by overall top-4):")
    print(f"{'model':<32}{'≤6':>14}{'7-8':>14}{'9-10':>14}{'11+':>14}")
    sorted_by_top4 = sorted(results.items(), key=lambda kv: -kv[1]['top4_pct'])[:10]
    for name, r in sorted_by_top4:
        cells = []
        for b in ['≤6', '7-8', '9-10', '11+']:
            if b in r['by_field']:
                v = r['by_field'][b]
                cells.append(f"{v['top4_pct']:>6.1f}% n={v['n_races']:>3}")
            else:
                cells.append('—')
        print(f"{name:<32}" + ''.join(f'{c:>14}' for c in cells))

    ts = datetime.utcnow().strftime('%Y%m%d_%H%M')
    out = {'eval_window': [START, END], 'specialists': results}
    Path(f'/home/strakajagr/EE_GATE3C_SPECIALISTS_{ts}.json').write_text(
        json.dumps(out, indent=2, default=str))
    print(f"\nSaved: /home/strakajagr/EE_GATE3C_SPECIALISTS_{ts}.json")


if __name__ == '__main__':
    main()
