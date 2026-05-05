-- Migration 008: Create trainer_stats materialized view
-- Aggregates career win/ITM/layoff/Lasix/claimed stats by trainer.
-- Minimum 5 starts required to appear in view.
-- feature_engineering_service._get_trainer_stats() queries this.
-- Refresh manually after large data loads: REFRESH MATERIALIZED VIEW trainer_stats

CREATE MATERIALIZED VIEW IF NOT EXISTS trainer_stats AS
SELECT
    trainer_name,
    COUNT(*)                                               AS total_starts,
    SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END) AS wins,
    ROUND(
        SUM(CASE WHEN finish_position = 1 THEN 1 ELSE 0 END)::numeric
        / NULLIF(COUNT(*), 0), 4
    )                                                      AS win_rate,
    SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END) AS itm,
    ROUND(
        SUM(CASE WHEN finish_position <= 3 THEN 1 ELSE 0 END)::numeric
        / NULLIF(COUNT(*), 0), 4
    )                                                      AS itm_rate,
    ROUND(
        SUM(CASE
            WHEN days_since_last_race >= 30
             AND finish_position = 1
            THEN 1 ELSE 0
        END)::numeric
        / NULLIF(SUM(CASE
            WHEN days_since_last_race >= 30
            THEN 1 ELSE 0
        END), 0), 4
    )                                                      AS layoff_win_rate,
    ROUND(
        SUM(CASE
            WHEN lasix_first_time = true
             AND finish_position = 1
            THEN 1 ELSE 0
        END)::numeric
        / NULLIF(SUM(CASE
            WHEN lasix_first_time = true
            THEN 1 ELSE 0
        END), 0), 4
    )                                                      AS lasix_win_rate,
    ROUND(
        SUM(CASE
            WHEN was_claimed = true
             AND finish_position = 1
            THEN 1 ELSE 0
        END)::numeric
        / NULLIF(SUM(CASE
            WHEN was_claimed = true
            THEN 1 ELSE 0
        END), 0), 4
    )                                                      AS claimed_win_rate
FROM past_performances
WHERE trainer_name    IS NOT NULL
  AND finish_position IS NOT NULL
  AND finish_position < 90
GROUP BY trainer_name
HAVING COUNT(*) >= 5;

CREATE UNIQUE INDEX IF NOT EXISTS idx_trainer_stats_name
    ON trainer_stats (trainer_name)
