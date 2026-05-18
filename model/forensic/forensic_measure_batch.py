"""
Batch invocation orchestration: forensic_measure.py across multiple artifact candidates.

Substrate-pragmatic: parallel invocation across artifacts; aggregates per-artifact metrics into single batch JSON.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_forensic_measure(artifact, baseline, window_start, window_end, stratify_bel, output):
    """Substrate-pragmatic single-artifact invocation."""
    cmd = [
        sys.executable,
        str(Path(__file__).parent / 'forensic_measure.py'),
        '--artifact', artifact,
        '--window-start', window_start,
        '--window-end', window_end,
        '--output', output,
    ]
    if baseline:
        cmd.extend(['--baseline', baseline])
    if stratify_bel:
        cmd.append('--stratify-bel')

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {'status': 'FAILED', 'stderr': result.stderr, 'stdout': result.stdout}

    with open(output) as f:
        return {'status': 'OK', 'metrics': json.load(f)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifacts-dir', help='Directory containing artifact JSONs to measure')
    parser.add_argument('--artifacts-list', help='Newline-delimited list file of artifact paths')
    parser.add_argument('--baseline', help='Common baseline artifact for dual-criterion delta')
    parser.add_argument('--window-start', default='2026-05-02')
    parser.add_argument('--window-end', default='2026-05-10')
    parser.add_argument('--stratify-bel', action='store_true')
    parser.add_argument('--output', required=True, help='Aggregate batch JSON output')
    args = parser.parse_args()

    # Resolve artifacts
    if args.artifacts_dir:
        artifacts = sorted(Path(args.artifacts_dir).glob('*.json'))
    elif args.artifacts_list:
        with open(args.artifacts_list) as f:
            artifacts = [line.strip() for line in f if line.strip()]
    else:
        raise ValueError("Either --artifacts-dir OR --artifacts-list required")

    print(f"Batch forensic measurement: {len(artifacts)} artifacts")

    batch_metrics = {}
    for i, artifact in enumerate(artifacts, 1):
        artifact_name = Path(artifact).stem
        output_path = f"/tmp/batch_forensic_{artifact_name}.json"
        print(f"  [{i}/{len(artifacts)}] {artifact_name}")
        batch_metrics[artifact_name] = run_forensic_measure(
            str(artifact), args.baseline, args.window_start, args.window_end,
            args.stratify_bel, output_path
        )

    with open(args.output, 'w') as f:
        json.dump(batch_metrics, f, indent=2)

    print(f"Batch forensic measurement complete: {args.output}")

    # Surface summary
    n_ok = sum(1 for m in batch_metrics.values() if m['status'] == 'OK')
    n_failed = len(batch_metrics) - n_ok
    print(f"  OK: {n_ok}/{len(batch_metrics)}")
    print(f"  FAILED: {n_failed}")


if __name__ == '__main__':
    main()
