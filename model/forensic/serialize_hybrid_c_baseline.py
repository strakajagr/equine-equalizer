"""
Serialize current production Hybrid C cohort as substrate-baseline for Build Dispatches 2 + 3 + Tier 2 execution.

Substrate-pragmatic per substrate-actual hybrid_c_predictions schema:
  - ensemble_version (varchar) is the version discriminator (NOT model_version_id)
  - predicted_at (timestamp) is the date column
  - horse_id is TEXT (not UUID) — type coercion applied at merge boundary
  - Predictions begin 2026-05-16; pre-dates substrate-thin
"""

import json
import sys


HYBRID_C_UUID_INFORMATIONAL = '2d34b010-f17a-492e-8f7c-270bd393731d'
ENSEMBLE_VERSION_VALUE = 'option_c_hybrid_ensemble_20260515'


def serialize_baseline(output_path):
    baseline = {
        'name': 'hybrid_c_option_c_v1_baseline',
        'model_version_id_informational': HYBRID_C_UUID_INFORMATIONAL,
        'model_type': 'ensemble_hybrid_option_c',
        's3_artifact_path': 's3://equine-model-artifacts/ensemble/option_c_hybrid_ensemble_20260515.json',

        # Substrate-pragmatic per substrate-actual hybrid_c_predictions schema:
        'predictions_table': 'hybrid_c_predictions',
        'prediction_column': 'hybrid_c_win_probability',
        'version_column': 'ensemble_version',
        'version_value': ENSEMBLE_VERSION_VALUE,
        'date_column': 'predicted_at',
        'horse_id_cast': None,

        'predictions_window': '2026-05-16..ongoing',
        'description': 'Current production Hybrid C cohort substrate-baseline; predictions begin 2026-05-16',
        'substrate_version': 'v3-patched-f',
    }

    with open(output_path, 'w') as f:
        json.dump(baseline, f, indent=2)
    print(f"Hybrid C baseline serialized: {output_path}")


if __name__ == '__main__':
    output = sys.argv[1] if len(sys.argv) > 1 else '/tmp/hybrid_c_baseline.json'
    serialize_baseline(output)
