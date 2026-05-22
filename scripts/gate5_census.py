"""Gate 5 — full data census. Every input data element × every month × 4.5 years.

For each INPUT table (data we ingest/derive — NOT prediction tables):
  - per-month coverage % for every column
  - constant/degenerate detection (always-same-value flag)
  - numeric distribution sanity (min/max/mean per year)
  - orphan-row checks (races without entries, entries without PPs, etc.)

Outputs:
  - /home/strakajagr/EE_GATE5_CENSUS_MASTER_<ts>.csv  — every (element, verdict)
  - /home/strakajagr/EE_GATE5_CENSUS_TIMELINE_<ts>.csv — element × month matrix
  - /home/strakajagr/EE_GATE5_CENSUS_<ts>.md  — human-readable summary
"""
import json
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import boto3
import pandas as pd

# Input tables to audit. Skip predictions, archives, migrations, output tables.
INPUT_TABLES = {
    'past_performances': {
        'date_col': 'race_date',
        'pk': 'pp_id',
        # Feature-relevant columns (the SELECT in _load_raw_pps + a few more)
        'cols': [
            'horse_id', 'race_id', 'race_date', 'track_code', 'race_number',
            'finish_position', 'field_size', 'computed_speed_figure',
            'speed_rating_raw', 'track_variant',
            'early_pace_figure', 'late_pace_figure', 'pace_delta',
            'call_1_position', 'call_2_position', 'call_3_position',
            'call_1_lengths', 'call_2_lengths', 'call_3_lengths', 'lengths_behind',
            'fraction_1', 'fraction_2', 'final_time',
            'running_style', 'trip_troubled', 'trip_pace_setter', 'trip_faded',
            'trip_late_rally', 'trip_no_factor', 'trip_gate_issue', 'wide_path',
            'purse', 'race_type', 'track_condition', 'surface', 'distance_furlongs',
            'claiming_price_entered', 'closing_odds', 'trainer_name',
            'days_since_last_race', 'race_start_number',
        ],
    },
    'entries': {
        'date_col_via_race': True,  # entries has no date; join races
        'pk': 'entry_id',
        'cols': [
            'horse_id', 'trainer_id', 'jockey_id', 'post_position', 'program_number',
            'morning_line_odds', 'weight_carried', 'allowance_weight',
            'apprentice_allowance',
            'lasix', 'lasix_first_time', 'bute',
            'blinkers_on', 'blinkers_off', 'blinkers_first_time',
            'tongue_tie', 'bar_shoes', 'front_bandages', 'mud_caulks',
            'equipment_change_from_last', 'medication_change_from_last',
            'is_scratched', 'is_entry',
        ],
    },
    'races': {
        'date_col': 'race_date',
        'pk': 'race_id',
        'cols': [
            'track_id', 'race_date', 'race_number', 'post_time', 'distance_furlongs',
            'surface', 'race_type', 'grade', 'race_name', 'purse', 'claiming_price',
            'conditions', 'field_size', 'rail_position', 'track_condition',
            'moisture_level', 'track_variant', 'going_stick_reading',
            'temperature', 'weather_conditions', 'wind_speed', 'wind_direction',
            'off_turf', 'equibase_race_id',
        ],
    },
    'results': {
        'date_col_via_race': True,
        'pk': 'result_id',
        'cols': [
            'horse_id', 'finish_position', 'official_finish', 'is_disqualified',
            'lengths_behind', 'final_time', 'beyer_speed_figure',
            'call_1_position', 'call_1_lengths', 'call_2_position', 'call_2_lengths',
            'stretch_position', 'stretch_lengths',
            'win_payout', 'place_payout', 'show_payout',
            'exacta_payout', 'trifecta_payout', 'superfecta_payout',
            'pick3_payout', 'pick3_payout_base_unit', 'pick3_pool_size',
            'pick4_payout', 'pick5_payout', 'pick6_payout',
            'daily_double_payout', 'quinella_payout',
        ],
    },
    'workouts': {
        'date_col': 'workout_date',
        'pk': 'workout_id',
        'cols': [
            'horse_id', 'track_code', 'distance_furlongs', 'workout_time',
            'workout_type', 'is_bullet', 'rank_on_day', 'total_works_on_day',
            'track_condition', 'exercise_rider',
        ],
    },
}

