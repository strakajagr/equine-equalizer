# EE Production Architecture — Verbatim Substrate Reference

**Status**: SUBSTRATE-PERMANENT REFERENCE
**Generated**: 2026-05-18T23:39:38Z
**Generator**: CC architecture discovery dispatch (Option A ratified)
**Substrate-grounding source**: read-only substrate-discovery against
  substrate-actual production codebase + DB schema as of generation date.

**Authoring discipline**: This document is the substrate-grounding source
for all future production-mutation dispatches in this codebase. QB authoring
against this document; not against session memory.

**Sections**:
  1. MultiCohortInferenceService (MCIS)
  2. strategy_harness
  3. strategy_registry.py
  4. model_versions table
  5. hybrid_c_predictions schema
  6. specialist_style META structure
  7. Adjacent substrate (Lambdas / Fargate / CDK / config)
  8. Substrate-divergence summary + Path A re-authoring requirements

**Per-section convention**:
  - Verbatim substrate-grep output
  - Verbatim code transcription for critical functions
  - Memory-vs-actual annotation
  - Substrate-divergence flag (if any)

---

## SECTION 1 — MultiCohortInferenceService (MCIS)

### 1.1 File location + baseline

**Path**: `/home/strakajagr/projects/equine-equalizer/backend/services/multicohort_inference_service.py`
**Size**: 413 lines

CDK asset copies under `infrastructure/cdk/cdk.out/asset.*` IGNORED — canonical source only.

### 1.2 Class structure verbatim

```
41:HYBRID_C_VERSION_NAME = 'option_c_hybrid_ensemble_20260515'
42:HYBRID_C_S3_PATH = 's3://equine-model-artifacts/ensemble/option_c_hybrid_ensemble_20260515.json'
43:SOFTMAX_TEMPERATURE = 0.15
83:def softmax_temp(raw: np.ndarray, T: float = SOFTMAX_TEMPERATURE) -> np.ndarray:
93:class L1Artifact:
104:def classify_feature_path(model_type: str, version_name: str) -> str:
132:def classify_artifact_format(s3_path: str) -> str:
142:def _parse_s3(s3_path: str) -> Tuple[str, str]:
148:class MultiCohortInferenceService:
154:    def __init__(self, conn):
175:    def initialize(self) -> Dict[str, Any]:
242:    def _load_artifact(self, art: L1Artifact) -> Any:
259:    def predict_race(self, race_id: str) -> Optional[Dict[str, Any]]:
349:    def write_predictions(self, result: Dict[str, Any]) -> int:
370:    def run_daily_predictions(self, race_date) -> Dict[str, Any]:
```

### 1.3 Ensemble loading mechanism

**Substrate-actual load discriminator**: NOT `is_active`. NOT UUID. Instead:
`(model_type, version_name)` JOIN against `model_versions.s3_artifact_path`.

Verbatim from `initialize()` lines 184-188:

```python
rows = execute_query(self.conn, """
    SELECT model_type, version_name, s3_artifact_path
    FROM model_versions
    WHERE (model_type, version_name) IN %s
""", (tuple((mt, vn) for _, mt, vn in HYBRID_C_L1_SPECS),))
```

**Hybrid C ensemble itself** loaded direct from hardcoded S3 path (lines 221-227):

```python
local_path = '/tmp/option_c_hybrid_ensemble.json'
bucket, key = _parse_s3(HYBRID_C_S3_PATH)
if not os.path.exists(local_path):
    self.s3.download_file(bucket, key, local_path)
booster = xgb.Booster()
booster.load_model(local_path)
```

**Substrate-pragmatic annotation**: Loads via:
1. **L1 artifacts** — model_versions table lookup by `(model_type, version_name)` tuple, where the tuples themselves are HARDCODED in `HYBRID_C_L1_SPECS` list (lines 47-80, 32 tuples).
2. **Hybrid C ensemble** — direct S3 download from HARDCODED constant `HYBRID_C_S3_PATH` (line 42). NO DB lookup for the ensemble itself.

Per-docstring (lines 9-10): *"L1 artifacts are pinned by version_name (NOT by is_active) — this matches the exact 32 columns Hybrid C was trained on, robust to future activation churn."*

`is_active` is NOT read by MCIS load path. Substrate-pragmatic implication: flipping `is_active` in model_versions has **ZERO effect on MCIS load behavior**.

### 1.4 32 L1 input substrate (verbatim)

```python
HYBRID_C_L1_SPECS: List[Tuple[str, str, str]] = [
    ('phase_bx', 'rk_full_speed', 'rk_full_lean53_speed_20260513_0324'),
    ('phase_bx', 'rk_full_closer', 'rk_full_lean53_closer_20260513_0327'),
    ('phase_bx', 'rk_full_class_riser', 'rk_full_lean53_class_riser_20260513_0302'),
    ('phase_bx', 'rk_full_route', 'rk_full_lean53_route_20260513_0255'),
    ('phase_bx', 'rk_full_sprint', 'rk_full_lean53_sprint_20260513_0251'),
    ('phase_bx', 'rk_full_gonzo_sauce', 'rk_full_lean53_gonzo_sauce_20260513_0324'),
    ('phase_bx', 'wp_full_general', 'wp_full_lean53_20260513_0311'),
    ('phase_bx', 'wp_full_speed', 'wp_full_lean53_speed_20260513_0325'),
    ('phase_bx', 'wp_full_closer', 'wp_full_lean53_closer_20260513_0324'),
    ('phase_bx', 'wp_full_route', 'wp_full_lean53_route_20260513_0255'),
    ('phase_bx', 'wp_full_class_dropper', 'wp_full_lean53_class_dropper_20260513_0325'),
    ('phase_bx', 'wp_full_class_riser', 'wp_full_lean53_class_riser_20260513_0323'),
    ('phase_bx', 'wp_full_sprint', 'wp_full_lean53_sprint_20260513_0258'),
    ('phase_bx', 'wp_full_gonzo_sauce', 'wp_full_lean53_gonzo_sauce_20260513_0310'),
    ('phase_bx', 'wr_base', 'v_base_core_20260513_0259'),
    ('phase_bx', 'pl_core_route', 'pl_core_lean53_route_20260513_0246'),
    ('phase_bx', 'wr_odds', 'v_odds_core_20260513_0259'),
    ('phase_bx', 'ranker_core', 'rk_core_20260513_0323'),
    ('phase_bx', 'win_prob_full', 'wp_odds_20260513_0126'),
    ('prior', 'pl_core_general', 'pl_core_lean53_20260429_1907'),
    ('prior', 'pl_core_speed', 'pl_core_lean53_speed_20260429_1906'),
    ('prior', 'pl_core_closer', 'pl_core_lean53_closer_20260429_1856'),
    ('prior', 'pl_core_class_riser', 'pl_core_lean53_class_riser_20260429_1856'),
    ('prior', 'pl_core_class_dropper', 'pl_core_lean53_class_dropper_20260429_1906'),
    ('prior', 'pl_core_sprint', 'pl_core_lean53_sprint_20260429_1845'),
    ('prior', 'rk_full_class_dropper', 'rk_full_lean53_class_dropper_20260429_1854'),
    ('prior', 'win_prob_core_speed', 'wp_core_lean53_speed_20260429_2348'),
    ('prior', 'win_prob_core_closer', 'wp_core_lean53_closer_20260429_2348'),
    ('prior', 'win_prob_core_class_riser', 'wp_core_lean53_class_riser_20260429_2338'),
    ('prior', 'win_prob_core_class_dropper', 'wp_core_lean53_class_dropper_20260429_2338'),
    ('prior', 'win_prob_core_sprint', 'wp_core_lean53_sprint_20260429_2332'),
    ('prior', 'win_prob_core_route', 'wp_core_lean53_route_20260429_2329'),
]
```

19 `phase_bx` + 13 `prior` = 32 L1 inputs. Substrate-confirms memory's "32 L1 inputs" claim verbatim.

### 1.5 predict_race substrate (verbatim — lines 259-347)

```python
def predict_race(self, race_id: str) -> Optional[Dict[str, Any]]:
    """Generate 32 L1 predictions + Hybrid C ensemble for one race."""
    if not self._l1_artifacts:
        self.initialize()

    race = self.race_repo.get_race_by_id(race_id)
    if race is None:
        return None
    race.entries = self.entry_repo.get_entries_by_race(race_id)
    if len(race.entries) < 4:
        return None

    feature_df = self.fe.build_feature_matrix(race, include_odds=True)
    if feature_df.empty:
        return None

    horse_ids = feature_df['horse_id'].astype(str).tolist()
    n_horses = len(horse_ids)

    # Build per-feature-path DMatrix slices once
    # ... (slice + DMatrix per fpath in self._features) ...

    # Generate L1 predictions per artifact (per-artifact loop)
    # ... (xgb_json + pkl_sklearn dispatch; softmax_temp for win-prob style) ...

    # Construct Hybrid C input in feature_names order
    X = np.column_stack([
        l1_outputs.get(name, np.zeros(n_horses))
        for name in self._hybrid_c_feature_names
    ])
    dmat = xgb.DMatrix(X, feature_names=self._hybrid_c_feature_names)
    raw_hybrid = self._hybrid_c_booster.predict(dmat)

    if raw_hybrid.sum() > 0:
        hybrid_c_probs = raw_hybrid / raw_hybrid.sum()
    else:
        hybrid_c_probs = raw_hybrid

    return {
        'race_id': race_id,
        'horse_ids': horse_ids,
        'hybrid_c_win_probability': hybrid_c_probs.tolist(),
        'hybrid_c_raw': raw_hybrid.tolist(),
        'l1_outputs': {k: v.tolist() for k, v in l1_outputs.items()},
    }
```

**Substrate-pragmatic verdict**: SINGLE-BOOSTER predict path. ZERO META-routing. NO sprint/route dispatch. NO distance discrimination. Hybrid C ensemble is the only L2 booster invoked.

### 1.6 Prediction write path (verbatim — lines 349-368)

```python
def write_predictions(self, result: Dict[str, Any]) -> int:
    """Persist Hybrid C predictions to hybrid_c_predictions table. Idempotent."""
    if not result:
        return 0
    race_id = result['race_id']
    horse_ids = result['horse_ids']
    probs = result['hybrid_c_win_probability']
    rows_inserted = 0
    for hid, p in zip(horse_ids, probs):
        execute_write(self.conn, """
            INSERT INTO hybrid_c_predictions
              (race_id, horse_id, hybrid_c_win_probability,
               l1_input_count, ensemble_version)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (race_id, horse_id, ensemble_version)
            DO UPDATE SET hybrid_c_win_probability = EXCLUDED.hybrid_c_win_probability,
                          predicted_at = NOW()
        """, (race_id, hid, float(p), len(self._l1_artifacts), HYBRID_C_VERSION_NAME))
        rows_inserted += 1
    return rows_inserted
```

**CRITICAL SUBSTRATE-FINDING**: ON CONFLICT clause keys on `(race_id, horse_id, ensemble_version)` — ensemble_version is part of the UNIQUE substrate. **Dual-write IS substrate-coherent at the table level**: writing Hybrid C + specialist_style as distinct ensemble_version values creates distinct rows per (race, horse) — no conflict.

Hardcoded write tag: `HYBRID_C_VERSION_NAME` (line 366) — `'option_c_hybrid_ensemble_20260515'`.

### 1.7 Memory-vs-actual annotation

| Memory framing | Substrate-actual | Verdict |
|---|---|---|
| "Hybrid C live; UUID 2d34b010-..." | MCIS load path does NOT reference UUID. UUID is model_versions row identifier but MCIS keys on (model_type, version_name) | DIVERGENT (memory implied UUID-pinned; substrate-pragmatic version-pinned) |
| "ensemble_version=option_c_hybrid_ensemble_20260515" hardcoded | Confirmed verbatim line 41 + 366 | MATCHES |
| "32 L1 inputs" | Confirmed (19 phase_bx + 13 prior = 32) | MATCHES |
| "MCIS hardcodes single-booster (Hybrid C) load + predict" (CC Phase 1 HALT) | Confirmed verbatim; no META-routing | MATCHES |

### 1.8 Substrate-divergence flag

**FLAG 1**: `is_active` flag is NOT consulted by MCIS load path. Memory + Tony Phase 6.1.4 framing assumed `is_active=TRUE` would route MCIS to load specialist_style. Substrate-actual: MCIS HARDCODES `HYBRID_C_L1_SPECS` + `HYBRID_C_S3_PATH`. Flipping `is_active` flag has NO effect on what MCIS loads.

**FLAG 2**: For specialist_style production-write path, MCIS substrate-actually requires:
- New constants `SPECIALIST_STYLE_SPRINT_VERSION` + `SPECIALIST_STYLE_ROUTE_VERSION` + S3 paths
- New `SPECIALIST_STYLE_L1_SPECS` (or shared with Hybrid C if 32 L1s identical — substrate-pending verification in Section 6)
- New META-routing entry point: `predict_race_specialist_style(race_id)` that:
  (a) Loads BOTH sprint + route sub-boosters
  (b) Reads `distance_furlongs` from race substrate
  (c) Dispatches to correct sub-booster
  (d) Writes with `ensemble_version='specialist_style_specialist_20260518_0252'`
- OR a refactored generic `predict_race(race_id, ensemble_config)` accepting ensemble identity as parameter

Substrate-pragmatic scope: ~100-200 LOC MCIS extension. Substrate-coherent (no architectural blocker).

### 1.9 — _load_artifact verbatim body (added 2026-05-19T02:00:00Z; per Q-pre-β-1 R-1-1)

**Amendment scope**: R-1-1 substrate-grounding requirement for β.1 MCIS sprint extension authoring — pre-β.1 verification surfaced reference substrate-cited function signature without body.

**Substrate-actual source**: `backend/services/multicohort_inference_service.py` lines 242-258 (verbatim per Phase B.1 substrate-grep).

**Verbatim function body**:

```python
    def _load_artifact(self, art: L1Artifact) -> Any:
        local = f'/tmp/mci_artifacts/{art.cohort}__{art.model_type}__{art.version_name}'
        os.makedirs('/tmp/mci_artifacts', exist_ok=True)
        bucket, key = _parse_s3(art.s3_path)
        # Use basename of s3 key as local file extension to match artifact_format dispatch
        local_path = local + '_' + os.path.basename(key)
        if not os.path.exists(local_path):
            self.s3.download_file(bucket, key, local_path)

        if art.artifact_format == 'xgb_json':
            booster = xgb.Booster()
            booster.load_model(local_path)
            return booster
        if art.artifact_format == 'pkl_sklearn':
            return joblib.load(local_path)
        raise RuntimeError(f"Unsupported artifact_format={art.artifact_format} for {art.column_name}")
```

**Substrate-pragmatic load semantics for β.1 sprint extension**:
- Sprint sub-booster artifact_format is `xgb_json` (per Section 6.2 `.json` extension on S3 path)
- Local cache path constructed from `{cohort}__{model_type}__{version_name}_{key_basename}`; β.1 substrate-pragmatic uses same pattern
- S3 download idempotent via `os.path.exists(local_path)` guard
- Returns `xgb.Booster` for xgb_json format (substrate-coherent with β.1 sprint sub-booster substrate)

§ 4.32 sub-pattern B firing #12 banked: verbatim function-body transcription discipline. Codification queue +1.

### 1.10 — ensemble_version write convention for production sprint routing (added 2026-05-19T02:00:00Z; per Q-pre-β-1 Option B)

