-- REPAIR-5 Step H — model_versions cutover transaction
--
-- Substrate-precondition: scripts/repair_5_retrain_wave.py completed
-- successfully; new clean model_versions rows tagged in notes field with
-- 'clean_post_repair5_<YYYYMMDD>' marker; all 39 model_types have at
-- least one new clean row inserted at is_active=FALSE.
--
-- Substrate-execution: single BEGIN/COMMIT transaction substrate-deactivates
-- the 39 contaminated rows + substrate-activates clean rows in lockstep.
-- Partial unique index idx_active_model_per_type WHERE is_active=true
-- substrate-validates that exactly one row per model_type ends active.
--
-- Substrate-rollback: on assertion failure inside transaction, ROLLBACK.
-- Substrate-cross-check pre/post via:
--   /tmp/repair_5_pre_cutover_snapshot.md
--   /tmp/repair_5_post_cutover_snapshot.md
--
-- Substrate-tag: replace 'clean_post_repair5_YYYYMMDD' below with the
-- substrate-actual tag printed by repair_5_retrain_wave.py at wave start.

\set clean_tag 'clean_post_repair5_REPLACE_WITH_ACTUAL_DATE'

BEGIN;

-- Phase 1 — Deactivate the 39 contaminated model_versions rows verbatim.
-- Substrate-grounded against production model_versions as of 2026-05-19.
UPDATE model_versions
SET is_active = FALSE
WHERE model_version_id IN (
    '42e796ae-c590-4110-a3d5-4b81647ba52f', -- ensemble
    '2d34b010-f17a-492e-8f7c-270bd393731d', -- ensemble_hybrid_option_c
    'ae0320ed-8028-45d5-bc92-9fd5465ca55e', -- longshot_rf
    'a862da1e-83bb-47e2-b5d8-0df9523e9756', -- pl_core_class_dropper
    'f97e0d34-0b42-45ee-9be4-3dee0f1c8dbd', -- pl_core_class_riser
    '91fa3b23-6368-4045-9df3-f64a54a393e9', -- pl_core_closer
    '7eb7f476-6b44-4250-88a7-e4fd695ec3bc', -- pl_core_general
    '73d257ca-8054-42b6-87e0-e25dde339a0f', -- pl_core_route
    'c914389b-a1f6-40ed-82fd-250f8e6452a4', -- pl_core_speed
    'a6eef6cd-5144-41a7-90e4-96a51c2619dc', -- pl_core_sprint
    'e5ec560b-a910-4a07-bef7-d9897be5a052', -- ranker_core
    'a7d71718-b3e3-4935-975c-d768c490b582', -- ranker_full
    '143404a6-99ef-4db4-a085-76ff7427d8b0', -- rk_full_class_dropper
    '504b82a8-dec2-4d86-959d-7f3f1179bf5d', -- rk_full_class_riser
    'a28b3683-61a9-475d-8fa5-b255c91c9238', -- rk_full_closer
    'ef13f650-f2da-43c2-a256-440482eda8ce', -- rk_full_general
    'a6977e6a-1343-4ee8-b27b-11a9d824a288', -- rk_full_gonzo_sauce
    'c77aa2e9-b680-49e0-878d-543d1e01b433', -- rk_full_route
    'e915c375-beb7-4400-8eca-35277959a10c', -- rk_full_speed
    '414f41dc-59ee-4f40-b299-ea50cd757aca', -- rk_full_sprint
    '8d6684cc-4364-4b7f-8d31-a19359cfab03', -- trajectory_lstm
    '543e9b66-7c54-465e-8ea1-b5c2420b8cef', -- win_prob_core_class_dropper
    '660e8705-3a58-4454-bf54-6f2cb1ca1bb4', -- win_prob_core_class_riser
    '5a652692-1126-4644-8f61-f5f1c2e1cc42', -- win_prob_core_closer
    'fa1543b2-a67e-4f85-b243-502bf5290f12', -- win_prob_core_general
    '5fd06c78-8769-4de3-8bf0-207f15c3e476', -- win_prob_core_route
    'ea21b258-c429-4c36-9de9-52898935ab8e', -- win_prob_core_speed
    '0be6a440-f08e-4010-be18-418ae38b848b', -- win_prob_core_sprint
    'd1702c76-8bd3-48c4-81c7-92dce5274861', -- win_prob_full
    '16d63aba-0d9c-4108-8e5e-185f97be9620', -- wp_full_class_dropper
    'c85bd29b-60a2-45c1-b81d-fc990eaa79c9', -- wp_full_class_riser
    '44fea74d-8ff5-49fa-8081-b2f694a767d1', -- wp_full_closer
    '93e9cccb-f9f2-40c5-9833-79e5ee2ad0da', -- wp_full_general
    '30f9b663-77c2-4cde-b8fd-9fe4dbfd88d0', -- wp_full_gonzo_sauce
    '85eacd05-dcb9-40c6-885a-e0b545854b10', -- wp_full_route
    'eca2056e-d3d4-421f-867e-219ac4045fd2', -- wp_full_speed
    '68220742-1bc7-489c-a956-86c6c90311a7', -- wp_full_sprint
    'a9397b4a-3a6e-4b75-b2cd-dd69a414acef', -- wr_base
    'f14f2902-4414-4b5b-b06e-c4d120a66993'  -- wr_odds
);

-- Phase 2 — Activate the newest clean row per model_type.
-- Substrate-pragmatic substrate-pattern: for each model_type, find the
-- single most recent model_version_id where notes contains the clean tag
-- AND is_active = FALSE; set is_active = TRUE.
WITH ranked_clean AS (
    SELECT model_version_id, model_type,
           ROW_NUMBER() OVER (
             PARTITION BY model_type ORDER BY created_at DESC
           ) AS rn
    FROM model_versions
    WHERE notes LIKE '%' || :'clean_tag' || '%'
      AND is_active = FALSE
)
UPDATE model_versions mv
SET is_active = TRUE
FROM ranked_clean rc
WHERE mv.model_version_id = rc.model_version_id
  AND rc.rn = 1;

-- Phase 3 — Read-back verification within transaction.
-- Substrate-assertion: exactly 1 active row per model_type for the
-- 39 model_types substrate-encompassed by retrain wave.
SELECT model_type, COUNT(*) AS active_count
FROM model_versions
WHERE is_active = TRUE
GROUP BY model_type
ORDER BY model_type;

-- Substrate-precondition for COMMIT: above query returns exactly the
-- 39 expected model_types each with active_count=1. If divergent,
-- substrate-substrate-rollback NOW:
--   ROLLBACK;
-- Otherwise:
COMMIT;

-- Post-commit verification (run separately):
-- \i /tmp/repair_5_post_cutover_verify.sql