REFERENCE_TABLES = ['trainer_stats_history', 'angle_stats_history', 'jockeys',
                    'trainers', 'horses', 'tracks', 'angle_stats']

# Boolean-typed cols where we need to detect always-FALSE (COUNT(col) reads 100%
# because the value is FALSE-not-null, but the column carries no information).
BOOLEAN_COLS = {
    'entries': [
        'lasix', 'lasix_first_time', 'bute',
        'blinkers_on', 'blinkers_off', 'blinkers_first_time',
        'tongue_tie', 'bar_shoes', 'front_bandages', 'mud_caulks',
        'equipment_change_from_last', 'medication_change_from_last',
        'is_scratched', 'is_entry',
    ],
    'past_performances': [
        'trip_troubled', 'trip_pace_setter', 'trip_faded',
        'trip_late_rally', 'trip_no_factor', 'trip_gate_issue',
    ],
    'results': ['is_disqualified'],
    'races': ['off_turf'],
    'workouts': ['is_bullet'],
}


def lambda_query(sql):
    cli = boto3.client('lambda', region_name='us-east-1')
    resp = cli.invoke(FunctionName='equine-ingestion',
                      Payload=json.dumps({'action': 'raw_query', 'sql': sql}).encode(),
                      InvocationType='RequestResponse')
    body = json.loads(resp['Payload'].read())
    if isinstance(body, dict) and body.get('statusCode') != 200:
        raise RuntimeError(f"Lambda error: {body}")
    return json.loads(body['body'])['rows']


def census_table_monthly(table, cols, date_col, via_race=False):
    """Query monthly coverage % for each column in a table over 2022-01 → present."""
    # Build COUNT(col) for each column
    count_clauses = [f'COUNT({c}) AS {c}_n' for c in cols]
    select_clauses = ', '.join(count_clauses)
    if via_race:
        sql = f"""
            SELECT TO_CHAR(r.race_date, 'YYYY-MM') AS month,
                   COUNT(*) AS n_total,
                   {select_clauses}
            FROM {table} t
            JOIN races r ON r.race_id = t.race_id
            WHERE r.race_date BETWEEN '2022-01-01' AND '2026-05-31'
            GROUP BY month ORDER BY month
        """
    else:
        sql = f"""
            SELECT TO_CHAR({date_col}, 'YYYY-MM') AS month,
                   COUNT(*) AS n_total,
                   {select_clauses}
            FROM {table}
            WHERE {date_col} BETWEEN '2022-01-01' AND '2026-05-31'
            GROUP BY month ORDER BY month
        """
    return lambda_query(sql)


def detect_bool_variation(table, cols, cfg):
    """For boolean cols: count TRUE per year. Find always-FALSE columns."""
    parts = []
    for c in cols:
        parts.append(f"COUNT(*) FILTER (WHERE {c} = TRUE) AS {c}_true")
    select_clauses = ', '.join(parts)
    if cfg.get('date_col_via_race'):
        sql = f"""
            SELECT EXTRACT(YEAR FROM r.race_date)::int AS yr,
                   COUNT(*) AS n_total, {select_clauses}
            FROM {table} t JOIN races r ON r.race_id = t.race_id
            WHERE r.race_date BETWEEN '2022-01-01' AND '2026-05-31'
            GROUP BY yr ORDER BY yr
        """
    else:
        date_col = cfg['date_col']
        sql = f"""
            SELECT EXTRACT(YEAR FROM {date_col})::int AS yr,
                   COUNT(*) AS n_total, {select_clauses}
            FROM {table}
            WHERE {date_col} BETWEEN '2022-01-01' AND '2026-05-31'
            GROUP BY yr ORDER BY yr
        """
    return lambda_query(sql)


def numeric_distribution(table, cols, via_race=False):
    """Per-year min/max/avg for numeric columns."""
    parts = []
    for c in cols:
        parts.append(f"MIN({c}) AS {c}_min")
        parts.append(f"MAX({c}) AS {c}_max")
        parts.append(f"AVG({c}) AS {c}_avg")
    select_clauses = ', '.join(parts)
    if via_race:
        sql = f"""
            SELECT EXTRACT(YEAR FROM r.race_date)::int AS yr, {select_clauses}
            FROM {table} t JOIN races r ON r.race_id = t.race_id
            WHERE r.race_date BETWEEN '2022-01-01' AND '2026-05-31'
            GROUP BY yr ORDER BY yr
        """
    else:
        return None  # caller handles
    return lambda_query(sql)