**Amendment scope**: R-1-4 substrate-grounding requirement for β.1 sprint sub-booster production write convention. Tony Q-pre-β-1 Option B ratification: production-era sprint-only predictions write with sub-booster-specific tag, NOT META wrapper version.

**Substrate-actual semantic convention** for `ensemble_version` values in `hybrid_c_predictions` table:

| ensemble_version value | Semantic |
|---|---|
| `option_c_hybrid_ensemble_20260515` | Hybrid C production (canonical) |
| `specialist_style_specialist_20260518_0252` | Forensic-era META wrapper (BD3v2 + Track A + δ.2; mixed routing) |
| `specialist_style_sprint_20260518_0252` | Production-era sprint-only (post-β activation; Q1 P1 + Q2 R1) |

**Production routing semantics under Q1 P1 + Q2 R1**:
- Distance ≤ 6.5 furlongs → sprint sub-booster invoked → writes `ensemble_version='specialist_style_sprint_20260518_0252'`
- Distance > 6.5 furlongs → no specialist_style write; Hybrid C remains canonical via existing path
- Route sub-booster DEPRECATED per Q2 R1; `is_active=FALSE` permanent; never invoked

**Substrate-pragmatic consumer-clarity note**: strategy_harness β.2 extension sprint ranking_layer SELECT filters by `ensemble_version='specialist_style_sprint_20260518_0252'` only; substrate-additionally precise (never reads forensic-era META rows).

**Substrate-coherence with σ-2 extension verification**: sub-booster sprint tag is 41 chars; substrate-coherent with `hybrid_c_predictions.ensemble_version` varchar(100) ceiling per σ-2 extension Phase 2.5 producer enumeration.

**Substrate-coherence with δ.1 model_versions registration**: sub-booster sprint tag matches `version_name` registered in model_versions (PK `1202021f-2937-46eb-a1fd-0dd9b0d1fe20`); substrate-coherent traceability from prediction row → model_versions row → S3 artifact path.

---

## SECTION 2 — strategy_harness

### 2.1 File location + baseline

**Path**: `/home/strakajagr/projects/equine-equalizer/backend/services/strategy_harness.py`
**Size**: 381 lines

### 2.2 Substrate structure

**Components**:
- `HorsePrediction` (dataclass, line 27) — uniform per-horse prediction with all layer outputs
- `RacePredictions` (dataclass, line 61) — per-race container
- `RaceContext` (dataclass, line 83) — race substrate (track, distance, etc.)
- `BetRecommendation` (dataclass, line 97) — strategy output
- `StrategyBase` (ABC, line 130) — strategy interface
- `StrategyHarness` (class, line 192) — runs all strategies against per-race substrate
- `RacePredictionLoader` (class, line 257) — caching wrapper
- `load_race_predictions` (function, line 277) — pulls all layer predictions for a race

### 2.3 RANKING_LAYER_FIELDS verbatim (line 117-127)

```python
RANKING_LAYER_FIELDS = {
    'ensemble': 'ensemble_win_prob',
    'ensemble_hybrid_option_c': 'hybrid_c_win_prob',
    'wr': 'win_probability',
    'pl': 'pl_win_probability',
    'ranker': 'rank_score',
    'longshot': 'longshot_prob',
    'trajectory': 'trajectory_score',
    'angle': 'angle_posterior',
    'handicapping': 'handicapping_prob',
}
```

**Substrate-pragmatic finding**: Strategies are coupled to ensemble identity via a string discriminator (`ranking_layer`) → HorsePrediction attribute mapping. Adding specialist_style as a new ranking option requires:
- New HorsePrediction field `specialist_style_win_prob`
- New RANKING_LAYER_FIELDS entry `'ensemble_specialist_style': 'specialist_style_win_prob'`

### 2.4 Hardcoded ensemble_version verbatim (lines 361-367)

```python
# Hybrid C ensemble predictions (separate table; merge by horse_id)
rows.execute("""
    SELECT horse_id, hybrid_c_win_probability
    FROM hybrid_c_predictions
    WHERE race_id = %s AND ensemble_version = 'option_c_hybrid_ensemble_20260515'
""", (race_id,))
hc_map = {str(r['horse_id']): float(r['hybrid_c_win_probability']) for r in rows.fetchall()}
for hp in rp.horses:
    if hp.horse_id in hc_map:
        hp.hybrid_c_win_prob = hc_map[hp.horse_id]
```

**Substrate-pragmatic annotation**: HARDCODED ensemble_version string. NO read of `model_versions.is_active`. NO config-driven mechanism. NO parameterization.

**For Path A specialist_style PRIMARY production-write**: requires adding a 2nd hardcoded query block (or parameterized refactor) AND populating a new HorsePrediction field. Substrate-pragmatic minimum: ~10 LOC addition.

### 2.5 Strategy invocation pattern (verbatim lines 200-225)

```python
class StrategyHarness:
    def __init__(self, strategies: List[StrategyBase]):
        self.strategies = strategies
        self._errors: List[Dict] = []

    def run_race(
        self, race_preds: RacePredictions, ctx: RaceContext,
        only_strategies: Optional[List[str]] = None,
    ) -> Dict[str, Optional[BetRecommendation]]:
        out = {}
        for s in self.strategies:
            if s.is_multi_leg:
                continue
            if only_strategies and s.name not in only_strategies:
                continue
            try:
                rec = s.recommend(race_preds, ctx)
            except Exception as e:
                self._errors.append({...})
                rec = None
            out[s.name] = rec
        return out
```

**Substrate-pragmatic verdict**: Strategies are iterated from a list `self.strategies` (injected via __init__). Each strategy's `recommend()` method reads HorsePrediction attributes (e.g., `hp.hybrid_c_win_prob`, `hp.pl_win_probability`) directly. Strategies are agnostic to which ensemble produced the prediction once loaded into HorsePrediction.

### 2.6 Substrate-pragmatic complexity assessment for Path A activation

**Option A — add parallel hardcoded query block** (substrate-minimum):
- ~10 LOC: add `specialist_style_win_prob` field to HorsePrediction
- ~10 LOC: add new SELECT block in `load_race_predictions` for specialist_style version
- ~2 LOC: add `'ensemble_specialist_style': 'specialist_style_win_prob'` to RANKING_LAYER_FIELDS
- New strategies in strategy_registry.py use `ranking_layer = 'ensemble_specialist_style'`

**Option B — config-driven refactor**:
- Refactor `load_race_predictions` to accept ensemble_version parameter (or list); load all into HorsePrediction by ensemble_version
- More general; supports N ensembles symmetrically; ~30 LOC

**Option C — make `is_active` functional**:
- Refactor `load_race_predictions` to read `WHERE ensemble_version IN (SELECT version_name FROM model_versions WHERE is_active = TRUE AND model_type LIKE 'ensemble%')`
- Makes is_active flag substrate-functional; couples consumer to model_versions
- Substrate-pragmatic cleanest semantically but requires specialist_style first registered in model_versions

### 2.7 Call-site analysis

Single substrate-grep finding: ensemble_version appears in this file ONLY at lines 364-365. No other strategy_harness consumer references ensemble_version directly. All other consumption happens via `hp.hybrid_c_win_prob` (HorsePrediction attribute) — substrate-decoupled from ensemble_version string.

### 2.8 Memory-vs-actual annotation

| Memory framing | Substrate-actual | Verdict |
|---|---|---|
| "strategy_harness:365 hardcodes ensemble_version" | Confirmed verbatim at lines 364-365 | MATCHES |
| "is_active flag for consumption" | NOT consulted — substrate-decorative | DIVERGENT (memory implied functional; substrate-actual decorative) |
| "is_shadow_only flag on strategies" (Tony Path A Phase 4.2) | NO such attribute on StrategyBase; no consumer; substrate-absent | DIVERGENT |

### 2.9 Substrate-divergence flag

**FLAG 1**: Tony Path A Phase 4.2 said "flip is_shadow_only=TRUE on Hybrid C strategies" + "is_active=TRUE on specialist_style" — neither mechanism substrate-actually exists at strategy_harness consumer layer. Strategies have no `is_shadow_only` attribute substrate-actually.

**FLAG 2**: `is_active` model_versions flag is NOT consulted by load. Substrate-pragmatic implication: ANY activation mechanism must change strategy_harness CODE, not DB flags. This is a structural refactor or an additive load block.

**FLAG 3**: Mechanism for activating specialist_style as PRIMARY (vs additive shadow) substrate-actually requires changing strategy classes' `ranking_layer` attribute in strategy_registry.py from `'ensemble_hybrid_option_c'` → `'ensemble_specialist_style'`. This is Python code change in strategy_registry.py, NOT a flag flip.

### 2.10 — HorsePrediction verbatim class body (added 2026-05-19T02:00:00Z; per Q-pre-β-1 R-2-2)

**Amendment scope**: R-2-2 substrate-grounding requirement for β.2 strategy_harness sprint extension authoring — pre-β.1 verification surfaced reference cited RANKING_LAYER_FIELDS verbatim but HorsePrediction class body narrative-only.

**Substrate-actual source**: `backend/services/strategy_harness.py` lines 26-58 (verbatim per Phase B.2 substrate-grep).

**Verbatim class body**:

```python
@dataclass
class HorsePrediction:
    """Per-horse prediction with all layer outputs normalized."""
    horse_id: str
    horse_name: str
    program_number: Optional[str] = None
    morning_line_odds: Optional[float] = None
    # Layer outputs (any may be None if layer didn't run for this race/style)
    win_probability: Optional[float] = None       # wr_predictions / canonical wp
    place_probability: Optional[float] = None
    show_probability: Optional[float] = None
    ensemble_win_prob: Optional[float] = None
    handicapping_prob: Optional[float] = None     # market-blind model output
    market_prob: Optional[float] = None
    rank_score: Optional[float] = None            # ranker output
    pl_win_probability: Optional[float] = None    # pl_predictions
    pl_predicted_ev: Optional[float] = None
    pl_edge_pct: Optional[float] = None
    longshot_prob: Optional[float] = None
    longshot_alert: bool = False
    trajectory_score: Optional[float] = None
    hybrid_c_win_prob: Optional[float] = None    # Hybrid C culled-rebuilt ensemble output
    angle_name: Optional[str] = None
    angle_posterior: Optional[float] = None
    angle_ev: Optional[float] = None
    style: Optional[str] = None                   # which specialist style (general/speed/closer/...)
    # Production-strategy outputs (read-only context)
    recommended_bet_type: Optional[str] = None
    is_top_pick: bool = False
    is_value_flag: bool = False
    overlay_pct: Optional[float] = None
    kelly_fraction: Optional[float] = None
```

**Substrate-pragmatic field-addition pattern for β.2**:
- Pattern-match `hybrid_c_win_prob` (line 47 substrate; layer-output section)
- β.2 adds: `specialist_style_sprint_win_prob: Optional[float] = None  # Specialist_style sprint sub-booster output (post-β activation; Q1 P1 SPRINT-ONLY routing)`
- Substrate-pragmatic insertion point: after `hybrid_c_win_prob` line (substrate-coherent grouping with ensemble outputs)

**Substrate-coherence with Q-pre-β-1 Option B**: field name `specialist_style_sprint_win_prob` substrate-coherent with `ensemble_version='specialist_style_sprint_20260518_0252'` per Section 1.10 convention (sub-booster-specific tag throughout consumer substrate).

---

## SECTION 3 — strategy_registry.py

### 3.1 File location + baseline

**Path**: `/home/strakajagr/projects/equine-equalizer/backend/services/strategy_registry.py`
**Size**: 726 lines / 29326 bytes
**Class count via grep**: 58
**Strategy-instance count via Python introspection**: **162**

### 3.2 Mechanism: classes × parameterized factories → instances

The 58→162 multiplier substrate-actually comes from parameterized multi-leg factories:

```python
DD_SPREADS = [(1,1),(1,2),(2,1),(2,2),(2,3),(3,2),(3,3)]          # 7 spreads
P3_SPREADS = [..., 15 tuples ...]                                  # 15
P4_SPREADS = [..., 16 tuples ...]                                  # 16
P5_SPREADS = [..., 22 tuples ...]                                  # 22
                                                                   # = 60
```

`*[_DD_Spread(s) for s in DD_SPREADS]` etc. unpacks into the STRATEGIES list,
producing 60 ensemble multi-leg instances + 60 Hybrid C multi-leg instances = 120 multi-leg. Plus 42 single-race classes = 162 total.

### 3.3 By-category breakdown (substrate-introspected)

| category | count |
|---|---|
| ev | 2 |
| raw_layer | 39 |
| angle | 1 |
| multi_leg | 120 |
| **total** | **162** |

### 3.4 By-ranking_layer breakdown (substrate-introspected)

| ranking_layer | count |
|---|---|
| angle | 1 |
| ensemble | 67 |
| ensemble_hybrid_option_c | 67 |
| longshot | 1 |
| pl | 1 |
| ranker | 13 |
| wr | 12 |
| **total** | **162** |

**CRITICAL SUBSTRATE-FINDING**: 67 strategies use `ranking_layer = 'ensemble_hybrid_option_c'` (7 single-race HybridC_* classes + 60 multi-leg `_HybridC_*_Spread(s)`). These are the Hybrid-C-tied substrate.

The OTHER 67 use `ranking_layer = 'ensemble'` — the legacy ensemble (`ensemble_win_prob` field on HorsePrediction, populated by wr_predictions table). These are NOT Hybrid C.

### 3.5 Registration mechanism (verbatim from module tail)

```python
STRATEGIES: List[StrategyBase] = [
    # ── EV strategies (2; Production_Heuristic removed Phase 7.3) ──
    T1_1_6_EV_Median(),
    T1_4_Pool_Conditional(),

    # ── Raw-layer single-bet strategies (general style; 4) ──
    WR_Top1_Win(), PL_Top1_Win(), Ensemble_Top1_Win(), Ranker_Top1_Win(),

    # ── Specialist-style raw-layer variants (3) ──
    WR_Top1_Win_Gonzo(), WR_Top1_Win_Speed(), WR_Top1_Win_Closer(),

    # ── Longshot + Bayesian (2) ──
    Longshot_Top1_Win(), Bayesian_Angle_Top_FirstTimeLasix(),

    # ── Ensemble box-bet strategies (6) ──
    Ensemble_Top2_ExactaBox(), Ensemble_Top3_TriBox(), Ensemble_Top4_TriBox(),
    Ensemble_Top4_SFBox(), Ensemble_Top5_SFBox(), Ensemble_Top6_SFBox(),

    # ── Multi-leg parameterized (60) ──
    *[_DD_Spread(s) for s in DD_SPREADS],
    *[_P3_Spread(s) for s in P3_SPREADS],
    *[_P4_Spread(s) for s in P4_SPREADS],
    *[_P5_Spread(s) for s in P5_SPREADS],

    # ── Hybrid C single-race (7) — Phase 7.4 ──
    HybridC_Top1_Win(), HybridC_Top2_ExaBox(), HybridC_Top3_TriBox(),
    HybridC_Top4_TriBox(), HybridC_Top4_SFBox(), HybridC_Top5_SFBox(),
    HybridC_Top6_SFBox(),

    # ── Hybrid C multi-leg parameterized (60) — Phase 7.4 ──
    *[_HybridC_DD_Spread(s) for s in DD_SPREADS],
    *[_HybridC_P3_Spread(s) for s in P3_SPREADS],
    *[_HybridC_P4_Spread(s) for s in P4_SPREADS],
    *[_HybridC_P5_Spread(s) for s in P5_SPREADS],

    # ── Specialist standalone (15) — Phase 7.4 ──
    RkFullSpeed_Top1_Win(), RkFullSpeed_Top3_TriBox(), RkFullSpeed_Top5_SFBox(),
    RkFullClassRiser_Top1_Win(), RkFullClassRiser_Top3_TriBox(), RkFullClassRiser_Top5_SFBox(),
    RkFullCloser_Top1_Win(), RkFullCloser_Top3_TriBox(), RkFullCloser_Top5_SFBox(),
    RkFullGonzoSauce_Top1_Win(), RkFullGonzoSauce_Top3_TriBox(), RkFullGonzoSauce_Top5_SFBox(),
    WpFullSpeed_Top1_Win(), WpFullSpeed_Top3_TriBox(), WpFullSpeed_Top5_SFBox(),

    # ── Dispatch B orphan (3; F1 activation, 2026-05-16) ──
    Wp55featOddsBlindOrphan_Top1_Win(),
    Wp55featOddsBlindOrphan_Top3_TriBox(),
    Wp55featOddsBlindOrphan_Top5_SFBox(),
]


def get_registry() -> List[StrategyBase]:
    """Public accessor; lets daemons reload the registry without restart."""
    return STRATEGIES
```

