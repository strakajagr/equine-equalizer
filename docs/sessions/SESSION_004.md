# SESSION 004 — Training Pipeline
**Date:** 2026-03-15
**Model:** Opus 4.6
**Goal:** Build complete XGBoost training pipeline: feature definitions, evaluation metrics, and end-to-end training script

---

## Files Created

| File | Purpose |
|------|---------|
| `model/features/feature_definitions.py` | Single source of truth for 72 feature names, groups, and metadata |
| `model/features/__init__.py` | Package init |
| `model/evaluation/metrics.py` | 6 evaluation functions: exacta/trifecta hit rate, top1/top3 accuracy, calibration, report |
| `model/evaluation/__init__.py` | Package init |
| `model/training/train.py` | Complete 7-step training pipeline with 8 functions + main |
| `model/training/__init__.py` | Package init |

---

## Training Pipeline Architecture

### Why `rank:pairwise`, Not Classification

A classification model would predict "will this horse win? yes/no" — treating each horse independently. This fails for horse racing because:

1. **The problem is inherently relative.** A horse doesn't win in a vacuum — it wins relative to the other horses in its race. A 85 Beyer horse wins a maiden race but loses a graded stakes.

2. **Finish position ordering matters more than win/lose.** We make money on exactas and trifectas — we need the model to get the relative ordering right, not just pick winners. A model that correctly identifies the top 3 horses (in any order) is profitable even if it rarely picks the exact winner.

3. **`rank:pairwise` optimizes exactly this.** It learns pairwise comparisons within each race group: "is Horse A likely to finish ahead of Horse B?" The model sees all horses in a race as a group and learns to rank them, which is the actual problem we're solving.

### GroupShuffleSplit: Why Race-Level Splits Prevent Data Leakage

Standard random train/test splits would put Horse A's entry from Race X in training and Horse B's entry from the same Race X in validation. This is data leakage because:

- The model learns field-relative features (beyer_vs_field_avg, front_runner_count_today, style_scenario_match) computed from ALL horses in the race
- If some horses from a race are in training, the model has indirect information about the validation horses

`GroupShuffleSplit(groups=race_id)` ensures all horses in a race are in the same split. The model never sees any horse from a validation race during training.

### Why Labels Are Inverted

XGBoost `rank:pairwise` treats higher labels as better. In racing, finish position 1 is best but numerically lowest. So we invert: `label = max_finish - actual_finish + 1`. The winner gets the highest label, last place gets 1.

### NDCG vs Exacta/Trifecta: Two Different Metrics for Two Different Purposes

| Metric | Used For | What It Measures |
|--------|----------|-----------------|
| **NDCG** | Training (early stopping) | Overall ranking quality — how well is the model ordering the entire field? Rewards correct ordering at the top more than the bottom. This is what XGBoost optimizes during training. |
| **Exacta hit rate** | Evaluation (our primary metric) | Did our top 2 predicted horses match the actual top 2 finishers? This is what determines P&L — an exacta box costs ~$2 and pays $20-$200+. |
| **Trifecta hit rate** | Evaluation (secondary metric) | Did our top 3 match the actual top 3? Higher payouts but harder to hit. |

**The Kalshi lesson applied:** In the Kalshi project, the Rules Engine was evaluated on overall win rate (41%) when the actual P&L driver was edge quality and position sizing. Here, we don't fall into the same trap: NDCG guides training, but we evaluate on exacta/trifecta hit rates because that's what generates revenue. A model with mediocre NDCG but high exacta hit rate is more valuable than the reverse.

### Feature Importance: Gain vs Weight

We use `importance_type='gain'` not `'weight'`:

- **Weight** = how many times a feature was used to split. High weight just means the feature had many useful split points — it says nothing about impact.
- **Gain** = average improvement in ranking quality each time the feature splits. High gain means when the model uses this feature, it learns something meaningful.

**What to expect from the first model:** Based on domain knowledge, we expect `beyer_last`, `beyer_avg_3`, `raw_speed_last`, `beyer_vs_raw_discrepancy`, `style_scenario_match`, and `lasix_first_time` to rank high. If `speed_sample_size` or `trainer_sample_size` rank unexpectedly high, the model may be using them as proxies for experience level rather than actual speed — worth investigating.

### Why `set_active` Is Manual

The pipeline registers the model in `model_versions` but does NOT automatically promote it to active. This is deliberate:

1. Review the evaluation report first
2. Check feature importance for signs of overfitting
3. Compare to previous model versions
4. Only then: `python train.py --set-active --version-name v1.0`

Auto-promotion means a bad model goes live immediately. The inference Lambda loads whatever model has `is_active = true` — promoting a degraded model means bad predictions for every race until someone notices.

---

## `train.py` Step by Step

```
Step 1: load_training_data()
  → Queries all qualifying races day by day
  → Loads entries and results for each race
  → Builds feature matrix via FeatureEngineeringService
  → Returns features_df + results_df

Step 2: prepare_xgboost_data()
  → Merges features with results (inner join)
  → GroupShuffleSplit by race_id (80/20)
  → Inverts finish positions for XGBoost labels
  → Creates DMatrix with group sizes for ranker

Step 3: train_model()
  → XGBoost rank:pairwise with NDCG eval metric
  → 500 max rounds, early stop at 50 no-improvement
  → Returns trained Booster

Step 4: get_feature_importance()
  → Extracts gain-based importance
  → Logs top 20 features

Step 5: evaluate_model()
  → Predicts on validation races
  → Converts scores to ranks and softmax probabilities
  → Computes exacta/trifecta hit rates, calibration
  → Prints evaluation report

Step 6: save_model()
  → Saves model.xgb + model_metadata.json locally
  → Optionally uploads to S3

Step 7: register_model()
  → Inserts model_versions row with all metrics
  → Optionally sets as active (manual flag only)
```

---

## Next Steps (Session 005+)

1. **Inference service implementation** — Load active model from S3, predict races, flag value plays
2. **Equibase data parser** — Implement `parse_equibase_file()` once 2023 dataset format is confirmed
3. **Historical backfill** — Load 2023 data → run training → evaluate first model
4. **Frontend scaffold** — Initialize Vite/React with race card and prediction views