def orphan_checks():
    """Check expected child-row counts: races without entries, entries without PPs, etc."""
    queries = {
        'races_no_entries': """
            SELECT COUNT(*) AS n FROM races r
            WHERE r.race_date BETWEEN '2022-01-01' AND '2026-05-31'
              AND NOT EXISTS (SELECT 1 FROM entries e WHERE e.race_id = r.race_id)
        """,
        'races_no_results': """
            SELECT COUNT(*) AS n FROM races r
            WHERE r.race_date BETWEEN '2022-01-01' AND '2026-05-31'
              AND NOT EXISTS (SELECT 1 FROM results res WHERE res.race_id = r.race_id)
        """,
        'entries_no_pp_history': """
            SELECT COUNT(*) AS n FROM entries e
            JOIN races r ON r.race_id = e.race_id
            WHERE r.race_date BETWEEN '2022-01-01' AND '2026-05-31'
              AND NOT EXISTS (
                SELECT 1 FROM past_performances pp
                WHERE pp.horse_id = e.horse_id AND pp.race_date < r.race_date
              )
        """,
        'races_no_pp_rows': """
            SELECT COUNT(DISTINCT r.race_id) AS n FROM races r
            WHERE r.race_date BETWEEN '2022-01-01' AND '2026-05-31'
              AND NOT EXISTS (
                SELECT 1 FROM past_performances pp
                WHERE pp.race_date = r.race_date
                  AND pp.race_number = r.race_number
              )
        """,
        'total_races': """
            SELECT COUNT(*) AS n FROM races r
            WHERE r.race_date BETWEEN '2022-01-01' AND '2026-05-31'
        """,
    }
    results = {}
    for name, sql in queries.items():
        try:
            r = lambda_query(sql)
            results[name] = int(r[0]['n']) if r else 0
        except Exception as e:
            results[name] = f'ERROR: {e}'
    return results