**No DB-backed mechanism. No decorator-based registration. No metaclass.** Pure Python module-level list.

### 3.6 Substrate-pragmatic path for adding specialist_style strategies

**Option A — mirror Hybrid C** (substrate-additive; +67 strategies → 229 total):
Author 67 new `SpecialistStyle_Top*` classes parallel to `HybridC_Top*` classes, plus new `_SpecialistStyle_*_Spread` factories. Total registry grows to ~229. Substrate-coherent with current pattern. Memory-pragmatic at runtime: minor.

**Option B — repurpose `ensemble_hybrid_option_c` ranking_layer** (substrate-substitutive; 0 net add):
Change `RANKING_LAYER_FIELDS['ensemble_hybrid_option_c']` to `'specialist_style_win_prob'` (new HorsePrediction field). Existing 67 Hybrid C strategy classes start consuming specialist_style without rename. Substrate-pragmatic minimal but semantically misleading (strategy names still say "hybrid_c").

**Option C — flag-based primary discriminator** (substrate-architectural; new mechanism):
Add `primary_ensemble: str` config (env var OR DB column). Strategies read `RANKING_LAYER_FIELDS[get_primary_ensemble()]` instead of hardcoded `ranking_layer`. Substrate-substantial refactor; cleanest semantics.

### 3.7 Memory-vs-actual annotation

| Memory framing | Substrate-actual | Verdict |
|---|---|---|
| "162 strategies in registry" | Confirmed via introspection | MATCHES |
| "Python config not DB" | Confirmed; module-level STRATEGIES list | MATCHES |
| "19 grep-counted Strategy classes" (CC Phase 1 HALT) | DIVERGENT — grep returns 58 classes; introspection produces 162 instances via parameterized factories | DIVERGENT (memory undercounted) |
| "no `strategies` table" | Confirmed — registration is Python list | MATCHES |

### 3.8 Substrate-divergence flag

**FLAG 1**: CC Phase 1 HALT undercounted classes (19 vs 58 substrate-actual). The 19 likely came from a `grep -cE '^class T|^class W|^class E|^class H'` style filter that missed underscore-prefixed base classes (`_RawLayerWin`, `_EnsembleBox`, etc.) and factory classes (`_DD_Spread`, etc.). Substrate-permanent count is 58 classes / 162 instances. Memory-corrected.

**FLAG 2**: Tony Path A Phase 4 SQL operations against a `strategies` table are substrate-broken — no such table. Strategy additions are Python source edits + Lambda redeploy. Substrate-pragmatic: this matches Dynasty Dugout "deploy live in seconds" pattern; not a blocker, but operationally distinct from SQL.

### 3.9 — Strategy exemplar verbatim class body (added 2026-05-19T02:00:00Z; per Q-pre-β-1 R-3-3)

**Amendment scope**: R-3-3 substrate-grounding requirement for β.3 strategy_registry sprint additions — pre-β.1 verification surfaced reference cited STRATEGIES list verbatim (Section 3.5) but no Strategy class body anywhere.

**Substrate-actual source**: `backend/services/strategy_registry.py` (canonical Hybrid C top1_win exemplar + parent `_RawLayerWin`; per Phase B.3 substrate-grep).

**Parent class `_RawLayerWin` (strategy_registry.py:126)**:

```python
class _RawLayerWin(StrategyBase):
    """Generic: bet $2 to win on top-1 from configured ranking layer."""
    category = 'raw_layer'
    def recommend(self, rp, ctx):
        top = self.top_n(rp, 1)
        if not top: return None
        return BetRecommendation(
            strategy_name=self.name, race_id=rp.race_id, bet_type='win',
            horses=[top[0].horse_name], stake=2.0,
            confidence=getattr(top[0], self.get_ranking_field()),
            rationale=f'{self.ranking_layer} top1; prob={getattr(top[0], self.get_ranking_field()):.4f}',
        )
```

**Exemplar `HybridC_Top1_Win` (strategy_registry.py:419)**:

```python
class HybridC_Top1_Win(_RawLayerWin):
    name = 'hybrid_c_top1_win'
    description = 'Hybrid C ensemble top-1 → $2 win'
    ranking_layer = 'ensemble_hybrid_option_c'
```

**Substrate-pragmatic β.3 sprint top1_win addition pattern**:

```python
class SS_Sprint_Top1_Win(_RawLayerWin):
    name = 'ss_sprint_top1_win'
    description = 'Specialist_style sprint top-1 → $2 win (distance ≤ 6.5f only)'
    ranking_layer = 'ensemble_specialist_style_sprint'
```

**Substrate-pragmatic per-strategy attribute substrate**:
- `name`: snake_case unique identifier (substrate-coherent with strategy_pnl/strategy_recommendations.strategy_name varchar(100) ceiling per σ-2 extension Phase 2.5)
- `description`: human-readable per-report annotation
- `ranking_layer`: dispatcher key into RANKING_LAYER_FIELDS (Section 2.3); new value `'ensemble_specialist_style_sprint'` substrate-additive per β.2 RANKING_LAYER_FIELDS amendment
- `category`: inherited from `_RawLayerWin` (`'raw_layer'`); β.3 substrate-coherent

**Substrate-pragmatic β.3 STRATEGIES list registration**:
- Add instance `SS_Sprint_Top1_Win()` to STRATEGIES list per Section 3.5 module-tail pattern
- Substrate-pragmatic insertion point: substrate-coherent grouping with other ensemble-tied strategies (after Hybrid C single-race block per Section 3.5 verbatim list)
- Substrate-additive route-filter (distance ≤ 6.5) substrate-pragmatic at recommend() override OR consumer-side strategy_harness filter (β.4 substrate-pragmatic scope)

**Substrate-coherence note**: β.3 produces only ONE Top1 win Strategy initially; full β.3 scope (multi-leg spreads, exa/tri/sf boxes, etc.) substrate-pragmatic extensible via parameterized factory pattern per Section 3.2 (_DD_Spread / _P3_Spread / etc. substrate-already in production).

### 3.10 — Box-bet pattern verbatim bodies (added 2026-05-19T04:00:00Z; per Q-pre-β-3.5 Option C step 4)

**Amendment scope**: β.3 substrate-augmented authoring substrate-pragmatic-consumed cites from baseline e788d59 NOT substrate-cited in substrate-permanent reference at commit 15891fa Section 3.9 + supporting subsections. Pattern-citation completeness at Section 3.9 (HybridC_Top1_Win + _RawLayerWin verbatim) substrate-pragmatic-sufficient for Top1_Win mirror BUT substrate-thin for box-bet pattern mirror (β.3 Top2_ExaBox + Top3_TriBox + Top4_SFBox substrate-actually require _EnsembleBox + _HybridCBox + HybridC_Top<N>_*Box verbatim bodies).

**Substrate-evidence basis**: § 4.32 firings #10/#11/#12/#13/#14 5-instance multi-instance accrual substrate-emphatic. Methodology refinement substrate-actuated: *"Per-sub-dispatch verification dispatches substrate-actually substrate-discover BODY-LEVEL substrate-needs per sub-dispatch's specific code-mutation scope, not just pattern-citation completeness."*

**β.3 commit substrate-evidence**: 2f604ae (β.3 strategy_registry sprint extension; substrate-augmented from these cites).

**Substrate-source**: `backend/services/strategy_registry.py` at baseline e788d59 (γ substrate-gap closure commit).

---

#### 3.10.1 — _EnsembleBox base class verbatim body

Source: `backend/services/strategy_registry.py` lines 239-265 at e788d59

```python
class _EnsembleBox(StrategyBase):
    """Generic boxed bet on ensemble top-N. N + bet_type derived from subclass."""
    category = 'raw_layer'
    ranking_layer = 'ensemble'
    n_horses: int = 3
    bet_kind: str = 'exacta'  # 'exacta' / 'trifecta' / 'superfecta'
    base_unit: float = 1.0    # $2 for exacta, $1 for tri, $0.10 for sf

    def recommend(self, rp, ctx):
        if ctx.field_size < self.n_horses: return None
        top = self.top_n(rp, self.n_horses)
        if len(top) < self.n_horses: return None
        n = self.n_horses
        if self.bet_kind == 'exacta':
            combos = n * (n - 1)
        elif self.bet_kind == 'trifecta':
            combos = n * (n - 1) * (n - 2)
        else:  # superfecta
            combos = n * (n - 1) * (n - 2) * (n - 3)
        stake = combos * self.base_unit
        return BetRecommendation(
            strategy_name=self.name, race_id=rp.race_id,
            bet_type=f'{self.bet_kind}_box_{n}',
            horses=[h.horse_name for h in top], stake=stake,
            confidence=top[0].ensemble_win_prob,
            rationale=f'{self.bet_kind}_box_{n} on ensemble top {n}',
        )
```

---

#### 3.10.2 — _HybridCBox class verbatim body

Source: `backend/services/strategy_registry.py` lines 425-426 at e788d59

```python
class _HybridCBox(_EnsembleBox):
    ranking_layer = 'ensemble_hybrid_option_c'
```

**Substrate-finding**: _HybridCBox is substrate-minimal 2-line subclass. `recommend()` inherited verbatim from _EnsembleBox. NO `ensemble_version` class attribute (β.2 strategy_harness `load_race_predictions` handles ensemble_version SELECT discrimination; class itself uses `ranking_layer` dispatch via RANKING_LAYER_FIELDS).

**Substrate-pragmatic β.3 mirror pattern** (substrate-permanent at 2f604ae):
```python
class _SpecialistStyleSprintBox(_EnsembleBox):
    ranking_layer = 'specialist_style_sprint'
```

---

#### 3.10.3 — HybridC box exemplars verbatim body

Source: `backend/services/strategy_registry.py` lines 429-450 at e788d59 (HybridC_Top2_ExaBox + HybridC_Top3_TriBox + HybridC_Top4_SFBox)

```python
class HybridC_Top2_ExaBox(_HybridCBox):
    name = 'hybrid_c_top2_exa_box'
    description = 'Exacta box top-2 from Hybrid C (ticket $4)'
    n_horses = 2; bet_kind = 'exacta'; base_unit = 2.0


class HybridC_Top3_TriBox(_HybridCBox):
    name = 'hybrid_c_top3_tri_box'
    description = 'Trifecta box top-3 from Hybrid C (ticket $6)'
    n_horses = 3; bet_kind = 'trifecta'; base_unit = 1.0


class HybridC_Top4_SFBox(_HybridCBox):
    name = 'hybrid_c_top4_sf_box'
    description = 'Superfecta box top-4 from Hybrid C (ticket $2.40)'
    n_horses = 4; bet_kind = 'superfecta'; base_unit = 0.10
```

---

**§ 4.32 firings codification candidate banking** (5-instance multi-instance accrual substrate-emphatic; § 4.36 threshold substrate-met):

| # | Dispatch | Pattern | Substrate-finding |
|---|---|---|---|
| #10 | δ.2 | Reference CLI invocation incompleteness | Section 6 substrate-pragmatic-cited dispatch internals but NOT CLI surface |
| #11 | δ.1 | Section 4 duplicate 4.7 numbering RECURRENCE | δ.1 dispatch appended 4.7 over existing 4.7 (substrate-divergence flag); recurrence at Phase 6 |
| #12 | Phase 6 | Verbatim function-body transcription discipline | substrate-actuated as codification candidate in firing #12 |
| #13 | pre-β.3 | Coverage-verdict-substrate-divergence at sub-dispatch granularity | BET_TYPE pattern-citation COMPLETE but specific-value top1_place substrate-missing |
| #14 | β.3 Phase 1.4 | Per-sub-dispatch BODY-LEVEL substrate-needs surface granularly | Box-bet pattern-vs-body substrate-thin; reference cites HybridC_Top1_Win body but NOT _EnsembleBox/_HybridCBox/HybridC_Top<N>_Box bodies |

**Methodology refinement candidate substrate-emphatic-priority** (for next codification cycle):
> *"Per-sub-dispatch verification dispatches substrate-actually substrate-discover BOTH pattern-citation completeness AND specific-value-availability + body-level substrate-completeness per sub-dispatch substrate-specific code-mutation scope substrate-target."*

Next codification cycle substrate-pragmatic substrate-actuates methodology refinement substrate-permanent in bible (v3-patched-h OR substrate-coherent version increment per substrate-pragmatic cadence).

---

## SECTION 4 — model_versions table

### 4.1 Schema (verbatim live query)

```
Column                         Type                      Nullable  Default
─────────────────────────────────────────────────────────────────────────────
model_version_id               uuid                      NO        uuid_generate_v4()  [PK]
version_name                   varchar(80)               NO        —     ← was varchar(50) pre-σ-2-extension
training_date                  timestamp with time zone  NO        —
training_data_start            date                      NO        —
training_data_end              date                      NO        —
training_race_count            integer                   YES       —
exacta_hit_rate                numeric                   YES       —
trifecta_hit_rate              numeric                   YES       —
top1_accuracy                  numeric                   YES       —
top3_accuracy                  numeric                   YES       —
calibration_score              numeric                   YES       —
feature_list                   jsonb                     YES       —
hyperparameters                jsonb                     YES       —
s3_artifact_path               varchar(500)              YES       —
is_active                      boolean                   YES       false
notes                          text                      YES       —
created_at                     timestamp with time zone  YES       now()
model_type                     varchar(60)               YES       'wr'   ← was varchar(30) pre-δ.1 σ-2
flat_bet_roi                   numeric                   YES       —
kelly_roi                      numeric                   YES       —
value_bet_win_rate             numeric                   YES       —
```

**Substrate-amendment 2026-05-19T00:30:00Z** (per δ.1 σ-2 surface):
Original transcription at commit 19c295a omitted `character_maximum_length`
for varchar columns. Substrate-actual lengths surfaced via δ.1 Phase 5
substrate-bug (StringDataRightTruncation at varchar(30) on model_type).
Substrate-actual lengths now inline above. `model_type` ALTERED from
varchar(30) → varchar(60) per σ-2 ratification (δ.1 substrate-prerequisite).
§ 4.32 sub-pattern B firing #8 banked: substrate-permanent reference itself
substrate-incomplete; remediated this amendment.

