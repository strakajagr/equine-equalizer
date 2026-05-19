-- 012_angle_stats_history.sql
-- REPAIR-4 Step C.5 — angle_stats AS-OF snapshot history
--
-- Substrate-discipline: angle_stats is substrate-aggregate refreshed in-place
-- by ingestion Lambda action='refresh_angle_stats'. At race-fire-time, current
-- angle_stats is approximately AS-OF (today's races' results not in yet) but
-- BACKTEST/TRAINING reads of angle_stats are substrate-leaky — they see
-- aggregates that include future races.
--
-- Fix: snapshot per-refresh into angle_stats_history with snapshot_date. AS-OF
-- inference reads pull WHERE snapshot_date <= race.race_date ORDER BY DESC
-- LIMIT 1.

CREATE TABLE IF NOT EXISTS angle_stats_history (
    angle_name    varchar(50)  NOT NULL,
    trainer_name  varchar(200),
    track_code    varchar(10),
    wins          integer      NOT NULL DEFAULT 0,
    starts        integer      NOT NULL DEFAULT 0,
    snapshot_date date         NOT NULL,
    created_at    timestamp    NOT NULL DEFAULT now()
);

-- NULLS NOT DISTINCT (PG 15+) — angle_stats permits NULL trainer_name
-- (global angle row) + NULL track_code. Without NULLS NOT DISTINCT,
-- multiple "global" rows per snapshot_date would be permitted under the
-- default NULL-distinct semantics.
CREATE UNIQUE INDEX IF NOT EXISTS idx_angle_stats_history_unique
    ON angle_stats_history (angle_name, trainer_name, track_code, snapshot_date)
    NULLS NOT DISTINCT;

CREATE INDEX IF NOT EXISTS idx_angle_stats_history_lookup
    ON angle_stats_history (angle_name, trainer_name, snapshot_date DESC);

CREATE INDEX IF NOT EXISTS idx_angle_stats_history_global_lookup
    ON angle_stats_history (angle_name, snapshot_date DESC)
    WHERE trainer_name IS NULL;

-- Backfill: seed today's snapshot from current angle_stats.
-- ON CONFLICT DO NOTHING so re-running the migration is substrate-safe.
INSERT INTO angle_stats_history (
    angle_name, trainer_name, track_code, wins, starts, snapshot_date
)
SELECT angle_name, trainer_name, track_code, wins, starts, CURRENT_DATE
FROM angle_stats
ON CONFLICT DO NOTHING;