def main():
    print("Gate 5 census — every input element × every month × 4.5 years")
    print("=" * 70)

    timeline = []   # rows: (table, column, month, coverage_pct, n_nn, n_total)
    master = []     # rows: (table, column, overall_pct, worst_month_pct, worst_month, constant_flag, verdict)

    for table, cfg in INPUT_TABLES.items():
        print(f"\n[{table}] querying monthly coverage for {len(cfg['cols'])} columns...")
        try:
            rows = census_table_monthly(
                table, cfg['cols'], cfg.get('date_col'),
                via_race=cfg.get('date_col_via_race', False),
            )
        except Exception as e:
            print(f"  ERROR: {e}")
            continue
        if not rows:
            print(f"  (no rows in window)")
            continue
        print(f"  {len(rows)} months returned")

        # Compute overall + worst-month per column
        for col in cfg['cols']:
            cov_per_month = {}
            n_nn_total = 0
            n_total = 0
            for r in rows:
                month = r['month']
                m_total = r['n_total']
                m_nn = r.get(f'{col}_n', 0) or 0
                pct = (100.0 * m_nn / m_total) if m_total else None
                cov_per_month[month] = pct
                n_nn_total += m_nn
                n_total += m_total
                timeline.append({
                    'table': table, 'column': col, 'month': month,
                    'coverage_pct': round(pct, 2) if pct is not None else None,
                    'n_nn': m_nn, 'n_total': m_total,
                })

            overall = 100.0 * n_nn_total / n_total if n_total else 0
            worst_pct = min((v for v in cov_per_month.values() if v is not None), default=None)
            worst_month = None
            for m, v in cov_per_month.items():
                if v == worst_pct:
                    worst_month = m
                    break

            # Verdict heuristic
            if overall < 1.0:
                verdict = 'CONSTANT-DEAD'
            elif overall < 50:
                verdict = 'SPARSE'
            elif overall < 90:
                verdict = 'PARTIAL'
            elif worst_pct is not None and worst_pct < 80 and overall >= 90:
                verdict = 'CLIFF'   # mostly good but a major outage
            elif overall >= 99:
                verdict = 'SOLID'
            else:
                verdict = 'OK'

            master.append({
                'table': table, 'column': col,
                'overall_pct': round(overall, 2),
                'worst_month_pct': round(worst_pct, 2) if worst_pct is not None else None,
                'worst_month': worst_month,
                'n_total_4yr': n_total,
                'verdict': verdict,
            })

    # Boolean variation pass — find always-FALSE columns
    print("\n[boolean variation]")
    bool_variation = {}
    for table, bcols in BOOLEAN_COLS.items():
        cfg = INPUT_TABLES.get(table)
        if not cfg:
            continue
        try:
            rows = detect_bool_variation(table, bcols, cfg)
        except Exception as e:
            print(f"  {table}: ERROR {e}")
            continue
        for col in bcols:
            yr_counts = {r['yr']: r.get(f'{col}_true', 0) for r in rows}
            total_true = sum(yr_counts.values())
            total_rows = sum(r['n_total'] for r in rows)
            true_pct = 100.0 * total_true / total_rows if total_rows else 0
            bool_variation[(table, col)] = {
                'total_true': total_true,
                'true_pct': true_pct,
                'yr_true_counts': yr_counts,
                'verdict': 'CONSTANT-DEAD' if total_true == 0 else
                           'VERY-SPARSE' if true_pct < 0.5 else 'NORMAL',
            }
            print(f"  {table}.{col}: {total_true:>6,} TRUE / {total_rows:,} "
                  f"({true_pct:.2f}%) — {bool_variation[(table, col)]['verdict']}")

    # Patch master table: override coverage verdict where boolean is constant
    for m in master:
        key = (m['table'], m['column'])
        if key in bool_variation and bool_variation[key]['verdict'] == 'CONSTANT-DEAD':
            m['verdict'] = 'CONSTANT-DEAD (always FALSE)'
            m['true_pct'] = 0.0
        elif key in bool_variation:
            m['true_pct'] = round(bool_variation[key]['true_pct'], 3)

    print("\n[orphan_checks]")
    orph = orphan_checks()
    for k, v in orph.items():
        print(f"  {k}: {v}")

    # Write outputs
    ts = datetime.utcnow().strftime('%Y%m%d_%H%M')
    master_path = f'/home/strakajagr/EE_GATE5_CENSUS_MASTER_{ts}.csv'
    timeline_path = f'/home/strakajagr/EE_GATE5_CENSUS_TIMELINE_{ts}.csv'

    # Normalize master rows (some may have extra 'true_pct' key from bool patch)
    all_keys = set()
    for m in master:
        all_keys.update(m.keys())
    fieldnames = ['table', 'column', 'overall_pct', 'worst_month_pct',
                  'worst_month', 'n_total_4yr', 'verdict']
    if 'true_pct' in all_keys:
        fieldnames.append('true_pct')
    with open(master_path, 'w') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        w.writeheader()
        for m in master:
            row = {k: m.get(k, '') for k in fieldnames}
            w.writerow(row)
    with open(timeline_path, 'w') as f:
        w = csv.DictWriter(f, fieldnames=list(timeline[0].keys()))
        w.writeheader()
        w.writerows(timeline)

    # Master summary
    print("\n" + "=" * 90)
    print(f"§1 CENSUS MASTER TABLE ({len(master)} elements)")
    print("=" * 90)
    print(f"{'table':<22}{'column':<32}{'overall':>9}{'worst-mo':>10}{'when':>9}  {'verdict':<14}")
    print("-" * 100)
    for m in sorted(master, key=lambda x: (x['table'], x['overall_pct'])):
        wm = m['worst_month_pct']
        wmo = m['worst_month']
        print(f"{m['table']:<22}{m['column']:<32}{m['overall_pct']:>8.2f}%"
              f"{(f'{wm:.1f}%' if wm is not None else '—'):>10}"
              f"{(wmo or '—'):>9}  {m['verdict']:<14}")

    # Broken list
    broken = [m for m in master if m['verdict'] not in ('SOLID', 'OK')]
    print(f"\n{len(broken)} elements NOT verdict-SOLID/OK")

    print(f"\nFiles saved:")
    print(f"  {master_path}")
    print(f"  {timeline_path}")

    return master, timeline, orph


if __name__ == '__main__':
    main()