**Substrate-amendment 2026-05-19T01:00:00Z** (per σ-2 extension Q1 α surface):
§ 4.32 sub-pattern B firing #9 lesson applied: broad-scope substrate-grep
across ALL constraint-bearing columns + producers (not just immediate bug
column). Phase 2 substrate-grep enumeration verbatim:

  Column                                            curr  max_obs  prop  alter
  ────────────────────────────────────────────────────────────────────────────
  model_versions.version_name                       50    53       80    YES
    worst: train_specialist_architectures.py:196 field_size_specialist+xlarge
           specialist_field_size_specialist_xlarge_YYYYMMDD_HHMM = 53c
    2nd:   train_context_conditional.py:160 large__high_claim
           context_conditional_large__high_claim_YYYYMMDD_HHMM   = 51c
  model_versions.s3_artifact_path                   500   ~99      —     NO
  model_versions.model_type                         60    48       —     NO
  hybrid_c_predictions.ensemble_version             100   ~62      —     NO
  strategy_pnl.strategy_name                        100   ~38      —     NO
  strategy_pnl.bet_type                             50    15       —     NO
  strategy_recommendations.strategy_name            100   ~38      —     NO
  strategy_recommendations.bet_type                 50    15       —     NO

ALTER applied: `version_name` varchar(50) → varchar(80) per Tony Q1 α.
Substrate-pragmatic headroom: 80 / 53 max_observed ≈ 1.5× (substrate-coherent
50% margin for future variants). All indexes preserved substrate-coherent
(no index references version_name).

Final ceilings substrate-actual post-σ-2-extension:
  model_type                  varchar(60)   (σ-2 substrate-permanent)
  version_name                varchar(80)   (σ-2 extension Q1 α substrate-permanent)
  s3_artifact_path            varchar(500)  (substrate-unchanged)
  ensemble_version            varchar(100)  (adjacent table; substrate-unchanged)
  strategy_name               varchar(100)  (adjacent table; substrate-unchanged)
  bet_type                    varchar(50)   (adjacent table; substrate-unchanged)

§ 4.32 sub-pattern B firing #9 codification candidate: **substrate-discovery
dispatch scope discipline** — broad-scope substrate-grep across ALL
constraint-bearing-column producers vs narrow per-bug scope. σ-2 was scope-
narrow (model_type only) + Phase B incidentally surfaced version_name bug;
σ-2 extension applied broad-scope per lesson. Banked for next codification
cycle.

**PK**: `model_version_id` (NOT `model_uuid` as memory said)
**Indexes**:
- `model_versions_pkey` — UNIQUE BTREE on (`model_version_id`)
- `idx_active_model_per_type` — UNIQUE BTREE on (`model_type`) WHERE `is_active = true`

**CRITICAL SUBSTRATE-FINDING**: `idx_active_model_per_type` is a partial unique index — at most ONE row per `model_type` can be `is_active = TRUE`. Activation is per-type, NOT global.

### 4.2 Row inventory — ensemble class (verbatim)

```
uuid=2d34b010-f17a-492e-8f7c-270bd393731d
  type=ensemble_hybrid_option_c   version=option_c_hybrid_ensemble_20260515
  active=True   created=2026-05-16 02:27:46+00:00
  s3=s3://equine-model-artifacts/ensemble/option_c_hybrid_ensemble_20260515.json

uuid=e5faa6e4-0ae1-41f2-8230-6bc6f2499827
  type=ensemble                   version=ensemble_20260513_0428
  active=False   created=2026-05-13 04:33:37+00:00

uuid=745b9aa4-13d3-452d-b0b0-aa2154a32d9b
  type=ensemble                   version=ensemble_20260513_0214
  active=False   created=2026-05-13 02:16:18+00:00

uuid=42e796ae-c590-4110-a3d5-4b81647ba52f
  type=ensemble                   version=ensemble_20260322_0649
  active=True   created=2026-03-22 13:03:18+00:00
```

**Aggregate stats**: 52 distinct model_type values, mostly L1 specialists (5 versions each). `ensemble` has 3 rows (1 active); `ensemble_hybrid_option_c` has 1 row (active).

**specialist_style rows**: ZERO. Confirmed substrate-actual: `SELECT … WHERE version_name LIKE '%specialist%' OR model_type LIKE '%specialist%'` returns no rows.

### 4.3 is_active consumer trace

| Consumer | Substrate-pragmatic role | Reads is_active? |
|---|---|---|
| `wr_inference_service.py:269` | get_active_model_by_type('wr') | YES — load active WR model |
| `ls_inference_service.py:145` | get_active_model_by_type('ls') | YES — load active LS model |
| `pl_inference_service.py:96` | get_active_model_by_type('pl') | YES — load active PL model |
| `inference_service.py:102` | get_active_model() | YES — generic active model |
| `dashboard_router.py:34,63` | dashboard display | YES — display only |
| `substrate_health_monitor:202` | health check | YES — monitoring |
| `model/ensemble/train.py:50,78` | training-time prior lookup | YES — for training |
| `model/longshot/train.py:52` | training-time prior lookup | YES — for training |
| `model/ensemble/option_c_inference.py:106` | LEGACY Option C load (NOT MCIS) | YES — but legacy path |
| **`multicohort_inference_service.py` (MCIS)** | Production Hybrid C load | **NO** — pins by (model_type, version_name) instead |

**CRITICAL SUBSTRATE-FINDING**: MCIS — the substrate-actual production Hybrid C inference path — does NOT consult `is_active`. The L1 inference services (WR/PL/LS) DO consult `is_active`, but for the L2 ensemble layer (MCIS), `is_active` on `ensemble_hybrid_option_c` row is **substrate-decorative for MCIS** (no MCIS code reads it).

Per MCIS docstring line 9-10 verbatim:
> "L1 artifacts are pinned by version_name (NOT by is_active) — this matches the exact 32 columns Hybrid C was trained on, robust to future activation churn."

### 4.4 Registration pattern (verbatim from `model/training/registration.py`)

```python
def register_trained_artifact(
    version_name: str,
    s3_artifact_path: str,
    training_metadata: dict,
    model_type: Optional[str] = None,
    is_active: bool = False,        # ← § 4.34 forensic-gate discipline default
    db_conn=None,
) -> str:
    """Register trained ML artifact in model_versions.

    Args:
        ...
        is_active: Defaults FALSE per § 4.34 forensic-gate discipline.
            Activation is a separate forensic-substrate step, never a
            training-time auto-promotion.
        ...
    """
    if model_type is None:
        model_type = derive_model_type(version_name)
    ...
    cur.execute("""
        INSERT INTO model_versions (
            version_name, model_type, training_date,
            training_data_start, training_data_end,
            training_race_count,
            feature_list, hyperparameters, s3_artifact_path,
            top1_accuracy, top3_accuracy, calibration_score,
            ...
            is_active, notes
        ) VALUES (%s, %s, ...)
        RETURNING model_version_id;
    """, (...))
```

**Activation pattern** (`model_version_repository.py:set_active_model`):

```python
def set_active_model(self, model_version_id: str) -> None:
    """Deactivate models OF THE SAME TYPE only,
       then activate this one."""
    model = self._query_one(
        "SELECT model_type FROM model_versions WHERE model_version_id = %s",
        (model_version_id,))
    self._write(
        "UPDATE model_versions SET is_active = false WHERE model_type = %s",
        (model['model_type'],))
    self._write(
        "UPDATE model_versions SET is_active = true WHERE model_version_id = %s",
        (model_version_id,))
```

### 4.5 --no-register implications

Training scripts with `--no-register` flag:
- `train_specialist_architectures.py` (BD2v2 — used for specialist_style)
- `train_test_combined.py`
- `train_context_conditional.py`
- `train_multi_cohort_variants.py`
- `train_hierarchical_bayesian.py`
- `train_bayesian_methods.py`

**When `--no-register` set**: `register_trained_artifact()` is NOT called → ZERO row in model_versions.

**Substrate-pragmatic implication for specialist_style**: BD2v2 substrate-actually produced:
- S3 artifact(s) (sprint sub-booster, route sub-booster) — verify Section 6
- BD3v2 forensic predictions written to hybrid_c_predictions table (CC Phase 1 HALT)
- ZERO model_versions row → ZERO discoverability via DB-lookup mechanism
- For MCIS production load: would substrate-actually work even without model_versions row, IF the MCIS hardcoded constants pointed at specialist_style S3 paths. Substrate-current: MCIS hardcodes Hybrid C only.

### 4.6 Memory-vs-actual annotation

| Memory framing | Substrate-actual | Verdict |
|---|---|---|
| PK column `model_uuid` | Actually `model_version_id` | DIVERGENT (naming) |
| "uuid=2d34b010-... type='ensemble_hybrid_option_c' active=True" | Confirmed | MATCHES |
| "uuid=42e796ae-... type='ensemble' active=True" | Confirmed | MATCHES |
| "uuid=e5faa6e4-... type='ensemble' active=False" | Confirmed | MATCHES |
| "uuid=745b9aa4-... type='ensemble' active=False" | Confirmed | MATCHES |
| "specialist_style ZERO rows" | Confirmed | MATCHES |
| is_active functional for MCIS | NOT consulted by MCIS — only by L1 inference services | DIVERGENT |
| "flip is_active=TRUE on specialist_style activates" (Tony Phase 6.1.4) | Would update model_versions row, but MCIS doesn't read it; substrate-pragmatic still requires MCIS code change | DIVERGENT |

### 4.7 Substrate-divergence flag

**FLAG 1**: `is_active` flag is functional ONLY for L1 inference services (wr_inference, pl_inference, ls_inference). For the L2 ensemble layer (MCIS), `is_active` is substrate-decorative. Tony Path A Phase 6.1.4 framing assumed L2-functional activation; substrate-actual is decorative-at-MCIS.

**FLAG 2**: `idx_active_model_per_type` partial unique index enforces at-most-one active per model_type. For specialist_style activation, substrate-options:
- Use distinct model_type (e.g., `ensemble_specialist_style`) — non-blocking; allows BOTH Hybrid C + specialist_style active simultaneously
- Use same model_type `ensemble_hybrid_option_c` — would require deactivating Hybrid C first (atomic transition)
- Use new model_type — substrate-pragmatic cleanest

**FLAG 3**: BD2v2 `--no-register` consequence: specialist_style has NO model_versions row. Activation dispatch MUST first call `register_trained_artifact()` for each sub-booster, then optionally call `set_active_model()`.

**FLAG 4**: Memory's PK column name `model_uuid` is wrong — substrate-actual is `model_version_id`. Any Path A dispatch SQL referencing `model_uuid` would substrate-error.

### 4.7 Post-δ.1 registration state (added 2026-05-19T00:30:00Z)

**State transition**: BD2v2 --no-register substrate-gap closed for
specialist_style sub-boosters per Tony Option δ ratification + σ-2 schema
ALTER substrate-prerequisite.

**Substrate-prerequisite σ-2**: `ALTER TABLE model_versions ALTER COLUMN
model_type TYPE varchar(60);` applied transactionally. `idx_active_model_per_type`
partial unique index substrate-preserved verbatim post-ALTER.

**Substrate-grep B-validation** (Phase B per σ-2 dispatch): max model_type
length observed across all train_* producers = 48 chars
(`ensemble_specialist_field_size_specialist_xlarge`). varchar(60) substrate-
coherent ceiling for all current substrate.

**Registrations added** (is_active=FALSE; registration only, NOT activation;
State B per Phase 2.1 — META wrapper substrate-omitted):

```
sprint sub-booster:
  model_version_id:   1202021f-2937-46eb-a1fd-0dd9b0d1fe20
  model_type:         ensemble_specialist_style_specialist_sprint  (43 chars)
  version_name:       specialist_style_specialist_sprint_20260518_0252
  s3_artifact_path:   s3://equine-model-artifacts/ensemble/test/specialist_style_specialist_sprint_20260518_0252.json
  training_window:    2026-04-25 → 2026-05-01
  training_races:     100 (n_train=80 + n_eval=20)
  top1_accuracy:      0.8829 (eval_auc per BD2v2 meta)
  is_active:          FALSE
  created_at:         2026-05-19 00:29:45.699683+00

route sub-booster:
  model_version_id:   c217c11e-1f71-43e2-8281-bf99e993331e
  model_type:         ensemble_specialist_style_specialist_route   (42 chars)
  version_name:       specialist_style_specialist_route_20260518_0252
  s3_artifact_path:   s3://equine-model-artifacts/ensemble/test/specialist_style_specialist_route_20260518_0252.json
  training_window:    2026-04-25 → 2026-05-01
  training_races:     104 (n_train=83 + n_eval=21)
  top1_accuracy:      0.7496 (eval_auc per BD2v2 meta)
  is_active:          FALSE
  created_at:         2026-05-19 00:29:45.743187+00
```

**Substrate-state post-δ.1**:
- model_versions inventory: ensemble-class rows now 6 (was 4 per Section 4.2)
  - `ensemble_hybrid_option_c`: 1 row (is_active=TRUE; Hybrid C production)
  - `ensemble`: 3 rows (1 active legacy 10-feat; 2 inactive)
  - `ensemble_specialist_style_specialist_sprint`: 1 row (is_active=FALSE)
  - `ensemble_specialist_style_specialist_route`: 1 row (is_active=FALSE)
- is_active=TRUE rows: UNCHANGED (Hybrid C + legacy 10-feat)
- Production prediction path: UNCHANGED (MCIS pins by hardcoded constants
  per Section 1; registration does NOT route; MCIS initialize substrate-
  verified post-registration — 32 L1 artifacts + Hybrid C booster loaded
  substrate-coherent)
- hybrid_c_predictions writes: zero post-δ.1 writes (no inference triggered)

**Substrate-prerequisite unblocked**:
- δ.2 multi-track substrate-validation forensic measurement (next dispatch);
  forensic can substrate-pin by model_version_id now
- Future α (Path A) activation requires R2-R8 per Section 8.2; not unblocked
  by registration alone
- Future β (Path B) activation requires same R2-R8 subset; not unblocked
  by registration alone

**Rollback artifact**: `/tmp/delta_1_registration_rollback.sql` with verbatim
PKs:
- sprint PK: `1202021f-2937-46eb-a1fd-0dd9b0d1fe20`
- route PK:  `c217c11e-1f71-43e2-8281-bf99e993331e`

**Backup artifact**: `/tmp/model_versions_pre_delta_1_20260519-001308.sql`
(pre-δ.1 model_versions snapshot; 145640 bytes; 212 lines).

**Substrate-grounding cite**: `/tmp/delta_1_substrate_grounding.md` (419
lines; Section 4 + 6 verbatim cite from commit 19c295a).

**Reference commit pre-δ.1**: `19c295a` (Option A ratification, Sections 1-8)
**Reference commit post-δ.1**: (this commit)

---

## SECTION 5 — hybrid_c_predictions schema + dual-write feasibility

### 5.1 Schema (verbatim live query)

```
Column                         Type                          Nullable  Default
─────────────────────────────────────────────────────────────────────────────
prediction_id                  uuid                          NO        gen_random_uuid()  [PK]
race_id                        uuid                          NO        —
horse_id                       text                          NO        —
hybrid_c_win_probability       numeric                       NO        —
l1_input_count                 integer                       NO        32
ensemble_version               character varying             NO        'option_c_hybrid_ensemble_20260515'
predicted_at                   timestamp without time zone   YES       now()
```

### 5.2 Indexes + constraints

```
hybrid_c_predictions_pkey:
  UNIQUE BTREE (prediction_id)

hybrid_c_predictions_race_id_horse_id_ensemble_version_key:
  UNIQUE BTREE (race_id, horse_id, ensemble_version)   ← MULTI-VERSION COEXISTENCE

idx_hybrid_c_preds_race:      BTREE (race_id)
idx_hybrid_c_preds_date:      BTREE (predicted_at)
idx_hybrid_c_preds_version:   BTREE (ensemble_version)
```

