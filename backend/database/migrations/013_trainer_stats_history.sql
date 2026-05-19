-- 013_trainer_stats_history.sql
-- REPAIR-5 Step B — trainer_stats AS-OF snapshot history
--
-- Substrate-discipline: trainer_stats is a materialized view aggregating
-- all past_performances rows into per-trainer career stats. At any moment
-- it reflects ALL historical races to date — including future races
-- relative to any training cohort row. Substrate-leakage class identical
-- to angle_stats from REPAIR-4 C.5.
--
-- Fix: snapshot to trainer_stats_history per refresh with snapshot_date.
-- AS-OF reads pull WHERE snapshot_date <= race_date ORDER BY DESC LIMIT 1.

CREATE TABLE IF NOT EXISTS trainer_stats_history (
    trainer_name      varchar(100) NOT NULL,
    total_starts      bigint       NOT NULL DEFAULT 0,
    wins              bigint       NOT NULL DEFAULT 0,
    win_rate          numeric,
    itm               bigint       NOT NULL DEFAULT 0,
    itm_rate          numeric,
    layoff_win_rate   numeric,
    lasix_win_rate    numeric,
    claimed_win_rate  numeric,
    snapshot_date     date         NOT NULL,
    created_at        timestamp    NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_trainer_stats_history_unique
    ON trainer_stats_history (trainer_name, snapshot_date);

CREATE INDEX IF NOT EXISTS idx_trainer_stats_history_lookup
    ON trainer_stats_history (trainer_name, snapshot_date DESC);

-- Backfill: seed today's snapshot from current trainer_stats materialized view.
INSERT INTO trainer_stats_history (
    trainer_name, total_starts, wins, win_rate, itm, itm_rate,
    layoff_win_rate, lasix_win_rate, claimed_win_rate, snapshot_date
)
SELECT
    trainer_name, total_starts, wins, win_rate, itm, itm_rate,
    layoff_win_rate, lasix_win_rate, claimed_win_rate, CURRENT_DATE
FROM trainer_stats
ON CONFLICT DO NOTHING;
