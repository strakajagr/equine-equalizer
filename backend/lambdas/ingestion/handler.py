import logging
import json
import os
import sys
from datetime import date
from shared.db import get_db
from services.ingestion_service import (
    IngestionService
)

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def handler(event, context):
    logger.info(
        f"Ingestion handler called with "
        f"event: {json.dumps(event)}"
    )

    action = event.get('action')

    # ── Migration action ──
    # Invoked manually to run DB migrations
    # from inside the VPC where Aurora is reachable
    if action == 'migrate':
        logger.info("Running database migrations")
        seed = event.get('seed', False)

        try:
            # Add task root to path so migrate.py
            # can import from the same codebase
            task_root = '/var/task'
            if task_root not in sys.path:
                sys.path.insert(0, task_root)

            migrate_path = os.path.join(
                task_root,
                'database/migrations/migrate.py'
            )

            # Build args
            args = [sys.executable, migrate_path]
            if seed:
                args.append('--seed')

            import subprocess
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                env={
                    **os.environ,
                }
            )

            logger.info(
                f"Migration stdout:\n{result.stdout}"
            )
            if result.stderr:
                logger.warning(
                    f"Migration stderr:\n{result.stderr}"
                )

            success = result.returncode == 0
            logger.info(
                f"Migration {'succeeded' if success else 'FAILED'}"
                f" (exit code {result.returncode})"
            )

            return {
                'statusCode': 200 if success else 500,
                'body': json.dumps({
                    'success': success,
                    'stdout': result.stdout,
                    'stderr': result.stderr,
                    'returncode': result.returncode
                })
            }

        except Exception as e:
            logger.error(
                f"Migration exception: {e}",
                exc_info=True
            )
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'success': False,
                    'error': str(e)
                })
            }

    # ── Refresh angle_stats table ──
    if action == 'refresh_angle_stats':
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM angle_stats")
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'first_time_lasix', pp.trainer_name, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        JOIN entries e ON pp.horse_id = e.horse_id
                        WHERE e.lasix_first_time = true
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                        GROUP BY pp.trainer_name
                        HAVING COUNT(*) >= 5
                    """)
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'first_time_lasix', NULL, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        JOIN entries e ON pp.horse_id = e.horse_id
                        WHERE e.lasix_first_time = true
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                    """)
                    # blinkers_on trainer-specific
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'blinkers_on', pp.trainer_name, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        JOIN entries e ON pp.horse_id = e.horse_id
                        WHERE e.blinkers_on = true
                          AND pp.trainer_name IS NOT NULL
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                        GROUP BY pp.trainer_name
                        HAVING COUNT(*) >= 5
                    """)
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'blinkers_on', NULL, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        JOIN entries e ON pp.horse_id = e.horse_id
                        WHERE e.blinkers_on = true
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                    """)
                    # class_drop trainer-specific
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'class_drop', pp.trainer_name, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        WHERE pp.purse IS NOT NULL
                          AND pp.trainer_name IS NOT NULL
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                          AND EXISTS (
                            SELECT 1 FROM past_performances pp2
                            WHERE pp2.horse_id = pp.horse_id
                              AND pp2.race_date < pp.race_date
                              AND pp2.purse > pp.purse * 1.15
                          )
                        GROUP BY pp.trainer_name
                        HAVING COUNT(*) >= 5
                    """)
                    cur.execute("""
                        INSERT INTO angle_stats (angle_name, trainer_name, track_code, wins, starts)
                        SELECT 'class_drop', NULL, NULL,
                          COUNT(*) FILTER (WHERE pp.finish_position = 1),
                          COUNT(*)
                        FROM past_performances pp
                        WHERE pp.purse IS NOT NULL
                          AND pp.finish_position IS NOT NULL AND pp.finish_position < 90
                          AND EXISTS (
                            SELECT 1 FROM past_performances pp2
                            WHERE pp2.horse_id = pp.horse_id
                              AND pp2.race_date < pp.race_date
                              AND pp2.purse > pp.purse * 1.15
                          )
                    """)
                conn.commit()

                # REPAIR-4 C.5: snapshot today's refreshed angle_stats into
                # angle_stats_history for AS-OF inference reads. ON CONFLICT
                # DO NOTHING handles the idempotency case where this action
                # runs more than once per day.
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO angle_stats_history (
                            angle_name, trainer_name, track_code,
                            wins, starts, snapshot_date
                        )
                        SELECT angle_name, trainer_name, track_code,
                               wins, starts, CURRENT_DATE
                        FROM angle_stats
                        ON CONFLICT DO NOTHING
                    """)
                conn.commit()

                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) as cnt FROM angle_stats")
                    count = cur.fetchone()
                    cur.execute(
                        "SELECT COUNT(*) as cnt FROM angle_stats_history "
                        "WHERE snapshot_date = CURRENT_DATE"
                    )
                    hist_count = cur.fetchone()
            return {'statusCode': 200, 'body': json.dumps({
                'refreshed': True,
                'rows': count['cnt'] if isinstance(count, dict) else count[0],
                'history_snapshot_rows': hist_count['cnt'] if isinstance(hist_count, dict) else hist_count[0],
            })}
        except Exception as e:
            logger.error(f"refresh_angle_stats failed: {e}", exc_info=True)
            return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

    # ── Refresh trainer_stats materialized view + snapshot to history ──
    # REPAIR-5 Step B: dual-write pattern parallel to refresh_angle_stats.
    # Invoke periodically (manual or cron) to accumulate daily snapshots.
    if action == 'refresh_trainer_stats':
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("REFRESH MATERIALIZED VIEW trainer_stats")
                conn.commit()

                # Dual-write: snapshot today's refreshed view into history
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO trainer_stats_history (
                            trainer_name, total_starts, wins, win_rate,
                            itm, itm_rate, layoff_win_rate,
                            lasix_win_rate, claimed_win_rate, snapshot_date
                        )
                        SELECT
                            trainer_name, total_starts, wins, win_rate,
                            itm, itm_rate, layoff_win_rate,
                            lasix_win_rate, claimed_win_rate, CURRENT_DATE
                        FROM trainer_stats
                        ON CONFLICT DO NOTHING
                    """)
                conn.commit()

                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) as cnt FROM trainer_stats")
                    count = cur.fetchone()
                    cur.execute(
                        "SELECT COUNT(*) as cnt FROM trainer_stats_history "
                        "WHERE snapshot_date = CURRENT_DATE"
                    )
                    hist_count = cur.fetchone()
            return {'statusCode': 200, 'body': json.dumps({
                'refreshed': True,
                'rows': count['cnt'] if isinstance(count, dict) else count[0],
                'history_snapshot_rows': hist_count['cnt'] if isinstance(hist_count, dict) else hist_count[0],
            })}
        except Exception as e:
            logger.error(f"refresh_trainer_stats failed: {e}", exc_info=True)
            return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

    # ── Collect workouts for today's entries from HRN ──
    # Invoke: {"action": "collect_workouts"} or {"action": "collect_workouts", "date": "2026-03-21"}
    if action == 'collect_workouts':
        from datetime import date as date_type
        from shared.db import execute_query
        target_date = event.get('date')
        if target_date and target_date not in ('', 'USE_TODAY'):
            target_date = date_type.fromisoformat(target_date)
        else:
            target_date = date_type.today()
        try:
            from services.data_sources.hrn_workout_scraper import HRNWorkoutScraper
            from repositories.workout_repository import WorkoutRepository
            scraper = HRNWorkoutScraper()
            with get_db() as conn:
                # Get all horses entered today
                horses = execute_query(conn,
                    """SELECT DISTINCT e.horse_id, h.horse_name
                       FROM entries e
                       JOIN horses h ON e.horse_id = h.horse_id
                       JOIN races r ON e.race_id = r.race_id
                       WHERE r.race_date = %s""",
                    (target_date,))
                logger.info(f"collect_workouts: {len(horses)} horses entered for {target_date}")
                repo = WorkoutRepository(conn)
                fetched = 0
                inserted = 0
                errors = []
                for h in horses:
                    try:
                        workouts = scraper.fetch_workouts(
                            horse_id=h['horse_id'],
                            horse_name=h['horse_name'],
                            cutoff_start=date_type(2022, 1, 1))
                        if workouts:
                            for w in workouts:
                                try:
                                    repo.bulk_insert_workouts([w])
                                    inserted += 1
                                except Exception:
                                    pass  # duplicate, skip
                            fetched += 1
                    except Exception as e:
                        errors.append(f"{h['horse_name']}: {str(e)[:60]}")
            return {'statusCode': 200, 'body': json.dumps({
                'date': str(target_date), 'horses_checked': len(horses),
                'horses_with_workouts': fetched, 'workouts_inserted': inserted,
                'errors': errors[:10]})}
        except Exception as e:
            logger.error(f"collect_workouts failed: {e}", exc_info=True)
            return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

    # ── Fetch results from HRN (uses Playwright) ──
    # Invoke: {"action": "fetch_results", "date": "2026-03-19"}
    if action == 'fetch_results':
        from datetime import date as date_type, timedelta
        target_date = event.get('date')
        if target_date and target_date not in ('USE_TODAY_MINUS_1', ''):
            target_date = date_type.fromisoformat(target_date)
        else:
            target_date = date_type.today() - timedelta(days=1)
        try:
            from services.data_sources import HRNScraper
            from shared.db import execute_query
            scraper = HRNScraper()
            race_results = scraper.fetch_results(target_date)
            logger.info(f"HRN returned {len(race_results)} race results for {target_date}")

            inserted = 0
            skipped = 0
            errors = []
            with get_db() as conn:
                from repositories.result_repository import ResultRepository
                result_repo = ResultRepository(conn)
                for race_data in race_results:
                    tc = race_data['track_code']
                    rn = race_data['race_number']
                    # Find the race_id and entries for this race
                    race_rows = execute_query(conn,
                        """SELECT r.race_id FROM races r
                           JOIN tracks t ON r.track_id = t.track_id
                           WHERE t.track_code = %s AND r.race_number = %s
                             AND r.race_date = %s""",
                        (tc, rn, target_date))
                    if not race_rows:
                        skipped += 1
                        continue
                    race_id = race_rows[0]['race_id']
                    # Get entries for this race
                    entry_rows = execute_query(conn,
                        """SELECT e.entry_id, e.horse_id, h.horse_name
                           FROM entries e JOIN horses h ON e.horse_id = h.horse_id
                           WHERE e.race_id = %s""",
                        (race_id,))
                    from shared.horse_naming import horse_match_key
                    entry_by_name = {}
                    for er in entry_rows:
                        entry_by_name[horse_match_key(er['horse_name'])] = er
                    for result in race_data.get('results', []):
                        entry = entry_by_name.get(
                            horse_match_key(result['horse_name'])
                        )
                        if not entry:
                            continue
                        try:
                            result_repo.insert_result({
                                'entry_id': entry['entry_id'],
                                'race_id': race_id,
                                'horse_id': entry['horse_id'],
                                'finish_position': result['finish_position'],
                                'official_finish': result['official_finish'],
                                'win_payout': result.get('win_payout'),
                                'place_payout': result.get('place_payout'),
                                'show_payout': result.get('show_payout'),
                                'exacta_payout': result.get('exacta_payout'),
                                'trifecta_payout': result.get('trifecta_payout'),
                            })
                            inserted += 1
                        except Exception as e:
                            errors.append(f"{tc} R{rn} {result['horse_name']}: {str(e)[:60]}")
            return {'statusCode': 200, 'body': json.dumps({
                'date': str(target_date), 'races_from_hrn': len(race_results),
                'results_inserted': inserted, 'races_skipped': skipped,
                'errors': errors[:10]})}
        except Exception as e:
            logger.error(f"fetch_results failed: {e}", exc_info=True)
            return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

    # ── Admin SQL (TEMPORARY — for schema changes) ──
    if action == 'run_admin_sql':
        sql = event.get('sql', '')
        if not sql:
            return {'statusCode': 400, 'body': json.dumps({'error': 'sql required'})}
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql)
                conn.commit()
            return {'statusCode': 200, 'body': json.dumps({'executed': sql[:100]})}
        except Exception as e:
            return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

    # ── Register model version ──
    # Invoke: {"action": "register_model", "version_name": "...",
    #          "model_type": "wr_base", "s3_path": "s3://...",
    #          "metrics": {"flat_bet_roi": 0.108, ...}}
    if action == 'register_model':
        import uuid
        version_name = event.get('version_name')
        model_type = event.get('model_type')
        s3_path = event.get('s3_path', '')
        metrics = event.get('metrics', {})
        if not version_name or not model_type:
            return {'statusCode': 400, 'body': json.dumps({'error': 'version_name and model_type required'})}
        try:
            mid = str(uuid.uuid4())
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO model_versions (
                            model_version_id, version_name, model_type,
                            training_date, training_data_start, training_data_end,
                            s3_artifact_path, is_active,
                            flat_bet_roi, kelly_roi, value_bet_win_rate,
                            top1_accuracy, exacta_hit_rate, trifecta_hit_rate
                        ) VALUES (%s,%s,%s, NOW(), '2022-01-01', '2025-12-31',
                                  %s, false, %s,%s,%s,%s,%s,%s)
                    """, (mid, version_name, model_type, s3_path,
                          metrics.get('flat_bet_roi'), metrics.get('kelly_roi'),
                          metrics.get('value_bet_win_rate'), metrics.get('top1_win_rate'),
                          metrics.get('exacta_hit_rate'), metrics.get('trifecta_hit_rate')))
                conn.commit()
            return {'statusCode': 200, 'body': json.dumps({'model_version_id': mid, 'version_name': version_name})}
        except Exception as e:
            return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

    # ── Deactivate all models (TEMPORARY) ──
    if action == 'deactivate_all':
        try:
            with get_db() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE model_versions SET is_active = false WHERE is_active = true")
                conn.commit()
            return {'statusCode': 200, 'body': json.dumps({'deactivated': 'all'})}
        except Exception as e:
            return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

    # ── Train WR model (NEW clean pipeline) ──
    # Uses model/wr/train.py with correct temporal filtering,
    # 66-feature definitions, and EV labels.
    # Invoke: {"action": "train_wr_model"}
    if action == 'train_wr_model':
        logger.info("Running NEW WR training pipeline")
        try:
            task_root = '/var/task'
            model_root = os.path.join(task_root, 'model')

            # model/wr/train.py imports "from shared.data_loader import ..."
            # which conflicts with backend's shared/ package already in
            # sys.modules. Temporarily swap so "shared" resolves to
            # model/shared/ during the import.
            saved_shared = {
                k: sys.modules.pop(k)
                for k in list(sys.modules) if k == 'shared' or k.startswith('shared.')
            }
            sys.path.insert(0, model_root)

            from model.wr.train import main as wr_main
            wr_main()

            # Restore backend shared modules
            sys.path.remove(model_root)
            for k in list(sys.modules):
                if k == 'shared' or k.startswith('shared.'):
                    sys.modules.pop(k, None)
            sys.modules.update(saved_shared)

            return {
                'statusCode': 200,
                'body': json.dumps({'status': 'WR training complete'})
            }
        except Exception as e:
            logger.error(f"WR training failed: {e}", exc_info=True)
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    # ── Train model action ──
    # Train XGBoost ranking model on historical data
    # Invoke: {"action": "train_model"}
    # Options: start_date, end_date, set_active
    if action == 'train_model':
        logger.info("Running training pipeline")
        try:
            # Add project root to path for model imports
            task_root = '/var/task'
            if task_root not in sys.path:
                sys.path.insert(0, task_root)

            from model.training.train import (
                load_training_data,
                prepare_xgboost_data,
                train_model as do_train,
                evaluate_model,
                save_model,
                register_model,
                get_feature_importance,
                DEFAULT_PARAMS,
            )
            from datetime import date as date_type

            start = date_type.fromisoformat(
                event.get('start_date', '2022-01-01')
            )
            end = date_type.fromisoformat(
                event.get('end_date', '2025-12-31')
            )
            set_active = event.get('set_active', False)
            s3_bucket = os.environ.get(
                'MODEL_ARTIFACTS_BUCKET',
                'equine-model-artifacts'
            )

            with get_db() as conn:
                features_df, results_df = \
                    load_training_data(conn, start, end)

                race_count = features_df[
                    'race_id'
                ].nunique()
                logger.info(
                    f"Loaded {len(features_df)} samples "
                    f"across {race_count} races"
                )

                (dtrain, dval,
                 val_df, val_results,
                 tg, vg) = prepare_xgboost_data(
                    features_df, results_df
                )

                model = do_train(dtrain, dval)
                importance = get_feature_importance(model)
                metrics = evaluate_model(
                    model, val_df, results_df
                )
                metrics['race_count'] = race_count

                version_name = event.get(
                    'version_name',
                    f"v{date.today().strftime('%Y%m%d')}"
                )
                s3_path = save_model(
                    model=model,
                    metrics=metrics,
                    params=DEFAULT_PARAMS,
                    output_dir='/tmp/equine-model',
                    s3_bucket=s3_bucket,
                    version_name=version_name,
                )

                model_version_id = register_model(
                    conn=conn,
                    version_name=version_name,
                    metrics=metrics,
                    params=DEFAULT_PARAMS,
                    s3_path=s3_path,
                    training_race_count=race_count,
                    set_active=set_active,
                )

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'model_version_id': model_version_id,
                    'version_name': version_name,
                    'race_count': race_count,
                    'metrics': metrics,
                    's3_path': s3_path,
                })
            }
        except Exception as e:
            logger.error(
                f"Training failed: {e}",
                exc_info=True
            )
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

    # ── Activate model version action ──
    # Deactivates all other versions of same type and activates specified one.
    # Invoke: {"action": "activate_model", "model_version_id": "<uuid>"}
    if action == 'activate_model':
        model_version_id = event.get('model_version_id')
        if not model_version_id:
            return {'statusCode': 400, 'body': json.dumps({'error': 'model_version_id required'})}
        try:
            from repositories.model_version_repository import ModelVersionRepository
            with get_db() as conn:
                repo = ModelVersionRepository(conn)
                repo.set_active_model(model_version_id)
            return {'statusCode': 200, 'body': json.dumps({'activated': model_version_id})}
        except Exception as e:
            logger.error(f"Activate model failed: {e}", exc_info=True)
            return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

    # ── Parse charts action ──
    # Parse Equibase PDF charts from S3 into Aurora
    # Invoke: {"action": "parse_charts", "track": "GP"}
    # Or all tracks: {"action": "parse_charts"}
    if action == 'parse_charts':
        logger.info("Running chart parser")
        track = event.get('track')  # optional
        date_from = event.get('date_from')  # YYYYMMDD
        date_to = event.get('date_to')  # YYYYMMDD
        try:
            from services.chart_parser import run_from_s3
            with get_db() as conn:
                result = run_from_s3(
                    conn, track=track,
                    date_from=date_from, date_to=date_to
                )
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        except Exception as e:
            logger.error(
                f"Chart parser failed: {e}",
                exc_info=True
            )
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': str(e)
                })
            }

    # ── Test scrape action ──
    # Invoked manually to test the HRN scraper
    if action == 'test_scrape':
        logger.info("Running test scrape")
        test_date = event.get('date')
        if test_date:
            from datetime import date as date_type
            scrape_date = date_type.fromisoformat(
                test_date
            )
        else:
            scrape_date = date.today()

        with get_db() as conn:
            service = IngestionService(conn)
            summary = service.fetch_daily_entries(
                scrape_date
            )
        return {
            'statusCode': 200,
            'body': json.dumps(summary)
        }

    # ── Raw query action (diagnostic only) ──
    # Invoke: {"action": "raw_query", "sql": "SELECT ..."}
    if action == 'raw_query':
        sql = event.get('sql', '')
        if not sql or not sql.strip().upper().startswith('SELECT'):
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Only SELECT queries allowed'
                })
            }
        with get_db() as conn:
            from shared.db import execute_query
            rows = execute_query(conn, sql)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'rows': [dict(r) for r in rows],
                    'count': len(rows)
                }, default=str)
            }

    # ── DB counts action ──
    if action == 'db_counts':
        with get_db() as conn:
            from shared.db import execute_one
            row = execute_one(
                conn,
                """SELECT
                    (SELECT COUNT(*) FROM races) as races,
                    (SELECT COUNT(*) FROM past_performances) as past_performances,
                    (SELECT COUNT(*) FROM horses) as horses,
                    (SELECT COUNT(*) FROM jockeys) as jockeys,
                    (SELECT COUNT(*) FROM trainers) as trainers,
                    (SELECT COUNT(*) FROM entries) as entries,
                    (SELECT COUNT(*) FROM results) as results"""
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'races': row['races'],
                    'past_performances': row['past_performances'],
                    'horses': row['horses'],
                    'jockeys': row['jockeys'],
                    'trainers': row['trainers'],
                    'entries': row['entries'],
                    'results': row['results'],
                })
            }

    # ── Activate model action ──
    # Invoke: {"action": "set_active_model", "model_id": "uuid"}
    if action == 'set_active_model':
        model_id = event.get('model_id')
        if not model_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'model_id required'
                })
            }
        with get_db() as conn:
            from repositories.model_version_repository \
                import ModelVersionRepository
            repo = ModelVersionRepository(conn)
            repo.set_active_model(model_id)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'activated': model_id
                })
            }

    # ── Query dates action ──
    # Invoke: {"action": "query_dates"}
    if action == 'query_dates':
        with get_db() as conn:
            from shared.db import execute_query
            rows = execute_query(
                conn,
                """SELECT race_date, COUNT(*) as cnt
                   FROM races
                   GROUP BY race_date
                   ORDER BY race_date DESC
                   LIMIT 60"""
            )
            # Also get month-level summary
            months = execute_query(
                conn,
                """SELECT
                     TO_CHAR(race_date, 'YYYY-MM') as month,
                     COUNT(*) as race_count
                   FROM races
                   GROUP BY month
                   ORDER BY month DESC"""
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'recent_dates': [
                        {'date': str(r['race_date']), 'count': r['cnt']}
                        for r in rows
                    ],
                    'by_month': [
                        {'month': r['month'], 'count': r['race_count']}
                        for r in months
                    ]
                })
            }

    # ── Match results action ──
    # Invoke: {"action": "match_results"}
    if action == 'match_results':
        with get_db() as conn:
            from shared.db import execute_query, execute_one
            # Find all predictions that don't have results yet
            # but whose races DO have results in the results table
            updated = execute_one(
                conn,
                """WITH pred_results AS (
                     SELECT
                       p.prediction_id,
                       p.race_id,
                       p.horse_id,
                       p.predicted_rank,
                       p.entry_id,
                       r.official_finish as actual_finish,
                       r.official_finish = 1 as was_win,
                       r.official_finish <= 2 as was_place,
                       r.official_finish <= 3 as was_show
                     FROM predictions p
                     JOIN results r
                       ON p.entry_id = r.entry_id
                     WHERE p.actual_finish IS NULL
                       AND r.official_finish IS NOT NULL
                       AND r.official_finish > 0
                   )
                   UPDATE predictions pred
                   SET
                     actual_finish = pr.actual_finish,
                     was_win = pr.was_win,
                     was_place = pr.was_place,
                     was_show = pr.was_show
                   FROM pred_results pr
                   WHERE pred.prediction_id = pr.prediction_id
                   RETURNING pred.prediction_id"""
            )

            # Now compute exacta/trifecta hits per race
            # Exacta hit = model's top 2 are actual top 2 (any order)
            # Trifecta hit = model's top 3 are actual top 3 (any order)
            exacta_update = execute_query(
                conn,
                """WITH race_tops AS (
                     SELECT race_id,
                       ARRAY_AGG(horse_id ORDER BY predicted_rank) FILTER (WHERE predicted_rank <= 2) as model_top2,
                       ARRAY_AGG(horse_id ORDER BY actual_finish) FILTER (WHERE actual_finish <= 2 AND actual_finish > 0) as actual_top2,
                       ARRAY_AGG(horse_id ORDER BY predicted_rank) FILTER (WHERE predicted_rank <= 3) as model_top3,
                       ARRAY_AGG(horse_id ORDER BY actual_finish) FILTER (WHERE actual_finish <= 3 AND actual_finish > 0) as actual_top3
                     FROM predictions
                     WHERE actual_finish IS NOT NULL
                     GROUP BY race_id
                   )
                   UPDATE predictions p
                   SET
                     exacta_hit = (
                       rt.model_top2 IS NOT NULL AND rt.actual_top2 IS NOT NULL
                       AND ARRAY_LENGTH(rt.model_top2, 1) = 2
                       AND ARRAY_LENGTH(rt.actual_top2, 1) = 2
                       AND rt.model_top2 <@ rt.actual_top2
                       AND rt.actual_top2 <@ rt.model_top2
                     ),
                     trifecta_hit = (
                       rt.model_top3 IS NOT NULL AND rt.actual_top3 IS NOT NULL
                       AND ARRAY_LENGTH(rt.model_top3, 1) = 3
                       AND ARRAY_LENGTH(rt.actual_top3, 1) = 3
                       AND rt.model_top3 <@ rt.actual_top3
                       AND rt.actual_top3 <@ rt.model_top3
                     )
                   FROM race_tops rt
                   WHERE p.race_id = rt.race_id
                   RETURNING p.prediction_id"""
            )

            # Get summary
            summary = execute_one(
                conn,
                """SELECT
                     COUNT(*) FILTER (WHERE actual_finish IS NOT NULL) as matched,
                     COUNT(*) FILTER (WHERE was_win = true AND predicted_rank = 1) as top1_wins,
                     COUNT(DISTINCT race_id) FILTER (WHERE exacta_hit = true) as exacta_hits,
                     COUNT(DISTINCT race_id) FILTER (WHERE trifecta_hit = true) as trifecta_hits,
                     COUNT(DISTINCT race_id) FILTER (WHERE actual_finish IS NOT NULL) as races_with_results
                   FROM predictions"""
            )

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'predictions_matched': summary['matched'] if summary else 0,
                    'top1_wins': summary['top1_wins'] if summary else 0,
                    'exacta_hits': summary['exacta_hits'] if summary else 0,
                    'trifecta_hits': summary['trifecta_hits'] if summary else 0,
                    'races_with_results': summary['races_with_results'] if summary else 0,
                })
            }

    # ── Run inference batch action ──
    # Invoke: {"action": "run_inference_batch",
    #   "start_date": "2025-11-01", "end_date": "2026-03-15"}
    if action == 'run_inference_batch':
        start = event.get('start_date')
        end = event.get('end_date')
        if not start or not end:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'start_date and end_date required'
                })
            }
        import boto3
        lambda_client = boto3.client('lambda')

        # Find dates with races but no predictions
        with get_db() as conn:
            from shared.db import execute_query
            rows = execute_query(
                conn,
                """SELECT r.race_date, COUNT(*) as race_count
                   FROM races r
                   LEFT JOIN predictions p
                     ON r.race_id = p.race_id
                   WHERE r.race_date BETWEEN %s AND %s
                     AND p.prediction_id IS NULL
                   GROUP BY r.race_date
                   ORDER BY r.race_date""",
                (start, end)
            )

        dates_to_run = [
            str(r['race_date']) for r in rows
        ]

        # Invoke inference Lambda async for each date
        invoked = 0
        errors = []
        for d in dates_to_run:
            try:
                lambda_client.invoke(
                    FunctionName='equine-inference',
                    InvocationType='Event',
                    Payload=json.dumps({
                        'source': 'batch',
                        'date': d
                    }).encode()
                )
                invoked += 1
            except Exception as e:
                errors.append(f"{d}: {str(e)[:80]}")
                logger.error(
                    f"Failed to invoke for {d}: {e}"
                )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'dates_found': len(dates_to_run),
                'invocations_sent': invoked,
                'dates': dates_to_run[:20],
            'errors': errors[:5],
            })
        }

    # ── Deduplicate horses action ──
    # Invoke: {"action": "dedup_horses"}
    if action == 'dedup_horses':
        with get_db() as conn:
            from shared.db import execute_query, execute_one
            # Find duplicate pairs: pick the one with MORE
            # PPs as canonical (usually PDF-parsed version)
            dupes = execute_query(
                conn,
                """WITH normalized AS (
                     SELECT horse_id, horse_name,
                       LOWER(REPLACE(REPLACE(
                         horse_name, ' ', ''), '''', ''
                       )) as norm_name,
                       (SELECT COUNT(*) FROM past_performances
                        WHERE horse_id = h.horse_id) as pp_count
                     FROM horses h
                   ),
                   pairs AS (
                     SELECT
                       n1.horse_id as id1, n1.horse_name as name1,
                         n1.pp_count as pp1,
                       n2.horse_id as id2, n2.horse_name as name2,
                         n2.pp_count as pp2
                     FROM normalized n1
                     JOIN normalized n2
                       ON n1.norm_name = n2.norm_name
                       AND n1.horse_id < n2.horse_id
                   )
                   SELECT
                     CASE WHEN pp1 >= pp2
                       THEN id1 ELSE id2 END as keep_id,
                     CASE WHEN pp1 >= pp2
                       THEN name1 ELSE name2 END as keep_name,
                     CASE WHEN pp1 >= pp2
                       THEN pp1 ELSE pp2 END as keep_pps,
                     CASE WHEN pp1 >= pp2
                       THEN id2 ELSE id1 END as dupe_id,
                     CASE WHEN pp1 >= pp2
                       THEN name2 ELSE name1 END as dupe_name,
                     CASE WHEN pp1 >= pp2
                       THEN pp2 ELSE pp1 END as dupe_pps
                   FROM pairs
                   ORDER BY keep_name"""
            )

            merged = 0
            merge_errors = []
            for d in dupes:
                keep = d['keep_id']
                dupe = d['dupe_id']
                cur = conn.cursor()
                try:
                    cur.execute("SAVEPOINT dedup_sp")

                    # Step 1: Delete conflicting entries
                    # where BOTH versions have an entry
                    # in the same race — delete the dupe's
                    cur.execute(
                        """DELETE FROM predictions
                           WHERE entry_id IN (
                             SELECT e_dupe.entry_id
                             FROM entries e_dupe
                             JOIN entries e_keep
                               ON e_dupe.race_id = e_keep.race_id
                             WHERE e_dupe.horse_id = %s
                               AND e_keep.horse_id = %s
                           )""",
                        (dupe, keep)
                    )
                    cur.execute(
                        """DELETE FROM results
                           WHERE entry_id IN (
                             SELECT e_dupe.entry_id
                             FROM entries e_dupe
                             JOIN entries e_keep
                               ON e_dupe.race_id = e_keep.race_id
                             WHERE e_dupe.horse_id = %s
                               AND e_keep.horse_id = %s
                           )""",
                        (dupe, keep)
                    )
                    cur.execute(
                        """DELETE FROM entries
                           WHERE horse_id = %s
                             AND race_id IN (
                               SELECT race_id FROM entries
                               WHERE horse_id = %s
                             )""",
                        (dupe, keep)
                    )

                    # Step 2: Delete conflicting PPs
                    cur.execute(
                        """DELETE FROM past_performances
                           WHERE horse_id = %s
                             AND (race_date, track_code,
                                  race_number) IN (
                               SELECT race_date, track_code,
                                      race_number
                               FROM past_performances
                               WHERE horse_id = %s
                             )""",
                        (dupe, keep)
                    )

                    # Step 3: Transfer remaining references
                    for tbl, col in [
                        ('past_performances', 'horse_id'),
                        ('entries', 'horse_id'),
                        ('predictions', 'horse_id'),
                        ('results', 'horse_id'),
                        ('workouts', 'horse_id'),
                    ]:
                        cur.execute(
                            f"UPDATE {tbl} SET {col} = %s"
                            f" WHERE {col} = %s",
                            (keep, dupe)
                        )

                    for col in [
                        'sire_id', 'dam_id', 'dam_sire_id'
                    ]:
                        cur.execute(
                            f"UPDATE horses SET {col} = %s"
                            f" WHERE {col} = %s",
                            (keep, dupe)
                        )

                    # Step 4: Delete duplicate horse
                    cur.execute(
                        "DELETE FROM horses"
                        " WHERE horse_id = %s",
                        (dupe,)
                    )
                    cur.execute("RELEASE SAVEPOINT dedup_sp")
                    merged += 1
                except Exception as e:
                    merge_errors.append(
                        f"{d['dupe_name']}: {str(e)[:80]}"
                    )
                    try:
                        cur.execute(
                            "ROLLBACK TO SAVEPOINT dedup_sp"
                        )
                    except Exception:
                        pass

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'duplicates_found': len(dupes),
                    'merged': merged,
                    'sample': [
                        {
                            'keep': f"{d['keep_name']} ({d['keep_pps']}pp)",
                            'removed': f"{d['dupe_name']} ({d['dupe_pps']}pp)"
                        }
                        for d in dupes[:10]
                    ],
                    'errors': merge_errors[:5],
                })
            }

    # ── Backfill workouts action ──
    # Fetches workout history from HRN horse profile pages for all
    # horses that have past_performances but no workouts yet.
    #
    # Run in batches (always offset=0 for sequential use):
    #   {"action": "backfill_workouts", "limit": 50}
    # Repeat until horses_processed == 0 (all done).
    #
    # The NOT EXISTS filter means horses drop out of the eligible set
    # as workouts are inserted, so offset=0 always gets the next batch.
    # Use offset only when you need to parallelize manually.
    if action == 'backfill_workouts':
        offset = int(event.get('offset', 0))
        limit = int(event.get('limit', 100))
        cutoff_str = event.get('cutoff_start', '2022-01-01')
        from datetime import date as date_type
        cutoff_start = date_type.fromisoformat(cutoff_str)

        try:
            from services.data_sources.hrn_workout_scraper import (
                HRNWorkoutScraper
            )
            from repositories.workout_repository import WorkoutRepository
            from shared.db import execute_query

            with get_db() as conn:
                # Horses with PP data but no workouts at all
                horses = execute_query(
                    conn,
                    """SELECT DISTINCT h.horse_id, h.horse_name
                       FROM horses h
                       JOIN past_performances pp
                         USING (horse_id)
                       WHERE NOT EXISTS (
                           SELECT 1 FROM workouts w
                           WHERE w.horse_id = h.horse_id
                       )
                       ORDER BY h.horse_name
                       OFFSET %s LIMIT %s""",
                    (offset, limit),
                )

                scraper = HRNWorkoutScraper()
                repo = WorkoutRepository(conn)

                total_inserted = 0
                horses_with_data = 0
                horses_no_data = 0
                errors = []

                for horse in horses:
                    try:
                        workouts = scraper.fetch_workouts(
                            horse_id=horse['horse_id'],
                            horse_name=horse['horse_name'],
                            cutoff_start=cutoff_start,
                        )
                        if workouts:
                            count = repo.bulk_insert_workouts(workouts)
                            total_inserted += count
                            horses_with_data += 1
                            logger.info(
                                f"Workouts: {horse['horse_name']} "
                                f"→ {count} inserted"
                            )
                        else:
                            horses_no_data += 1
                    except Exception as e:
                        err = (
                            f"{horse['horse_name']}: "
                            f"{str(e)[:80]}"
                        )
                        errors.append(err)
                        logger.error(
                            f"Workout backfill failed "
                            f"for {horse['horse_name']}: {e}"
                        )

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'offset': offset,
                    'limit': limit,
                    'cutoff_start': cutoff_str,
                    'horses_processed': len(horses),
                    'horses_with_workouts': horses_with_data,
                    'horses_no_workouts_found': horses_no_data,
                    'workouts_inserted': total_inserted,
                    'errors': errors[:10],
                }),
            }
        except Exception as e:
            logger.error(
                f"Backfill workouts failed: {e}",
                exc_info=True,
            )
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)}),
            }

    # ── Compute speed figures action ──
    # Full pipeline: par times → condition adj → pace figures →
    # track variants → normalize to Beyer scale.
    # Pure-SQL implementation — no chunked Python loops.
    # Invoke: {"action": "compute_speed_figures"}
    if action == 'compute_speed_figures':
        from shared.db import execute_query, execute_one

        # Step 1: Schema — quick DDL in its own transaction
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    ALTER TABLE past_performances
                    ADD COLUMN IF NOT EXISTS computed_speed_figure
                        DECIMAL(5,1),
                    ADD COLUMN IF NOT EXISTS speed_rating_raw
                        DECIMAL(5,1)
                """)
            conn.commit()
        logger.info("Schema ready")

        # Steps 2-6: All data work in one transaction.
        # LOCK TABLE before any writes — serializes with concurrent
        # chart parsing inserts so we wait rather than deadlock.
        # lock_timeout = 5 min (chart parser max runtime).
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("SET lock_timeout = '300s'")
                cur.execute(
                    "LOCK TABLE past_performances IN EXCLUSIVE MODE"
                )
            logger.info("Exclusive lock acquired")

            # Step 2+3: Compute speed_rating_raw + pace figures
            # in a single bulk UPDATE ... FROM using inline CTE
            # for par times. Aurora handles all the row iteration.
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE past_performances pp
                    SET
                      speed_rating_raw = GREATEST(-50.0, LEAST(50.0,
                        (par.par_time
                         -- condition adjustment (seconds)
                         - (pp.final_time - CASE COALESCE(pp.track_condition,'fast')
                             WHEN 'fast'          THEN 0.0
                             WHEN 'fast(sealed)'  THEN 0.0
                             WHEN 'good'          THEN 2.0/5.0
                             WHEN 'good(sealed)'  THEN 3.0/5.0
                             WHEN 'sloppy'        THEN 1.0/5.0
                             WHEN 'sloppy(sealed)'THEN 1.5/5.0
                             WHEN 'muddy'         THEN 5.0/5.0
                             WHEN 'muddy(sealed)' THEN 3.0/5.0
                             WHEN 'wetfast'       THEN 0.5/5.0
                             WHEN 'wetfast(sealed)'THEN 1.0/5.0
                             WHEN 'heavy'         THEN 8.0/5.0
                             WHEN 'frozen'        THEN 3.0/5.0
                             WHEN 'firm'          THEN 0.0
                             WHEN 'yielding'      THEN 5.0/5.0
                             WHEN 'soft'          THEN 7.0/5.0
                             ELSE 0.0 END
                           -- lengths-behind adj for non-winners
                           + CASE WHEN pp.finish_position > 1
                                       AND COALESCE(pp.lengths_behind,0) > 0
                                  THEN COALESCE(pp.lengths_behind,0) * 0.2
                                  ELSE 0.0 END
                         )
                        ) * 5.0
                      )),

                      early_pace_figure = CASE
                        WHEN pp.fraction_1 IS NOT NULL
                             AND pp.call_1_lengths IS NOT NULL
                        THEN ROUND((pp.fraction_1
                                    + pp.call_1_lengths / 5.0)::numeric, 2)
                        ELSE NULL END,

                      late_pace_figure = CASE
                        WHEN pp.fraction_2 IS NOT NULL
                             AND pp.call_2_lengths IS NOT NULL
                        THEN ROUND((
                               pp.final_time
                               + COALESCE(pp.lengths_behind,0) / 5.0
                               - (pp.fraction_2 + pp.call_2_lengths / 5.0)
                             )::numeric, 2)
                        ELSE NULL END,

                      pace_delta = CASE
                        WHEN pp.fraction_1 IS NOT NULL
                             AND pp.call_1_lengths IS NOT NULL
                             AND pp.fraction_2 IS NOT NULL
                             AND pp.call_2_lengths IS NOT NULL
                        THEN ROUND((
                               -- late_pace - early_pace
                               (pp.final_time
                                + COALESCE(pp.lengths_behind,0) / 5.0
                                - (pp.fraction_2 + pp.call_2_lengths / 5.0))
                               - (pp.fraction_1 + pp.call_1_lengths / 5.0)
                             )::numeric, 2)
                        ELSE NULL END

                    FROM (
                        SELECT track_code, distance_furlongs, surface,
                               PERCENTILE_CONT(0.5) WITHIN GROUP
                                 (ORDER BY final_time) AS par_time
                        FROM past_performances
                        WHERE finish_position = 1
                          AND final_time > 0 AND final_time < 200
                          AND distance_furlongs BETWEEN 3.5 AND 12.0
                          AND surface IS NOT NULL
                          AND track_condition IN (
                              'fast','fast(sealed)','firm','wetfast')
                        GROUP BY track_code, distance_furlongs, surface
                        HAVING COUNT(*) >= 5
                    ) par
                    WHERE pp.track_code = par.track_code
                      AND pp.distance_furlongs = par.distance_furlongs
                      AND pp.surface = par.surface
                      AND pp.final_time > 0
                      AND pp.final_time < 200
                      AND pp.finish_position IS NOT NULL
                      AND pp.finish_position < 90
                      AND pp.distance_furlongs IS NOT NULL
                      AND pp.surface IS NOT NULL
                """)
                updated = cur.rowcount
            logger.info(f"Speed ratings + pace figures updated: {updated:,}")

            # Step 4+5: Apply daily track variants in one pass.
            # Rows with no variant (< 3 winners that day) get variant = 0.
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE past_performances pp
                    SET track_variant         = ROUND(v.variant::numeric, 1),
                        computed_speed_figure = ROUND(
                          (pp.speed_rating_raw - v.variant)::numeric, 2)
                    FROM (
                        SELECT track_code, race_date, surface,
                               AVG(speed_rating_raw) AS variant
                        FROM past_performances
                        WHERE finish_position = 1
                          AND speed_rating_raw IS NOT NULL
                        GROUP BY track_code, race_date, surface
                        HAVING COUNT(*) >= 3
                    ) v
                    WHERE pp.track_code = v.track_code
                      AND pp.race_date  = v.race_date
                      AND pp.surface    = v.surface
                      AND pp.speed_rating_raw IS NOT NULL
                """)
                with_variant = cur.rowcount

            # Rows without a qualifying variant: computed = raw, variant = 0
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE past_performances
                    SET track_variant         = 0,
                        computed_speed_figure = ROUND(
                          speed_rating_raw::numeric, 2)
                    WHERE speed_rating_raw IS NOT NULL
                      AND computed_speed_figure IS NULL
                """)
                no_variant = cur.rowcount
            logger.info(
                f"Variants applied: {with_variant:,} with variant, "
                f"{no_variant:,} at zero"
            )

            # Step 6: Diagnostics — inspect pre-norm distributions
            raw_stats = execute_one(conn, """
                SELECT
                  AVG(speed_rating_raw)::float  as mean,
                  PERCENTILE_CONT(0.5) WITHIN GROUP
                    (ORDER BY speed_rating_raw)::float as median,
                  STDDEV(speed_rating_raw)::float as std,
                  MIN(speed_rating_raw)::float  as min_val,
                  MAX(speed_rating_raw)::float  as max_val,
                  COUNT(*) as cnt
                FROM past_performances
                WHERE speed_rating_raw IS NOT NULL
            """)
            logger.info(
                f"speed_rating_raw: mean={raw_stats['mean']:.2f} "
                f"median={raw_stats['median']:.2f} "
                f"std={raw_stats['std']:.2f} "
                f"min={raw_stats['min_val']:.2f} "
                f"max={raw_stats['max_val']:.2f} "
                f"n={int(raw_stats['cnt']):,}"
            )

            # Get median/std of computed_speed_figure (pre-norm adjusted vals)
            norm_stats = execute_one(conn, """
                SELECT
                  AVG(computed_speed_figure)::float as mean,
                  PERCENTILE_CONT(0.5) WITHIN GROUP
                    (ORDER BY computed_speed_figure)::float as median,
                  STDDEV(computed_speed_figure)::float as std,
                  MIN(computed_speed_figure)::float as min_val,
                  MAX(computed_speed_figure)::float as max_val,
                  COUNT(*) as cnt
                FROM past_performances
                WHERE computed_speed_figure IS NOT NULL
            """)
            median_fig = float(norm_stats['median'])
            std_fig = float(norm_stats['std'])
            logger.info(
                f"pre-norm computed_speed_figure: "
                f"mean={norm_stats['mean']:.2f} "
                f"median={median_fig:.2f} std={std_fig:.2f} "
                f"min={norm_stats['min_val']:.2f} "
                f"max={norm_stats['max_val']:.2f} "
                f"n={int(norm_stats['cnt']):,}"
            )

            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE past_performances
                    SET computed_speed_figure = ROUND(
                      LEAST(130, GREATEST(0,
                        (computed_speed_figure - %s) / %s
                        * 12 + 80
                      ))::numeric, 1
                    )
                    WHERE computed_speed_figure IS NOT NULL
                """, (median_fig, std_fig))
            # get_db() context manager commits all writes at exit

            # Validation
            result = execute_one(conn, """
                SELECT
                  AVG(computed_speed_figure)::float  as avg_fig,
                  MAX(computed_speed_figure)::float  as max_fig,
                  MIN(computed_speed_figure)::float  as min_fig,
                  COUNT(early_pace_figure)           as has_early_pace,
                  COUNT(late_pace_figure)            as has_late_pace
                FROM past_performances
            """)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'pre_norm': {
                        'raw_mean': round(float(raw_stats['mean']), 2),
                        'raw_median': round(float(raw_stats['median']), 2),
                        'raw_std': round(float(raw_stats['std']), 2),
                        'adj_median': round(median_fig, 2),
                        'adj_std': round(std_fig, 2),
                    },
                    'validation': {
                        'avg_fig': round(float(result['avg_fig']), 2),
                        'max_fig': round(float(result['max_fig']), 2),
                        'min_fig': round(float(result['min_fig']), 2),
                        'has_early_pace': int(result['has_early_pace']),
                        'has_late_pace': int(result['has_late_pace']),
                    },
                    'rows_with_speed_rating': int(raw_stats['cnt']),
                }, default=str)
            }

    # ── Normalize speed figures action ──
    if action == 'normalize_figures':
        with get_db() as conn:
            from shared.db import execute_one
            # Get distribution stats
            stats = execute_one(
                conn,
                """SELECT
                     PERCENTILE_CONT(0.5) WITHIN GROUP
                       (ORDER BY computed_speed_figure)
                       as median_fig,
                     STDDEV(computed_speed_figure) as std_fig
                   FROM past_performances
                   WHERE computed_speed_figure IS NOT NULL"""
            )
            median_fig = float(stats['median_fig'])
            std_fig = float(stats['std_fig'])

            # Normalize: median→80, std→12 points
            with conn.cursor() as cur:
                cur.execute(
                    """UPDATE past_performances
                       SET computed_speed_figure = ROUND(
                         LEAST(130, GREATEST(0,
                           (computed_speed_figure - %s) / %s
                           * 12 + 80
                         ))::numeric, 1
                       )
                       WHERE computed_speed_figure
                         IS NOT NULL""",
                    (median_fig, std_fig)
                )
            conn.commit()

            # Validate
            result = execute_one(
                conn,
                """SELECT
                     ROUND(AVG(computed_speed_figure)::numeric, 1)
                       as avg_fig,
                     ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP
                       (ORDER BY computed_speed_figure)::numeric, 1)
                       as median_fig,
                     ROUND(MIN(computed_speed_figure)::numeric, 1)
                       as min_fig,
                     ROUND(MAX(computed_speed_figure)::numeric, 1)
                       as max_fig,
                     COUNT(*) as count
                   FROM past_performances
                   WHERE computed_speed_figure IS NOT NULL"""
            )

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'pre_norm_median': median_fig,
                    'pre_norm_std': std_fig,
                    'post_norm': dict(result),
                }, default=str)
            }

    # ── Health check action ──
    # ── Trip flag extraction ──
    # Invoke: {"action": "backfill_trip_flags"}
    # Step 1: DDL (add columns if not exist)
    # Step 2: Pure-SQL UPDATE with regex flag extraction
    # Step 3: Return verification counts
    if action == 'backfill_trip_flags':
        with get_db() as conn:
            with conn.cursor() as cur:
                # Step 1 — DDL
                logger.info("Adding trip flag columns if not exist")
                cur.execute("""
                    ALTER TABLE past_performances
                    ADD COLUMN IF NOT EXISTS trip_troubled    BOOLEAN DEFAULT FALSE,
                    ADD COLUMN IF NOT EXISTS trip_pace_setter BOOLEAN DEFAULT FALSE,
                    ADD COLUMN IF NOT EXISTS trip_faded       BOOLEAN DEFAULT FALSE,
                    ADD COLUMN IF NOT EXISTS trip_late_rally  BOOLEAN DEFAULT FALSE,
                    ADD COLUMN IF NOT EXISTS trip_no_factor   BOOLEAN DEFAULT FALSE,
                    ADD COLUMN IF NOT EXISTS trip_gate_issue  BOOLEAN DEFAULT FALSE,
                    ADD COLUMN IF NOT EXISTS wide_path        INTEGER DEFAULT 0
                """)
            conn.commit()

            # Step 2 — Pure-SQL backfill
            # All pattern matching on lowercased comment, no Python row loop
            logger.info("Backfilling trip flags via pure SQL")
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE past_performances SET
                        trip_troubled = (
                            lower(comment) ~ 'bumped|steadied|checked|blocked|troubledtrip|stopped|joggedin'
                        ),
                        trip_pace_setter = (
                            lower(comment) ~ 'pace|^led|,led|vied|dueled|promptedwinner|pressedwinner|briefspeed|pressedpace|promptedpace'
                        ),
                        trip_faded = (
                            lower(comment) ~ 'tired|weakened|faded|doneearly|throughafterhalf|finishedearly|weakenedwhenheaded|flattened|gaveway|gavewaywhenheaded|retreated|steadyretreat|falteredwhenheaded|wkndlate|weakenedlate|(^|,)empty|foldedup|steadyfade'
                        ),
                        trip_late_rally = (
                            lower(comment) ~ 'rallied|closed|passedtiring|finishedwell|gamely|railrally|mildrallyoutside|mildrally|ranon|kepton|mildkick'
                        ),
                        trip_no_factor = (
                            lower(comment) ~ 'nofactor|nomenace|failedtomenace|outrun|neverinvolved|neverathreat|nothreat|norally|remainedback|trailedinside|trailedthroughout|noavail|noimpact|noresponse|norealthreat|neverafactor|showedlittle|noclosingbid|pulledup|walkedoff|vannedoff|finishedafterhalf|failedtorespond|lackedrally'
                        ),
                        trip_gate_issue = (
                            lower(comment) ~ 'brokeslow|slowstart|stumbled|missedbreak|dwelt|offstepslow|offslow|offbitslow|offslowly|reluctantloading|brokethroughgate|headturnedstart|stepslow'
                        ),
                        wide_path = LEAST(8, COALESCE(
                            (SELECT MAX(m[1]::int)
                             FROM regexp_matches(lower(comment), '(\\d+)(?:-\\d+)?w[d]?', 'g') AS m),
                            0
                        ))
                    WHERE comment IS NOT NULL
                """)
                updated = cur.rowcount
            conn.commit()
            logger.info(f"Trip flags updated for {updated} rows")

            # Step 3 — Verification counts
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        COUNT(*)                   as total_rows,
                        SUM(trip_troubled::int)    as troubled,
                        SUM(trip_pace_setter::int) as pace_setter,
                        SUM(trip_faded::int)       as faded,
                        SUM(trip_late_rally::int)  as late_rally,
                        SUM(trip_no_factor::int)   as no_factor,
                        SUM(trip_gate_issue::int)  as gate_issue,
                        SUM(CASE WHEN wide_path > 0 THEN 1 ELSE 0 END) as wide_nonzero,
                        ROUND(AVG(wide_path)::numeric, 2)::float as avg_wide
                    FROM past_performances
                """)
                stats = dict(cur.fetchone())

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'rows_updated': updated,
                    'distribution': stats
                })
            }

    # ── Load workouts from S3 JSON ──
    # Reads a JSON file uploaded by collect_daily_workouts.py --s3-json
    # Invoke: {"action": "load_workouts_from_s3", "s3_key": "workout-loads/...json"}
    if action == 'load_workouts_from_s3':
        import boto3
        from datetime import date as _date
        from repositories.horse_repository import HorseRepository
        from repositories.workout_repository import WorkoutRepository

        s3_key    = event.get('s3_key')
        s3_bucket = event.get('s3_bucket') or os.environ.get('RAW_DATA_BUCKET')

        if not s3_key:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 's3_key is required'})
            }
        if not s3_bucket:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'RAW_DATA_BUCKET env var or s3_bucket param required'})
            }

        try:
            s3 = boto3.client('s3')
            obj = s3.get_object(Bucket=s3_bucket, Key=s3_key)
            workout_rows = json.loads(obj['Body'].read().decode('utf-8'))
        except Exception as e:
            logger.error(f"Failed to read s3://{s3_bucket}/{s3_key}: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f'S3 read failed: {str(e)}'})
            }

        logger.info(
            f"load_workouts_from_s3: {len(workout_rows)} rows "
            f"from s3://{s3_bucket}/{s3_key}"
        )

        inserted  = 0
        skipped   = 0
        errors    = 0

        try:
            with get_db() as conn:
                horse_repo   = HorseRepository(conn)
                workout_repo = WorkoutRepository(conn)

                from shared.horse_naming import normalize_horse_name
                for row in workout_rows:
                    horse_name = normalize_horse_name(row.get('horse_name', ''))
                    eq_refno   = row.get('eq_refno')
                    sex        = row.get('sex')

                    if not horse_name:
                        skipped += 1
                        continue

                    # Resolve horse_id — refno first, then name, then create
                    horse_id = None
                    if eq_refno:
                        h = horse_repo.get_horse_by_registration(str(eq_refno))
                        if h:
                            horse_id = str(h.horse_id)
                    if not horse_id:
                        h = horse_repo.get_horse_by_name(horse_name)
                        if h:
                            horse_id = str(h.horse_id)
                    if not horse_id:
                        horse_id = horse_repo.upsert_horse({
                            'registration_id': eq_refno,
                            'horse_name':      horse_name,
                            'sex':             sex,
                        })

                    workout_date = row.get('workout_date')
                    if isinstance(workout_date, str):
                        workout_date = _date.fromisoformat(workout_date)

                    try:
                        workout_repo.insert_workout({
                            'horse_id':           horse_id,
                            'workout_date':       workout_date,
                            'track_code':         row.get('track_code'),
                            'distance_furlongs':  row.get('distance_furlongs'),
                            'workout_time':       row.get('workout_time'),
                            'is_bullet':          row.get('is_bullet', False),
                            'track_condition':    row.get('track_condition'),
                            'workout_type':       row.get('workout_type'),
                            'rank_on_day':        row.get('rank_on_day'),
                            'total_works_on_day': row.get('total_works_on_day'),
                            'exercise_rider':     None,
                        })
                        inserted += 1
                    except Exception as e:
                        logger.warning(
                            f"Insert failed for {horse_name} "
                            f"{workout_date}: {e}"
                        )
                        errors += 1

        except Exception as e:
            logger.error(f"load_workouts_from_s3 DB error: {e}", exc_info=True)
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

        logger.info(
            f"load_workouts_from_s3 complete: "
            f"inserted={inserted} skipped={skipped} errors={errors}"
        )
        return {
            'statusCode': 200,
            'body': json.dumps({
                'inserted': inserted,
                'skipped':  skipped,
                'errors':   errors,
                'source':   f's3://{s3_bucket}/{s3_key}',
            })
        }

    if action == 'health':
        with get_db() as conn:
            from shared.db import execute_one
            result = execute_one(
                conn, 'SELECT NOW() as t'
            )
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'status': 'ok',
                    'db_time': str(result['t'])
                })
            }

    # ── Normal scheduled ingestion ──
    logger.info(
        f"Daily ingestion triggered for {date.today()}"
    )
    try:
        with get_db() as conn:
            service = IngestionService(conn)
            service.fetch_daily_entries(date.today())
        return {
            'statusCode': 200,
            'body': 'Ingestion complete'
        }
    except Exception as e:
        logger.error(
            f"Ingestion failed: {e}",
            exc_info=True
        )
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