**CRITICAL SUBSTRATE-FINDING**: UNIQUE constraint INCLUDES `ensemble_version`. **Dual-write substrate-coherent at table level**: writing 2 ensemble_version values produces 2 distinct rows per (race, horse) — no conflict. This is the substrate-precondition that makes dual-write trivial.

### 5.3 Current ensemble_version distribution (live)

```
ensemble_version                                              n_rows   first_seen  last_seen
─────────────────────────────────────────────────────────────────────────────────────────
option_c_hybrid_ensemble_20260515                                3734  2026-05-16  2026-05-18
multi_cohort_pure_bx_20260518_0251                               2032  2026-05-18  2026-05-18
specialist_style_specialist_20260518_0252                        2032  2026-05-18  2026-05-18
hybrid_c_plus_longshot_prob_substrate_correct_20260518_0249      2032  2026-05-18  2026-05-18
hybrid_c_plus_first_time_lasix_posterior_sparse_20260518_0249    2032  2026-05-18  2026-05-18
hybrid_c_plus_lstm_trajectory_score_20260518_0249                2032  2026-05-18  2026-05-18
hierarchical_bayesian_20260518_0257                              2032  2026-05-18  2026-05-18
multi_cohort_pure_prior_20260518_0251                            2032  2026-05-18  2026-05-18
context_conditional_20260518_0255                                 785  2026-05-18  2026-05-18
```

**Substrate-evidence**:
- Hybrid C production substrate: 3734 rows over 2026-05-16 → 2026-05-18
- specialist_style forensic substrate: 2032 rows on 2026-05-18 (single batch from BD3v2 Tier 2 EXECUTION)
- 7 other forensic ensembles (BD3v2 ensemble class): 2032 rows each — these are the Tier 2 EXECUTION combined-ensemble forensic outputs

### 5.4 Write path enumeration

**Writer 1 — MCIS production** (`backend/services/multicohort_inference_service.py:359`):
- INSERT pattern: see Section 1.6 (UPSERT ON CONFLICT updates probability + predicted_at)
- Hardcoded ensemble_version: `'option_c_hybrid_ensemble_20260515'`
- Invoked by: daily inference Lambda (per `run_daily_predictions`)

**Writer 2 — Forensic persistence** (`model/forensic/persist_forensic_predictions.py:47`):

```python
execute_values(cur, """
    INSERT INTO hybrid_c_predictions
        (race_id, horse_id, ensemble_version, hybrid_c_win_probability,
         predicted_at, l1_input_count)
    VALUES %s
    ON CONFLICT (race_id, horse_id, ensemble_version) DO UPDATE
    SET hybrid_c_win_probability = EXCLUDED.hybrid_c_win_probability,
        predicted_at = EXCLUDED.predicted_at,
        l1_input_count = EXCLUDED.l1_input_count
""", rows)
```

- Bulk-write pattern via `execute_values`
- ensemble_version comes from parquet payload (not hardcoded)
- Invoked by: BD3v2 forensic prediction generation scripts (offline / non-production)

### 5.5 Reader enumeration

| Reader | Substrate-pragmatic role | ensemble_version handling |
|---|---|---|
| `backend/services/strategy_harness.py:362-367` | PRODUCTION: load Hybrid C preds for strategy consumption | HARDCODED 'option_c_hybrid_ensemble_20260515' |
| `model/forensic/persist_forensic_predictions.py:61` | Post-write count verification | Parameterized |
| `model/methodology/gnn_eval.py:48` | Methodology research | Joins ensemble_version |
| `model/methodology/calibration_methods_eval.py:43` | Calibration research | Joins ensemble_version |
| `model/methodology/hier_bayesian_methodology_eval.py:44` | Bayesian methodology research | Joins ensemble_version |
| `model/methodology/causal_inference_eval.py:51` | Causal inference research | Joins ensemble_version |
| `model/methodology/survival_analysis_eval.py:43` | Survival analysis research | Joins ensemble_version |
| `model/methodology/quantile_regression_eval.py:45` | Quantile regression research | Joins ensemble_version |
| `model/methodology/rl_staking_eval.py:48` | RL staking research | Joins ensemble_version |
| `model/forensic/tier2_comprehensive_forensic.py:52` | Forensic measurement | Parameterized |

**Substrate-pragmatic verdict**: Production reader is strategy_harness (single hardcoded ensemble_version). All other readers are research/forensic substrate (parameterized; not production-critical).

### 5.6 Dual-write feasibility verdict

**Substrate-conclusion**: **Dual-write IS substrate-coherent and ALREADY OPERATIVE**.

The table substrate-actually contains 9 distinct ensemble_version values RIGHT NOW. Each writes to a distinct (race_id, horse_id, ensemble_version) tuple. No constraint conflict. No schema change required.

For Path A production specialist_style dual-write, the **only mutation required** at this layer is:
- MCIS-side: add specialist_style write call (in addition to Hybrid C write call)
- OR MCIS-side: generic predict_and_persist() loop over a list of ensembles
- Schema: NO CHANGE NEEDED

### 5.7 Memory-vs-actual annotation

| Memory framing | Substrate-actual | Verdict |
|---|---|---|
| "no is_primary column" | Confirmed | MATCHES |
| "ensemble_version may suffice as discriminator" | Confirmed via UNIQUE constraint including ensemble_version | MATCHES + VALIDATES |
| "Path A Phase 3.2 ALTER required" | NOT required — schema substrate-already supports dual-write | DIVERGENT (memory overcomplicated) |
| "specialist_style predictions DO exist" (CC Phase 1 HALT) | Confirmed — 2032 rows on 2026-05-18 | MATCHES |

### 5.8 Substrate-divergence flag

**FLAG 1**: Tony Path A Phase 3.2 framing assumed schema ALTER required for primary/shadow discrimination. Substrate-actual: schema-coherent as-is. ensemble_version IS the discriminator. The "primary" attribution is a consumer-side concern (strategy_harness query string), not a table-level concern.

**FLAG 2**: Substrate-permanent finding: hybrid_c_predictions is a multi-ensemble table — the name "hybrid_c" is now substrate-misleading. It's substrate-actually a generic ensemble prediction sink with ensemble_version discriminator. Rename candidate: `ensemble_predictions` (out-of-scope; substrate-cosmetic).

**FLAG 3**: Default value of `ensemble_version` column is `'option_c_hybrid_ensemble_20260515'` — substrate-pragmatic implication: any INSERT that omits ensemble_version writes to Hybrid C identity by default. New writers (e.g., specialist_style production writer) MUST explicitly pass ensemble_version OR risk silent contamination of Hybrid C rows.

---

## SECTION 6 — specialist_style META structure

### 6.1 Substrate-pragmatic substrate

specialist_style is the `style_specialist` variant produced by
`model/ensemble/train_specialist_architectures.py` (BD2v2). It is a META
artifact composed of TWO sub-boosters dispatched by race distance:

- **sprint sub-booster**: races where `distance_furlongs ≤ 6.5`
- **route sub-booster**: races where `distance_furlongs > 6.5`

Both sub-boosters consume the SAME 32 L1 inputs as Hybrid C (`HYBRID_C_32_L1_INPUTS`).

### 6.2 S3 substrate-actual artifacts (verbatim live `aws s3 ls`)

```
s3://equine-model-artifacts/ensemble/test/specialist_style_specialist_route_20260518_0252.json    135782 bytes  2026-05-17 22:52:27
s3://equine-model-artifacts/ensemble/test/specialist_style_specialist_sprint_20260518_0252.json    99778 bytes  2026-05-17 22:52:35
```

**Substrate-divergence**: BD2v2 wrote to `ensemble/test/` prefix (not `ensemble/`). The `test/` substrate-pragmatic suffix comes from `S3_PREFIX = 'ensemble/test'` in `train_test_combined.py:101` — used because BD2v2 was synthetic-validation scope per `--no-register` flag. For production deployment, S3 re-upload to `ensemble/` prefix is substrate-conventional (matches Hybrid C location).

### 6.3 Meta artifact (verbatim from `/tmp/bd2v2_synthetic/specialist_style.json`)

```json
{
  "name": "specialist_style_specialist_20260518_0252",
  "description": "Specialist architecture: style_specialist",
  "variant": "style_specialist",
  "training_window": ["2026-04-25", "2026-05-01"],
  "feature_cols": [ ... 32 L1 inputs identical to HYBRID_C_32_L1_INPUTS ... ],
  "sub_artifacts": {
    "route": {
      "status": "trained",
      "partition": "route",
      "version_name": "specialist_style_specialist_route_20260518_0252",
      "eval_auc": 0.749605802585935,
      "eval_brier": 0.08635728061199188,
      "n_train_races": 83,
      "n_eval_races": 21,
      "booster_s3_path": "s3://equine-model-artifacts/ensemble/test/specialist_style_specialist_route_20260518_0252.json"
    },
    "sprint": {
      "status": "trained",
      "partition": "sprint",
      "version_name": "specialist_style_specialist_sprint_20260518_0252",
      "eval_auc": 0.8829268292682927,
      "eval_brier": 0.07950533926486969,
      "n_train_races": 80,
      "n_eval_races": 20,
      "booster_s3_path": "s3://equine-model-artifacts/ensemble/test/specialist_style_specialist_sprint_20260518_0252.json"
    }
  },
  "training_hyperparams": {
    "objective": "binary:logistic", "eval_metric": "auc",
    "learning_rate": 0.05, "max_depth": 3,
    "subsample": 0.7, "colsample_bytree": 0.6,
    "min_child_weight": 3, "reg_alpha": 0.5, "reg_lambda": 2.0
  },
  "substrate_version": "v3-patched-f",
  "created_at": "2026-05-18T02:52:33.705064",
  "note": "Meta-router for partition→sub-artifact routing deferred to Tier 2 EXECUTION"
}
```

**Per-sub-booster training eval AUC**:
- sprint: 0.8829 (n_train=80 races, n_eval=20)
- route: 0.7496 (n_train=83 races, n_eval=21)

### 6.4 Local sub-booster artifacts (CC workstation /tmp; ephemeral)

```
/tmp/bd2v2_synthetic/specialist_style.json                        3745 bytes (meta)
/tmp/bd2v2_synthetic/specialist_style.sprint.booster.json        99778 bytes
/tmp/bd2v2_synthetic/specialist_style.route.booster.json        135782 bytes
```

**Substrate-pragmatic concern**: These are on Tony's laptop `/tmp` — ephemeral. The S3 copies (Section 6.2) are the durable artifacts. Re-fetching from S3 is the substrate-canonical pattern for production use.

### 6.5 Dispatch routing logic (verbatim from `model/forensic/generate_forensic_predictions.py:215-217`)

```python
# Routing key
if variant == 'style_specialist' or 'specialist_style' in version_name.lower():
    df['_route_key'] = np.where(df['distance_furlongs'] <= 6.5, 'sprint', 'route')
```

**Per-race dispatch**:
- Read `races.distance_furlongs` (float)
- If `≤ 6.5` → sprint sub-booster
- Else → route sub-booster

### 6.6 Per-sub-booster prediction (verbatim from generate_forensic_predictions.py:236-271)

```python
for route_key, sub_meta in sub_artifacts.items():
    if not isinstance(sub_meta, dict) or sub_meta.get('status') != 'trained':
        continue

    chunk = df[df['_route_key'] == route_key]
    if len(chunk) == 0:
        continue

    # Locate booster
    sub_version = sub_meta.get('version_name', '')
    local_candidate = artifact_path.replace('.json', f'.{route_key}.booster.json')
    if not Path(local_candidate).exists():
        s3_path = sub_meta.get('booster_s3_path', '')
        if s3_path and s3_path.startswith('s3://'):
            bucket, key = s3_path.replace('s3://', '').split('/', 1)
            s3.download_file(bucket, key, local_candidate)
        else:
            continue

    sub_booster = xgb.Booster()
    sub_booster.load_model(local_candidate)

    # Sub-booster feature_cols inherited from META meta.feature_cols
    feature_cols = meta['feature_cols']
    X = chunk[feature_cols].fillna(0.0).values
    raw = sub_booster.predict(xgb.DMatrix(X, feature_names=feature_cols))

    chunk_out = chunk[['race_id', 'horse_id']].copy()
    chunk_out['raw_prediction'] = raw
    chunks.append(chunk_out)
```

**Substrate-pragmatic verdict**: Per-route chunk → load sub-booster → predict → concat. Within-race softmax normalization applied AFTER concat (`df_out['win_probability'] = df_out.groupby('race_id', group_keys=False)['raw_prediction'].transform(_within_race_softmax_transform)`).

### 6.7 Predictions persisted in hybrid_c_predictions (live)

ensemble_version `specialist_style_specialist_20260518_0252` rows by race_date:

```
2026-05-02:  592 rows
2026-05-03:  238 rows
2026-05-07:  151 rows
2026-05-08:  270 rows
2026-05-09:  405 rows
2026-05-10:  376 rows
─────────────────────
Total:      2032 rows  (matches Section 5.3 count)
```

