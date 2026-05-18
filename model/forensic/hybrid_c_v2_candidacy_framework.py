"""
Hybrid C v2 candidacy adjudication framework per § 4.34 + § 4.36.

Per-booster activation classification:
  - ACTIVATE: Δ AUC ≥ threshold AND Δ ROI ≥ 0pp (dual-criterion gate)
  - SUBSTRATE-AMBIGUOUS-INVERSE: AUC↓+ROI↑ (§ 4.36 codification extension candidate)
  - SUBSTRATE-AMBIGUOUS-CALIBRATION-DEGRADATION: AUC↑+ROI↓ (§ 4.36 codified pattern)
  - KEEP-CURRENT: both axes regress

Hybrid C v2 retrain candidacy:
  - Combined L1 input substrate: substrate-validated ACTIVATE-classification boosters
  - Substrate-pragmatic: extend Hybrid C 32-input baseline → 32 + N ACTIVATE additions
  - Tony adjudication required on per-booster ACTIVATE classification before retrain
"""

import argparse
import glob
import json


def classify_booster(metrics):
    delta = metrics.get('dual_criterion_delta', {})
    inv = metrics.get('inverse_pattern_36_extension_candidate', {})

    delta_auc = delta.get('delta_auc')
    delta_roi = delta.get('delta_roi_pp')

    if delta_auc is None or delta_roi is None:
        return 'SUBSTRATE-THIN', 'Missing metrics; substrate-pragmatic re-measurement required'

    if delta.get('dual_criterion_pass'):
        return 'ACTIVATE', f'Δ AUC {delta_auc:+.4f} ≥ {delta.get("auc_threshold")} AND Δ ROI {delta_roi:+.1f}pp ≥ 0'

    if inv.get('detected'):
        return 'SUBSTRATE-AMBIGUOUS-INVERSE-PATTERN', \
               f'AUC↓+ROI↑ (Δ AUC {delta_auc:+.4f}, Δ ROI {delta_roi:+.1f}pp); § 4.36 codification extension candidate'

    if delta_auc > 0 and delta_roi < 0:
        return 'SUBSTRATE-AMBIGUOUS-CALIBRATION-DEGRADATION', \
               f'AUC↑+ROI↓ pattern (§ 4.36 codified); KEEP CURRENT'

    if delta_auc < 0 and delta_roi < 0:
        return 'KEEP-CURRENT', f'Both axes regress (Δ AUC {delta_auc:+.4f}, Δ ROI {delta_roi:+.1f}pp)'

    return 'SUBSTRATE-AMBIGUOUS-OTHER', f'Δ AUC {delta_auc:+.4f}, Δ ROI {delta_roi:+.1f}pp; Tony adjudication'


def build_candidacy(forensic_results, methodology_results=None):
    classifications = {}
    activate = []
    inverse_pattern = []

    for ensemble, metrics in forensic_results.items():
        cls, rationale = classify_booster(metrics)
        classifications[ensemble] = {'classification': cls, 'rationale': rationale}
        if cls == 'ACTIVATE':
            activate.append(ensemble)
        elif cls == 'SUBSTRATE-AMBIGUOUS-INVERSE-PATTERN':
            inverse_pattern.append(ensemble)

    methodology_validated = []
    methodology_investigation = []
    methodology_absent = []
    if methodology_results:
        for name, m in methodology_results.items():
            v = m.get('verdict', '')
            if 'substrate-validated' in v:
                methodology_validated.append(name)
            elif 'substrate-investigation' in v:
                methodology_investigation.append(name)
            elif 'substrate-absent' in v:
                methodology_absent.append(name)

    return {
        'per_ensemble_classification': classifications,
        'activate_candidates': activate,
        'inverse_pattern_36_extension_candidates': inverse_pattern,
        'hybrid_c_v2_retrain_candidacy': {
            'substrate_pragmatic_path': '32-input Hybrid C + ACTIVATE-classification additions',
            'activate_count': len(activate),
            'inverse_pattern_count': len(inverse_pattern),
            'tony_adjudication_required_before_retrain': True,
        },
        'methodology_aggregate': {
            'substrate_validated_production_candidates': methodology_validated,
            'substrate_investigation_required': methodology_investigation,
            'substrate_absent': methodology_absent,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subtrack1-forensic', required=True)
    parser.add_argument('--subtrack2-methodology-dir', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    with open(args.subtrack1_forensic) as f:
        forensic = json.load(f)

    methodology = {}
    for f in sorted(glob.glob(f'{args.subtrack2_methodology_dir}/*.json')):
        name = f.split('/')[-1].replace('.json', '')
        with open(f) as fp:
            methodology[name] = json.load(fp)

    candidacy = build_candidacy(forensic, methodology)
    with open(args.output, 'w') as f:
        json.dump(candidacy, f, indent=2, default=str)

    # Surface
    print('\n' + '=' * 80)
    print('HYBRID C v2 CANDIDACY ADJUDICATION SURFACE')
    print('=' * 80)
    print(f'\nPer-ensemble classification ({len(candidacy["per_ensemble_classification"])} ensembles):')
    for ens, c in candidacy['per_ensemble_classification'].items():
        print(f'  {ens[:60]:<60} {c["classification"]}')
        print(f'    {c["rationale"]}')
    print(f'\nACTIVATE candidates: {len(candidacy["activate_candidates"])}')
    for v in candidacy['activate_candidates']:
        print(f'  + {v}')
    print(f'\n§ 4.36 extension candidates (inverse pattern AUC↓+ROI↑): {len(candidacy["inverse_pattern_36_extension_candidates"])}')
    for v in candidacy['inverse_pattern_36_extension_candidates']:
        print(f'  ! {v}')
    print(f'\nMethodology substrate-validated production candidates:')
    for v in candidacy['methodology_aggregate']['substrate_validated_production_candidates']:
        print(f'  + {v}')


if __name__ == '__main__':
    main()