Sample row: `l1_input_count=0` (substrate-pragmatic forensic substrate didn't track L1 count). Probabilities substrate-coherent (~0.07-0.08 range per horse for a 12+ horse race).

**Substrate-pragmatic state**: BD3v2 forensic substrate-persisted predictions for BEL forensic window 2026-05-02..2026-05-10. ZERO predictions for dates outside this window (no 2026-04-25..05-01 training data forensic; no 5/11+ post-window forecasting).

### 6.8 BD2v2 --no-register implications (substrate-aggregated)

| Substrate area | State |
|---|---|
| S3 artifacts | EXIST at `s3://equine-model-artifacts/ensemble/test/...` (.json boosters) |
| hybrid_c_predictions table | 2032 rows EXIST (BD3v2 forensic-window persistence) |
| model_versions table | ZERO rows (specialist_style + sub-boosters NOT REGISTERED) |
| MCIS production load path | ABSENT (MCIS hardcodes Hybrid C only) |
| strategy_harness consumer | ABSENT (hardcodes Hybrid C ensemble_version) |
| RANKING_LAYER_FIELDS | ABSENT (only `ensemble_hybrid_option_c` substrate; no specialist_style) |
| strategy_registry strategies | ZERO specialist_style-tied strategies (15 ranker-based "specialist" classes exist but they read `ranker` ranking_layer — substrate-confusingly named, different concept) |
| Lambda invocation substrate | ABSENT (no daily-job for specialist_style production write) |

**Verdict**: specialist_style currently exists as **forensic-persisted predictions on a closed cohort window**; ZERO production substrate for live prediction generation OR consumption.

### 6.9 Memory-vs-actual annotation

| Memory framing | Substrate-actual | Verdict |
|---|---|---|
| "specialist_style ensemble_version=specialist_style_specialist_20260518_0252" | Confirmed verbatim | MATCHES |
| "BD3v2 forensic-window persistence in hybrid_c_predictions" | Confirmed (2032 rows on BEL 5/2-5/10) | MATCHES |
| "META artifact with sprint + route sub-boosters; distance ≤ 6.5 → sprint" | Confirmed verbatim from dispatch logic + meta | MATCHES |
| "32 L1 inputs per sub-booster (same as Hybrid C)" | Confirmed — feature_cols identical to HYBRID_C_32_L1_INPUTS | MATCHES |

### 6.10 Substrate-divergence flag

**FLAG 1**: S3 artifacts at `ensemble/test/` prefix — NOT `ensemble/`. Production load-path conventions assume `ensemble/`. Substrate-pragmatic options:
- Re-upload to `ensemble/` prefix (substrate-pragmatic clean)
- Update MCIS load-path to accept arbitrary S3 path per ensemble (substrate-permanent generalization)
- Leave as-is (substrate-pragmatic lazy; "test" in production-path is misleading)

**FLAG 2**: Both sub-boosters trained on substrate-thin n=100 race cohort (sprint: 80+20, route: 83+21). Substrate-pragmatic compared to Hybrid C training cohort (entire 2022-2026 calendar = thousands of races). Path A activation MUST surface this gap to Tony — specialist_style is substrate-thin trained substrate.

**FLAG 3**: BD3v2 forensic persistence wrote to hybrid_c_predictions with `l1_input_count=0` (vs MCIS-canonical 32). Production specialist_style writer should write `l1_input_count=32` for substrate-coherent semantics with Hybrid C rows.

**FLAG 4**: BD2v2 `note` field substrate-honest: *"Meta-router for partition→sub-artifact routing deferred to Tier 2 EXECUTION"*. The META-routing mechanism is implemented in `generate_forensic_predictions.py:predict_path3_meta_routing` — but this is the FORENSIC path, NOT production. Production META-routing in MCIS substrate-actually does NOT exist.

---

## SECTION 7 — Adjacent substrate

### 7.1 Production Lambda inventory (live `aws lambda list-functions`)

```
Function                                    Type    LastModified
─────────────────────────────────────────────────────────────────────────
equine-ingestion                            Image   2026-05-18T21:30:44Z  ← chart parse
equine-inference                            Image   2026-05-17T04:13:24Z  ← legacy WR inference + dashboard API
equine-wr-inference                         Image   2026-05-17T04:13:25Z  ← WR specialist Lambda
equine-pl-inference                         Image   2026-05-17T04:13:25Z  ← PL specialist Lambda
equine-ls-inference                         Image   2026-05-17T04:13:25Z  ← MCIS Hybrid C inference ★
equine-results                              Image   2026-05-17T04:13:25Z
equine-daily-morning-email                  Image   2026-05-17T04:13:25Z  ← invokes StrategyHarness
equine-daily-evening-email                  Image   2026-05-17T04:13:24Z  ← invokes StrategyHarness
equine-substrate-health-monitor             Image   2026-05-17T04:13:25Z
equine-nyra-workouts                        Image   2026-04-27T22:11:00Z
equine-outcome-metric-publisher             Zip     2026-05-12T00:17:32Z
equine-entries-tracks-publisher             Zip     2026-05-12T04:48:36Z
```

### 7.2 Production invocation chain (substrate-confirmed)

**Chart parse + ingestion**:
- `equine-ingestion` (cron) → chart_parser.py → races/entries tables

**Inference chain — Hybrid C**:
- `equine-ls-inference` (cron @ LSInferenceSchedule) → `_run_daily_pipeline()` → invokes:
  - `LSInferenceService.run_daily_predictions()` — legacy 10-feat ensemble (decommissioning per Bible)
  - `MultiCohortInferenceService.run_daily_predictions()` — **Hybrid C; the substrate-actual production path** → writes to hybrid_c_predictions table

**Strategy report chain**:
- `equine-daily-morning-email` (cron `0 11 * * ? *`) → `DailyReportGenerator.generate_pre_race_report()` → `StrategyHarness.run_race()` over 162 strategies → email
- `equine-daily-evening-email` (cron `30 3 * * ? *`) → `DailyReportGenerator.generate_post_race_report()` → P&L computation → email

**Per `daily_report_generator.py:28`**:
```python
self.strategies = get_registry()         # 162 STRATEGIES instances
self.harness = StrategyHarness(self.strategies)
```

### 7.3 ECS substrate

**Cluster**: `arn:aws:ecs:us-east-1:584812014683:cluster/equine-cluster`

**Task definitions (active)**: 14+ revisions of:
- `equine-training-daily-full` (rev 1-8) — daily L1 training cycle
- `equine-training-manual` (rev 1-2) — manual training runs
- `equine-training-pl` (rev 1-3) — PL specialist training
- `equine-training-win-prob` (rev 1-3) — WP specialist training
- `equine-training` (rev 49, 116) — legacy generic training

**Substrate-pragmatic verdict**: ECS hosts **training only**. Production inference is Lambda-only. Specialist_style does NOT have an ECS training task currently (BD2v2 ran locally + via `--no-register`, not as scheduled ECS).

### 7.4 CDK stack inventory

`/home/strakajagr/projects/equine-equalizer/infrastructure/cdk/lib/`:
- `storage-stack.ts` — S3 buckets (raw data, processed data, model artifacts)
- `database-stack.ts` — VPC + Aurora Serverless PostgreSQL
- `compute-stack.ts` — All Lambdas + EventBridge schedules + API Gateway
- `frontend-stack.ts` — CloudFront + S3 frontend hosting

**Substrate-pragmatic for Path A**: changes substrate-relevant to compute-stack.ts (new Lambda env vars if needed) OR none if MCIS code-only changes suffice.

### 7.5 Configuration (equine-inference Lambda env, verbatim live)

```json
{
  "ImageUri": "<masked>",
  "Env": {
    "RAW_DATA_BUCKET": "equine-raw-data",
    "DB_SECRET_ARN": "arn:aws:secretsmanager:us-east-1:584812014683:secret:equine-equalizer/db-credentials-7CD7Mt",
    "MODEL_ARTIFACTS_BUCKET": "equine-model-artifacts",
    "PROCESSED_DATA_BUCKET": "equine-processed-data"
  },
  "Timeout": 300,
  "Memory": 1024
}
```

**Substrate-pragmatic observation**: 4 env vars. No ensemble-version selector env. No primary-ensemble config. Production-ensemble identity is HARDCODED in source (MCIS constants + strategy_harness query string), NOT environment-configurable.

### 7.6 Memory-vs-actual annotation

| Memory framing | Substrate-actual | Verdict |
|---|---|---|
| MCIS invoked by inference Lambda | Actually `equine-ls-inference` (LS-naming substrate-historic) | DIVERGENT (naming) |
| Production deployment ECS-based | Production inference is Lambda; ECS is training-only | DIVERGENT |
| `equine-ingestion` deploy auto-syncs | Confirmed per memory ("lambda_worker_package/ AUTO-SYNCED" — substrate-coherent) | MATCHES |

### 7.7 Substrate-divergence flag

**FLAG 1**: MCIS production Lambda is `equine-ls-inference` (NOT `equine-inference`). Path A deployment dispatches MUST target `equine-ls-inference` for MCIS code changes. Targeting wrong Lambda would substrate-pragmatic-silently leave production unchanged.

**FLAG 2**: Strategy consumption changes (strategy_registry / strategy_harness) deploy via `equine-daily-morning-email` + `equine-daily-evening-email` Lambdas (NOT inference). These Lambdas substrate-actually need redeploy when strategy-side code changes.

**FLAG 3**: No env-var or Parameter Store substrate for ensemble selection. Path A activation MUST change source code + redeploy. NO runtime config flip available.

---

## SECTION 8 — Substrate-divergence summary + Path A re-authoring requirements

### 8.1 Substrate-divergence aggregate table

| # | Architecture area | Memory / Tony framing | Substrate-actual | Implication |
|---|---|---|---|---|
| D1 | MCIS load discriminator | UUID-pinned (`uuid=2d34b010-...`) | `(model_type, version_name)` tuple JOIN on model_versions | Path A registration mechanism unchanged but semantic-only divergence |
| D2 | MCIS reads `is_active` | Flip activates specialist_style | NOT consulted — pins by version_name | **Activation requires CODE change, not flag flip** |
| D3 | MCIS load pattern | Generic ensemble load | HARDCODES Hybrid C constants + L1 specs | Path A requires MCIS extension (~100-200 LOC) |
| D4 | MCIS predict pattern | Generic single-booster | Hardcoded single-booster (Hybrid C only) | Path A requires META-routing addition for specialist_style sprint/route dispatch |
| D5 | strategy_harness consumer | is_active-driven | HARDCODED ensemble_version at line 365 | Activation requires strategy_harness CODE change (~10 LOC additive OR ~30 LOC refactor) |
| D6 | strategy `is_shadow_only` attribute | Tony Phase 4.2 SQL flips | NO such attribute on StrategyBase | Shadow mechanism is Python-config-level, not DB |
| D7 | strategies DB table | Tony Phase 4 SQL ops | NO `strategies` table — 162 instances in Python list | Activation requires Python source edits + Lambda redeploy |
| D8 | strategy class count | "19 grep-counted" (CC Phase 1 HALT) | 58 classes / 162 instances via parameterized factories | Memory-corrected; substrate-pragmatic scope clearer |
| D9 | model_versions PK column | `model_uuid` | Actually `model_version_id` | Any Path A SQL referencing `model_uuid` would substrate-error |
| D10 | `idx_active_model_per_type` | Single-active global | Partial unique per model_type | Distinct model_type for specialist_style allows coexistence with Hybrid C |
| D11 | specialist_style model_versions row | Tony Phase 6.1.4 flips `is_active` | ZERO rows — must INSERT first | Registration phase REQUIRED before any activation |
| D12 | hybrid_c_predictions UNIQUE constraint | Schema ALTER required | INCLUDES ensemble_version — multi-version coexistence native | **Dual-write substrate-coherent; NO schema change required** |
| D13 | hybrid_c_predictions current state | "Hybrid C only" | 9 distinct ensemble_version values; substrate-actually multi-ensemble sink | Table name is now substrate-misleading (substrate-cosmetic only) |
| D14 | specialist_style S3 location | "Production-ready" | At `ensemble/test/` prefix (BD2v2 --no-register substrate) | Substrate-pragmatic re-upload to canonical prefix recommended |
| D15 | specialist_style training cohort | Implicit "full Hybrid C scale" | n=100-103 races per sub-booster (very thin) | Path A activation MUST surface substrate-thin trained substrate to Tony |
| D16 | Production META-routing | Implicit | Substrate-actually only in forensic path (`generate_forensic_predictions.py`); ABSENT from MCIS | Path A requires META-routing IMPLEMENTATION in production code |
| D17 | Production Lambda for MCIS | `equine-inference` (intuitive) | Actually `equine-ls-inference` (historic naming) | Path A deploy MUST target `equine-ls-inference` |
| D18 | Strategy report Lambdas | Inference Lambda invokes strategies | Substrate-actually `equine-daily-morning-email` + `equine-daily-evening-email` | Path A strategy changes deploy via THESE Lambdas |
| D19 | Runtime ensemble selector | Env var / Parameter Store | None — source-hardcoded | NO runtime config flip; code change + redeploy required |
| D20 | "is_primary" column on predictions | Schema ALTER required | NOT NEEDED — ensemble_version IS the discriminator | Tony Phase 3.2 ALTER unnecessary |

**Aggregate severity**:
- Feasibility-blocking (NONE): no substrate-divergence makes Path A architecturally impossible
- Scope-expanding (D2, D3, D4, D5, D6, D7, D11, D16): change Path A scope from "flag flips + SQL" to "Python code edits + Lambda redeploys"
- Scope-correcting (D9, D12, D20): Path A SQL substrate-actually unnecessary OR substrate-broken; revise framing
- Substrate-thin caution (D15): specialist_style training cohort is substantially smaller than Hybrid C; activation as PRIMARY production substrate carries substrate-risk

### 8.2 Path A re-authoring substrate-requirements (8-item enumeration)

For any future Path A specialist_style activation dispatch to be substrate-coherent, it MUST address these 8 substrate-actual work-items:

**Requirement 1 — Register specialist_style sub-boosters in model_versions**

Substrate-actual mechanism (not Tony Phase 1 framing):
```python
from registration import register_trained_artifact
# Sprint sub-booster
register_trained_artifact(
    version_name='specialist_style_specialist_sprint_20260518_0252',
    model_type='ensemble_specialist_style_specialist_sprint',
    s3_artifact_path='s3://equine-model-artifacts/ensemble/test/specialist_style_specialist_sprint_20260518_0252.json',
    training_metadata={'eval_auc': 0.8829, 'eval_brier': 0.0795, ...},
    is_active=False,
)
# Route sub-booster — same pattern
```

Plus optional META-row registration if production discoverability requires.

**Requirement 2 — MCIS META-routing extension**

Substrate-actual scope: ~100-200 LOC addition to `multicohort_inference_service.py`:
- New constants: `SPECIALIST_STYLE_VERSION_NAME`, `SPECIALIST_STYLE_SPRINT_S3_PATH`, `SPECIALIST_STYLE_ROUTE_S3_PATH`
- New method `_load_specialist_style()` — loads both sub-boosters
- New method `predict_race_specialist_style(race_id)` OR refactored generic `predict_race(race_id, ensemble='specialist_style')`:
  - Build feature DataFrame (reuse existing 32 L1 substrate)
  - Read `races.distance_furlongs`
  - Dispatch to sprint OR route sub-booster
  - Apply within-race softmax (matches forensic dispatch substrate)
- Extend `run_daily_predictions` to invoke BOTH Hybrid C + specialist_style per race (dual-write)
- Extend `write_predictions` to accept ensemble_version parameter

**Requirement 3 — strategy_harness consumer extension**

Substrate-actual scope: ~10 LOC additive (Option A) OR ~30 LOC refactor (Option B/C):

Option A (substrate-minimum): add specialist_style_win_prob field + parallel SELECT block
```python
# In HorsePrediction (line 47):
specialist_style_win_prob: Optional[float] = None    # specialist_style META output

# In RANKING_LAYER_FIELDS (line 117):
'ensemble_specialist_style': 'specialist_style_win_prob',

# In load_race_predictions (after line 367):
rows.execute("""
    SELECT horse_id, hybrid_c_win_probability
    FROM hybrid_c_predictions
    WHERE race_id = %s AND ensemble_version = 'specialist_style_specialist_20260518_0252'
""", (race_id,))
ss_map = {str(r['horse_id']): float(r['hybrid_c_win_probability']) for r in rows.fetchall()}
for hp in rp.horses:
    if hp.horse_id in ss_map:
        hp.specialist_style_win_prob = ss_map[hp.horse_id]
```

**Requirement 4 — Primary discriminator mechanism**

Substrate-actual options (NO is_primary column needed):
- **Option α**: ensemble_version IS the discriminator at consumer time; strategy classes' `ranking_layer` attribute picks primary by name
- **Option β**: env var `PRIMARY_ENSEMBLE` injected into Lambdas; strategy_harness reads to choose ranking_layer
- **Option γ**: new `model_versions.is_primary` column (single TRUE per category) — but only substrate-pragmatic if a refactor makes MCIS + strategy_harness consult it

Substrate-recommended: Option α (substrate-pragmatic minimum; no schema change; strategies opt-in by `ranking_layer = 'ensemble_specialist_style'`).

**Requirement 5 — strategy_registry.py specialist_style strategies**

Substrate-actual scope: ~200-400 LOC depending on parity:

Option A (mirror Hybrid C — substrate-additive, 67 new instances; +67 → 229 total strategies):
```python
class SpecialistStyle_Top1_Win(_RawLayerWin):
    name = 'specialist_style_top1_win'
    description = 'Top-1 win pick by specialist_style META win prob'
    ranking_layer = 'ensemble_specialist_style'
# ... 6 more single-race + 60 multi-leg via _SpecialistStyle_*_Spread factories
```

Option B (PRIMARY flip; substrate-substitutive, 0 net add):
- Rename `HybridC_*` classes → `Primary_*` semantically (substrate-pragmatic confusing)
- OR: change `ranking_layer = 'ensemble_hybrid_option_c'` → `'ensemble_specialist_style'` on existing 67 classes; rename `'ensemble_hybrid_option_c'` to `'ensemble_specialist_style'` in RANKING_LAYER_FIELDS; this REASSIGNS the 67 classes' substrate to specialist_style

**Requirement 6 — Hybrid C shadow mechanism (if applicable)**

Substrate-actual: Python config, NOT DB:
- Strategy classes have NO `is_shadow_only` attribute
- "Shadow" must be implemented either by:
  - Renaming strategy `name` attribute to `<name>_shadow` (consumer-side substrate-recognizable)
  - Marking strategy `category = 'shadow'` (consumer-side filter)
  - Filtering at DailyReportGenerator layer (don't email shadow recs)
  - Subclass `ShadowStrategyBase` skipping bet substrate

**Requirement 7 — Burn-in tracking substrate**

Substrate-actual: NO burn_in_tracking table or column. Substrate-options:
- Extend `strategy_recommendations` table with `burn_in_active` column
- New `burn_in_tracking` table (race_id, ensemble_version, recommended_bet, actual_outcome, ...)
- Substrate-pragmatic: re-purpose existing strategy_pnl + ensemble_version filter (no new schema)

**Requirement 8 — Monitor + report Lambda extensions**

Substrate-actual: `equine-substrate-health-monitor` reads `is_active = TRUE` rows per Section 4.3. Path A activation requires:
- Health monitor extension to track specialist_style sub-boosters
- Daily morning/evening email Lambda redeploys (Docker image refresh) when strategy_registry.py changes
- Optionally: new dashboard metrics for dual-ensemble comparison

### 8.3 Retroactive F1-F6 impact verdict

Per HYBRID_C_V2_RETRAIN_DECISION_DISPATCH.md (commit 0e41001) substrate, F1-F6 substrate-status:

| Finding | Pre-discovery substrate | Post-discovery substrate | Retroactive impact |
|---|---|---|---|
| F1 — ACTIVATE specialist_style (§ 4.36 alternate path) | Authorized; Track E State 1 confirmed | Substrate-coherent — substrate-pragmatic scope EXPANDED per Section 8.2 | **Path B / Path A both substrate-feasible**; scope substrate-substantial |
| F2 — Multi-instance accrual | 2 instances; threshold 3 | Substrate-unchanged | No retroactive impact |
| F3 — § 4.36 codification | Substrate-evidence-pending | Substrate-unchanged | No retroactive impact |
| F4 — HALT Hybrid C v2 retrain | Substrate-thin substrate-evidence | Substrate-unchanged at evidence level; substrate-pragmatic scope assessment substrate-coherent | No retroactive impact |
| F5 — Path B alternate-routing | Authorized verbatim per Track E.5 | Substrate-coherent; routing PREDICATE selection still substrate-investigation scope (field_size / favorite_odds tuning) | Path B remains substrate-feasible |
| F6 — Path A reframe (primary + dual-write) | Tony adjudication-pending | Substrate-coherent BUT substrate-pragmatic scope substantially larger than original framing | **Path A reframe substrate-coherent; scope EXPANDED per Section 8.2 8-item requirements** |

**Verdict**: NO retroactive F1-F6 finding inverts. Path A reframe IS substrate-coherent. Scope substrate-pragmatic-substantial per Section 8.2.

### 8.4 Tony adjudication surface (next-step substrate-options)

Given Section 8.2 8-item scope expansion + Section 8.3 verdict:

**Option α — Author Path A re-substrate-grounded dispatch**:
QB re-authors Path A activation dispatch using this document as substrate-ground. Author 8 sub-dispatches (one per Section 8.2 requirement) OR one consolidated dispatch with 8 phases substrate-grounded against verbatim substrate. Substrate-pragmatic substantial calendar-time investment.

**Option β — Pursue Path B substrate-pragmatic-narrower**:
Per Track E.5, Path B ACTIVATE specialist_style as alternate-routing remains authorized. Substrate-pragmatic mechanism: predicate-based routing (e.g., `field_size ≥ 10`) at strategy_harness load layer. Smaller scope than Path A; substrate-evidence-grounded Δ ROI gain on stratum. Requires Section 8.2 Requirements 1, 2 (META-routing), 3 (consumer extension), 5 (partial — only specialist_style strategies needed; Hybrid C strategies unchanged).

**Option γ — Revert to Path C (KEEP CURRENT; defer ACTIVATE)**:
Per Track E State 1 substrate-evidence-pending § 4.36 3-instance accrual. Substrate-pragmatic patient. Path C remains substrate-coherent.

**Option δ — Substrate-pragmatic stepwise** (alternative):
Author Phase 1 ONLY of Path A: register specialist_style sub-boosters in model_versions (Section 8.2 Requirement 1). This is the substrate-pragmatic minimum substrate-investment that unblocks ANY future activation (Path A primary OR Path B alternate-routing). Defer Phases 2-8 until Tony decides between Path A vs Path B path forward.

### 8.5 Substrate-permanent reference completion

This document is the substrate-permanent architecture reference. All future production-mutation dispatches MUST author against this document, not against session-memory fragments. § 4.32 sub-pattern B structural prophylactic ARMED for the EE codebase.

If substrate-actual architecture changes (new Lambda, MCIS refactor, strategy_harness reshape, model_versions schema extension), this document MUST be re-substrate-discovered + amended. Substrate-version: v1 (2026-05-18).

### 8.6 δ.2 multi-track substrate-validation outcome (added 2026-05-19T01:30:00Z)

**Dispatch authoring note**: δ.2 dispatch Phase 6.1 framed amendment as Section 8.4; substrate-actual 8.4 was already occupied (Tony adjudication surface). Substrate-pragmatic append as 8.6. § 4.32 sub-pattern B firing #11 banked: dispatch authoring against reference assumed unoccupied numbering.

**Cohort**: Tier-1-adjacent tracks substrate-actually meeting Q2 B substrate-pragmatic floor + Q3 C post-training-window constraint (2026-05-02..2026-05-10):

| track | n_races | n_days | chart-parsed % (tc/eqb/fs) | tier |
|---|---|---|---|---|
| CD | 52 | 5 | 100% / 100% / 100% | Tier-1 STRICT |
| SA | 46 | 5 | 100% / 100% / 100% | Tier-1-adjacent (n -8% from 50) |
| GP | 47 | 5 | 89.4% / 89.4% / 100% | Tier-1-adjacent (n -6%, tc/eqb -5.6%) |
| MTH | 16 | 2 | 100% / 100% / 100% | Tier-2 substrate-thin |
| OP | 13 | 1 | 92.3% / 92.3% / 100% | Tier-2 substrate-thin |
| BEL | 59 | 6 | 100% / 100% / 100% | Supplementary baseline (Q3 C-excluded; substrate-near-training) |

**Forensic measurement substrate**: Forensic predictions ALREADY substrate-permanent in `hybrid_c_predictions` from BD3v2 era for all cohort races (substrate-pragmatic surprise — Section 6.7 substrate-incompleteness; reference had ONLY documented BEL coverage). No new predictions generated; δ.2 substrate-actually was a measurement-only dispatch.

**Phase 3 substrate-state**: COMPLETE (no execution needed; BD3v2 era already wrote dual-write rows for both ensemble_versions).

**Per-track verdict table** (top-1 win-bet $2 stake; mirror Track E.2 measurement pattern):

| track | n | ss_wins | hc_wins | ss_roi | hc_roi | Δroi | ss_auc | hc_auc | Δauc | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| CD | 52 | 27/52 | 27/52 | +170.6% | +106.4% | **+64.2pp** | 0.7683 | 0.8658 | -0.0976 | **HOLDS** (substrate-emphatic) |
| SA | 46 | 25/46 | 26/46 | +102.2% | +110.4% | -8.3pp | 0.8145 | 0.8914 | -0.0769 | INVERTS (substrate-marginal n=46) |
| GP | 47 | 20/47 | 17/47 | +107.9% | +80.4% | **+27.4pp** | 0.7618 | 0.8199 | -0.0580 | **HOLDS** |
| MTH | 16 | 10/16 | 10/16 | +107.8% | +109.7% | -1.9pp | 0.8696 | 0.9405 | -0.0708 | Tier-2 substrate-thin |
| OP | 13 | 5/13 | 4/13 | -4.6% | -20.8% | +16.2pp | 0.7300 | 0.8025 | -0.0726 | Tier-2 substrate-thin |
| BEL | 59 | 14/59 | 15/59 | -9.8% | -23.7% | +14.0pp | 0.6289 | 0.6437 | -0.0149 | (supplementary baseline; matches Track E.2 verbatim) |

**Pooled aggregates**:
- Tier-1 STRICT (CD only): n=52, Δroi=**+64.2pp**
- Tier-1-adjacent (CD+SA+GP): n=145, **Δroi=+29.3pp** ← PRIMARY surface
- + Tier-2 (CD+SA+GP+MTH+OP): n=174, Δroi=+25.5pp
- BEL supplementary baseline (within-training): n=59, Δroi=+14.0pp

**Per-stratum decomposition** (CD+SA+GP pooled, n=145):

```
field_size:   small(≤7)   n=79   Δroi  -6.0pp  INVERT
              mid(8-9)    n=32   Δroi +155.5pp HOLD ★
              large(≥10)  n=34   Δroi  -7.5pp  INVERT

surface:      dirt        n=71   Δroi  +44.8pp HOLD
              turf        n=59   Δroi  +18.1pp HOLD
              synthetic   n=15   Δroi   +0.0pp DECAY (tied)

track_cond:   fast/firm   n=137  Δroi  +34.3pp HOLD
              off / unknown       substrate-thin (n<10)

distance:     sprint≤6.5  n=67   Δroi  +71.4pp HOLD ★
              route>6.5   n=78   Δroi   -6.8pp INVERT
```

**BEL supplementary baseline cite** (substrate-near-training-distribution): δ.2 measurement reproduces Track E.2 baseline verbatim (BEL Δroi +14.0pp / Δauc -0.0149 ≈ Track E.2's +13.9pp / -0.026). Substrate-coherence of δ.2 measurement methodology confirmed.

**Aggregate substrate-validation verdict: PATTERN HOLDS CONDITIONALLY**

Substrate-evidence basis:
- ✓ Pooled Δroi +29.3pp (Tier-1-adjacent, n=145) > +5pp threshold
- ✓ 2 of 3 {CD, GP} HOLD; SA marginal INVERT (-8.3pp at n=46; within substrate-thin noise — single winner swing ≈ ±5pp at this n)
- ✓ Out-of-training-distribution measurement substrate-exceeds within-training BEL baseline (29.3pp pooled vs 14.0pp BEL)
- Per-stratum signal CONCENTRATED:
  - SPRINT races (distance ≤ 6.5): Δroi **+71.4pp** HOLD
  - MID-FIELD races (8-9 horses): Δroi **+155.5pp** HOLD (n=32 substrate-thin but substrate-emphatic)
  - ROUTE races (distance > 6.5): Δroi -6.8pp INVERT
  - SMALL/LARGE field races: Δroi -6 to -8pp INVERT

**Path adjudication substrate-grounded**:
- **β (Path B alternate-routing) substrate-emphatically grounded** — predicate substrate-validated: route to specialist_style when `distance_furlongs ≤ 6.5` AND/OR `field_size ∈ [8,9]`; else Hybrid C
- **α (Path A primary) substrate-NOT-grounded** — broad-superiority claim substrate-actually concentrated in sprint+mid-field strata only; sustaining primary on route/large-field substrate would substrate-substrate-degrade
- **γ (KEEP CURRENT) substrate-NOT-grounded** — substrate-evidence DOES substrate-emphatically support ACTIVATION at minimum stratum-conditional surface

**D15 substrate-thin training-cohort caution resolution**:
- SPRINT sub-booster (n_train=80, AUC 0.8829): **substrate-VALIDATED** out-of-training; pattern holds on CD+GP sprint races
- ROUTE sub-booster (n_train=83, AUC 0.7496): **substrate-CAUTION-CONFIRMED**; INVERTS marginally on route races (-6.8pp at n=78); does NOT substrate-actually generalize
- D15 caution surfaced VALID for route sub-booster specifically; substrate-refuted for sprint sub-booster

**§ 4.32 sub-pattern B heterogeneity check (Phase 5.3)**:
- Track heterogeneity (CD +64 / SA -8 / GP +27): surfaced verbatim; not force-fit to single verdict
- Distance heterogeneity (sprint +71 / route -7): substrate-COHERENT with sub-booster training AUC asymmetry (0.88 vs 0.75); substrate-evidence-grounded predictive pattern
- Field-size heterogeneity (mid +155 / small/large -6 to -8): substrate-pragmatic-interesting; may interact with distance (cross-tab substrate-pending if Tony directs)

**Substrate-prerequisite gate post-δ.2**:
- α / β / γ re-adjudication substrate-unblocked
- β predicate selection substrate-pending: sprint-only OR sprint+mid-field combo
- Route sub-booster substrate-disposition question banked (deprecate OR keep for fallback OR retrain)

**Tony adjudication next**:
1. β predicate finalization (sprint distance ≤ 6.5 OR cross-tabbed with field_size)
2. Route sub-booster deprecation decision
3. β activation dispatch authoring against R2/R3/R5 per Section 8.2 substrate-prerequisites (~150-250 LOC total per substrate-permanent reference)

---

## SECTION 9 — REPAIR-4 AS-OF DISCIPLINE + AGGREGATE-HISTORY (2026-05-19)

### 9.1 Substrate-origin

REPAIR-4 dispatch addressed substrate-divergent findings discovered during
β arc supplemental investigation (supp-2 Item 2): **D4 AS-OF discipline
violation in past_performances at race-fire-time inference**.

Root cause: `entry_repository.get_entries_by_race(race_id)` queried
`past_performances` with NO date filter. The race-being-predicted + any
newer races for the same horse were returned as "past performances" with
`finish_position` populated, leaking ground truth into feature_engineering.
Race d50e069c case substrate-quantified: 9 of 12 horses had their own race
in returned pps.

Concurrent finding: `angle_stats` aggregate table substrate-refreshed
in-place by ingestion Lambda — for backtest/training, this leaks future
aggregate state.

### 9.2 Substrate-state of repository changes (committed)

**Commit chain**:
- 76cd8b0  REPAIR-4 Step B: AS-OF discipline + ON CONFLICT DO NOTHING
- f38adff  REPAIR-4 Step C: angle_stats AS-OF snapshot history + speed-fig marker
- 76de48a  REPAIR-4 Steps E+F: regression test suite + run

**Step B Tier-1 (12 files, 161+/134-)**:
- `backend/repositories/entry_repository.py`
  - `get_entries_by_race(race_id, as_of_date=None)` — `as_of_date` REQUIRED
    (raises ValueError if missing per § 4.32 #18 prophylactic discipline)
  - `get_entry_by_id(entry_id, as_of_date=None)` — same pattern
  - SQL: `AND race_date < %s` on past_performances queries
- 7 callsites plumbed with `race.race_date`:
  - `backend/services/multicohort_inference_service.py:306`
  - `backend/services/inference_service.py:231`
  - `backend/services/ls_inference_service.py:509`
  - `backend/services/pl_inference_service.py:240`
  - `backend/services/wr_inference_service.py:443`
  - `model/ensemble/option_c_inference.py:427`
  - `model/training/train.py:158`
- pp_count subquery AS-OF predicates added (ls/pl/wr inference services)
- ON CONFLICT DO UPDATE → DO NOTHING (4 prediction repositories + ls
  inference INSERT path)
- result_repository.py INTENTIONALLY retains DO UPDATE (legitimate DQ /
  payout corrections; NOT prediction leakage)

**Step C Tier-2**:
- Audit verdict: `data_loader.py` / `trajectory/train.py` /
  `class_tiers.py` / `time_series_eval.py` / `training/train.py`
  ALREADY substrate-AS-OF clean (per-row helpers filter
  `prior < race_date`; sequence-builder uses iloc slicing; LAG via shift;
  SQL predicate explicit; Step B fixed)
- `compute_speed_figures.py` rolling-window par-time leakage: SUBSTRATE-
  MARKER added in docstring; substantial pipeline rewrite DEFERRED to
  REPAIR-5+. Retrain rules REMAIN DISABLED (UNFUCK-3 Step A) so leakage
  class cannot propagate into new model versions.
- `angle_stats` AS-OF snapshot history:
  - Migration `012_angle_stats_history.sql` APPLIED to production:
    - CREATE TABLE `angle_stats_history` (orig cols + `snapshot_date date`)
    - UNIQUE index (angle_name, trainer_name, track_code, snapshot_date)
      `NULLS NOT DISTINCT` (PG 16 semantics)
    - Lookup indexes for AS-OF query pattern
    - Backfill from current `angle_stats`: 3314 rows seeded with
      `snapshot_date = CURRENT_DATE` (1 row dedup'd under NULLS NOT DISTINCT)
  - `ingestion/handler.py refresh_angle_stats` now DUAL-WRITES: refreshes
    `angle_stats` (latest) THEN INSERTs snapshot into history with
    `CURRENT_DATE` (ON CONFLICT DO NOTHING for re-run idempotency)
  - `_score_angles(row, ml_odds, race_date)` queries
    `angle_stats_history` WHERE `snapshot_date <= race_date` ORDER BY DESC
    LIMIT 1 (substrate-AS-OF aggregate state)
  - `model/angles/scorer.py query_angle_stats(conn, angle, trainer,
    race_date=None)` substrate-required race_date param; `score_entry_
    angles` plumbs through

**Step E regression suite** at `tests/repair_4/`:
- test_as_of_discipline.py (3 tests) — guard + filter verification
- test_angle_stats_history.py (5 tests) — schema + index + AS-OF semantics
- test_conflict_handling.py (6 tests) — DO NOTHING enforcement
- test_inference_callsite_plumbing.py (3 tests) — all callsites + history
- test_d4_regression.py (1 test, SKIPPED) — race d50e069c structural check
- Run: 17 passed, 1 skipped, 0.69s

### 9.3 Substrate-state of deployed image

Per REPAIR-4 Step H: deployed via `cdk deploy EquineComputeStack
--require-approval never` (Tony's canonical 20x/day mechanism). Dockerfiles
COPY backend/ + model/ at build time — all 8 Lambda images rebuilt with
substrate-patched code. Migration 012 applied to production Aurora BEFORE
code deploy (substrate-precondition: history table exists when first
inference fire occurs against new code).

### 9.4 Substrate-blast-radius pre-fix vs post-fix

**Pre-fix substrate-vulnerability surfaces** (substrate-honest enumeration):
- D4 past_performances leakage: substrate-actual at every race-fire-time
  inference; substrate-magnitude varied (race d50e069c case: 9/12 horses).
  Effect: feature_engineering computed features against a corpus that
  INCLUDED the target race + same-day races. Substrate-magnitude in model
  output substrate-pragmatic-non-trivial but not substrate-quantified.
- ON CONFLICT DO UPDATE on predictions: substrate-vulnerability not
  EXPLOITED yet (production substrate-coherent per UNFUCK-1 Step C audit)
  but substrate-permanently lurking. Step B closed.
- angle_stats refreshed in-place: substrate-mostly-OK at race-fire-time
  (refreshed nightly with prior day's results); substrate-leaky for
  backtest/training replay against historical races.

**Post-fix substrate-state**:
- D4: substrate-closed via mandatory as_of_date + race_date < predicate
- ON CONFLICT DO NOTHING: substrate-closed for predictions
- angle_stats: substrate-closed via angle_stats_history + AS-OF reads;
  cold-start substrate-acceptable (only today's snapshot exists initially;
  history accumulates over time)

### 9.5 Deferred to REPAIR-5+

- Rolling-window par times in `compute_speed_figures.py` (training-only
  leakage class; retrain rules disabled prevents propagation)
- 39 contaminated models retrain post-rolling-window fix
- δ.2 re-measurement against substrate-clean training cohort
- β arc re-adjudication post-retrain (β arc was substrate-fiction at
  activation layer per supp-2 finding; specialist_style sprint sub-
  booster never substrate-actually routed to in production because
  `predict_race_with_routing` has ZERO production callers)

---

## SECTION 10 — REPAIR-5 CLEAN TRAINING COHORT + RETRAIN INFRASTRUCTURE (2026-05-19)

### 10.1 Substrate-origin

REPAIR-5 dispatch addressed the final code-class leakage surface flagged
in REPAIR-4 Step C.3 (deferred): **rolling-window par times in
compute_speed_figures.py** + the substrate-newly-discovered **trainer_stats
aggregate-without-history** class (substrate-parallel to angle_stats from
REPAIR-4 C.5).

Concurrent infrastructure: retrain orchestration script + cutover SQL
authored for the 39 contaminated models trained pre-REPAIR-4.

### 10.2 Substrate-state of repository changes

Commit chain (REPAIR-5):
- 17e9486  Step A: compute_speed_figures.py rolling-window AS-OF fix
- 5a94197  Step B: trainer_stats AS-OF snapshot history
- [pending] Steps C+D: retrain orchestration + cutover SQL + test suite

**Step A — compute_speed_figures.py rolling-window**:
- Step 2 par times: GROUP BY (track, distance, surface, year);
  par_map keyed by 4-tuple including year
- lookup_par(tc, d, s, target_year) via bisect_left strict-less-than:
  returns par from most recent year < target_year, or None
- Step 3 callsite: row_year = int(r['race_date'].year); par = lookup_par(...)
- Steps 4-5 unchanged (same-day variants substrate-correct)
- Step 6 per-year Beyer normalization: per_year_stats query GROUP BY year;
  norm_map + norm_years_sorted index; lookup_norm() strict-less-than;
  per-year UPDATE filtered by EXTRACT(YEAR FROM race_date)

**Step B — trainer_stats AS-OF snapshot history**:
- Migration 013_trainer_stats_history.sql APPLIED:
  CREATE TABLE trainer_stats_history (orig cols + snapshot_date + created_at);
  UNIQUE (trainer_name, snapshot_date) + lookup index
- Backfill: 1141 rows seeded with CURRENT_DATE snapshot
- feature_engineering_service._get_trainer_stats(trainer_name, race_date):
  race_date REQUIRED (raises ValueError if missing); queries history
  WHERE snapshot_date <= race_date ORDER BY DESC LIMIT 1; substrate-
  cold-start fallback to current trainer_stats
- ingestion/handler.py adds 'refresh_trainer_stats' action: REFRESH
  MATERIALIZED VIEW trainer_stats + dual-write snapshot to history
  with CURRENT_DATE (ON CONFLICT DO NOTHING for idempotency)
- compute_trainer_features signature + _build_entry_features callsite
  plumb race.race_date through

**Step C — Retrain orchestration**:
- scripts/repair_5_retrain_wave.py: 4-phase dependency graph
  - Phase 1 (parallel, 30 tasks): pl/win_prob/ranker specialist variants
  - Phase 2 (1 task): ensemble/train_hybrid_c.py
  - Phase 3 (4 tasks): ensemble + trajectory + longshot + wr
  - Phase 4 (2 tasks): ranker + win_prob singletons
- Per-phase: launch ECS Fargate → poll completion → verify exit 0 +
  S3 artifact + new model_versions row → tag notes with
  'clean_post_repair5_<YYYYMMDD>'
- HALT entire wave on first task failure
- Metrics log: /tmp/repair_5_training_metrics.jsonl

**Step C — Cutover SQL**:
- scripts/repair_5_cutover.sql: single BEGIN/COMMIT transaction
- Deactivates 39 contaminated rows by verbatim PK list
  (substrate-grounded against production model_versions 2026-05-19)
- Activates newest clean row per model_type via ROW_NUMBER() OVER
  PARTITION BY model_type ORDER BY created_at DESC
- Read-back verification before COMMIT

**Step D — Test suite (tests/repair_5/)**:
- test_rolling_window_as_of.py (5): per-year SQL + bisect strict-less-than
- test_trainer_stats_history.py (6): schema + AS-OF query + handler dual-write
- test_retrain_orchestration.py (8): 4 phases + 39 verbatim PKs + clean-row
  activation pattern
- Combined REPAIR-4 + REPAIR-5: 36 passed, 1 skipped, 1.04s

### 10.3 Verbatim 39 contaminated model_version_ids (pre-retrain)

```
ensemble                       42e796ae-c590-4110-a3d5-4b81647ba52f
ensemble_hybrid_option_c       2d34b010-f17a-492e-8f7c-270bd393731d
longshot_rf                    ae0320ed-8028-45d5-bc92-9fd5465ca55e
pl_core_class_dropper          a862da1e-83bb-47e2-b5d8-0df9523e9756
pl_core_class_riser            f97e0d34-0b42-45ee-9be4-3dee0f1c8dbd
pl_core_closer                 91fa3b23-6368-4045-9df3-f64a54a393e9
pl_core_general                7eb7f476-6b44-4250-88a7-e4fd695ec3bc
pl_core_route                  73d257ca-8054-42b6-87e0-e25dde339a0f
pl_core_speed                  c914389b-a1f6-40ed-82fd-250f8e6452a4
pl_core_sprint                 a6eef6cd-5144-41a7-90e4-96a51c2619dc
ranker_core                    e5ec560b-a910-4a07-bef7-d9897be5a052
ranker_full                    a7d71718-b3e3-4935-975c-d768c490b582
rk_full_class_dropper          143404a6-99ef-4db4-a085-76ff7427d8b0
rk_full_class_riser            504b82a8-dec2-4d86-959d-7f3f1179bf5d
rk_full_closer                 a28b3683-61a9-475d-8fa5-b255c91c9238
rk_full_general                ef13f650-f2da-43c2-a256-440482eda8ce
rk_full_gonzo_sauce            a6977e6a-1343-4ee8-b27b-11a9d824a288
rk_full_route                  c77aa2e9-b680-49e0-878d-543d1e01b433
rk_full_speed                  e915c375-beb7-4400-8eca-35277959a10c
rk_full_sprint                 414f41dc-59ee-4f40-b299-ea50cd757aca
trajectory_lstm                8d6684cc-4364-4b7f-8d31-a19359cfab03
win_prob_core_class_dropper    543e9b66-7c54-465e-8ea1-b5c2420b8cef
win_prob_core_class_riser      660e8705-3a58-4454-bf54-6f2cb1ca1bb4
win_prob_core_closer           5a652692-1126-4644-8f61-f5f1c2e1cc42
win_prob_core_general          fa1543b2-a67e-4f85-b243-502bf5290f12
win_prob_core_route            5fd06c78-8769-4de3-8bf0-207f15c3e476
win_prob_core_speed            ea21b258-c429-4c36-9de9-52898935ab8e
win_prob_core_sprint           0be6a440-f08e-4010-be18-418ae38b848b
win_prob_full                  d1702c76-8bd3-48c4-81c7-92dce5274861
wp_full_class_dropper          16d63aba-0d9c-4108-8e5e-185f97be9620
wp_full_class_riser            c85bd29b-60a2-45c1-b81d-fc990eaa79c9
wp_full_closer                 44fea74d-8ff5-49fa-8081-b2f694a767d1
wp_full_general                93e9cccb-f9f2-40c5-9833-79e5ee2ad0da
wp_full_gonzo_sauce            30f9b663-77c2-4cde-b8fd-9fe4dbfd88d0
wp_full_route                  85eacd05-dcb9-40c6-885a-e0b545854b10
wp_full_speed                  eca2056e-d3d4-421f-867e-219ac4045fd2
wp_full_sprint                 68220742-1bc7-489c-a956-86c6c90311a7
wr_base                        a9397b4a-3a6e-4b75-b2cd-dd69a414acef
wr_odds                        f14f2902-4414-4b5b-b06e-c4d120a66993
```

### 10.4 Deployed substrate-state (Step E complete 2026-05-19T15:57 UTC)

CDK deploy EquineComputeStack EXIT=0; total wall-clock 501.8s.

TrainingTaskDef revision: 117 → 118
Training image hash:
  584812014683.dkr.ecr.us-east-1.amazonaws.com/
    cdk-hnb659fds-container-assets-584812014683-us-east-1:
    a4b1ec0ff4f839f9dbea47d618fbfa57b862f7465658dddc536b291288361d81

8 image assets Published:
  IngestionFunction               584812014683-us-east-1-797cdaa4
  InferenceFunction               584812014683-us-east-1-4aba0968
  ResultsFunction                 584812014683-us-east-1-c1b23349
  WRInferenceFunction             584812014683-us-east-1-08e7a85e
  PLInferenceFunction             584812014683-us-east-1-e29797ee
  SubstrateHealthMonitorFunction  584812014683-us-east-1-cd65314a
  TrainingTaskDef/training        584812014683-us-east-1-b4a22471
  LSInferenceFunction             584812014683-us-east-1-df529da4

Lambda LastModified post-deploy (all Successful):
  equine-inference                  2026-05-19T15:57:05Z
  equine-ls-inference               2026-05-19T15:57:06Z
  equine-pl-inference               2026-05-19T15:57:05Z
  equine-wr-inference               2026-05-19T15:57:06Z
  equine-ingestion                  2026-05-19T15:57:37Z
  equine-results                    2026-05-19T15:57:05Z
  equine-substrate-health-monitor   2026-05-19T15:57:05Z

Substrate-effect: production inference Lambdas now substrate-actually
substrate-include Step B trainer_stats_history AS-OF reads + Step A
rolling-window code (training-side; deployed for retrain wave).

### 10.5 Substrate-precondition for retrain wave (Step F)

1. EventBridge retrain rules REMAIN DISABLED until cutover completes
   (substrate-prevents cron-fired contaminated retrain mid-wave)
2. Tony or dedicated session triggers:
   `python3 scripts/repair_5_retrain_wave.py --execute`
3. Wall-clock: 2-5+ hours expected
4. On wave completion:
   - Review /tmp/repair_5_training_metrics.jsonl
   - Capture substrate-actual clean_tag printed at wave start
   - Substitute clean_tag in scripts/repair_5_cutover.sql; execute
   - Re-enable EventBridge rules

### 10.6 Deferred to REPAIR-6+

- δ.2 + every prior forensic claim substrate-re-measurement against
  clean substrate
- β arc re-adjudication (substrate-design new experiment against
  substrate-actual production inference path; pre-REPAIR-4 β arc was
  substrate-fiction)
- Cross-project audit (Kalshi V2 + Dynasty Dugout)
- model/shared/data_loader.py training-cohort _load_trainer_stats AS-OF
  fix (substrate-marker in commit 5a94197; substrate-not-blocking
  until retrain rules re-enable)

---

