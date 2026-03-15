import logging
from datetime import date
from models.canonical import Result, Prediction

logger = logging.getLogger(__name__)


class EvaluationService:
    """
    Records race results and evaluates model performance.

    Runs nightly after races complete.

    Responsibilities:
    - Pull actual results from data source
    - Match results to predictions
    - Calculate hit rates (exacta, trifecta, win)
    - Calculate exotic EV (expected value)
    - Update model performance metrics
    - Flag if model needs retraining
    """

    def __init__(self, conn):
        self.conn = conn

    def record_results(
        self, race_date: date
    ) -> dict:
        """
        Match actual results to predictions
        for a given race date.
        Updates prediction result fields.
        Called nightly by results Lambda.
        """
        from repositories.result_repository import (
            ResultRepository
        )
        from repositories.prediction_repository import (
            PredictionRepository
        )
        from repositories.race_repository import (
            RaceRepository
        )

        result_repo = ResultRepository(self.conn)
        pred_repo = PredictionRepository(self.conn)
        race_repo = RaceRepository(self.conn)

        races = race_repo.get_qualifying_races_by_date(
            race_date
        )

        updated = 0
        for race in races:
            results = result_repo.get_results_by_race(
                race.race_id
            )
            predictions = pred_repo \
                .get_predictions_by_race(race.race_id)

            if not results or not predictions:
                continue

            # Build result lookup by horse_id
            result_by_horse = {
                r.horse_id: r for r in results
            }

            # Build top 2 and top 3 actual finishers
            sorted_results = sorted(
                results,
                key=lambda r: r.official_finish
            )
            actual_top2 = {
                r.horse_id
                for r in sorted_results[:2]
            }
            actual_top3 = {
                r.horse_id
                for r in sorted_results[:3]
            }

            # Get top 2 and top 3 predicted
            sorted_preds = sorted(
                predictions,
                key=lambda p: p.predicted_rank or 99
            )
            predicted_top2 = {
                p.horse_id
                for p in sorted_preds[:2]
            }
            predicted_top3 = {
                p.horse_id
                for p in sorted_preds[:3]
            }
            exacta_hit = predicted_top2 == actual_top2
            trifecta_hit = predicted_top3 == actual_top3

            for pred in predictions:
                result = result_by_horse.get(
                    pred.horse_id
                )
                if not result:
                    continue

                actual_finish = result.official_finish
                pred_repo.update_prediction_result(
                    prediction_id=pred.prediction_id,
                    actual_finish=actual_finish,
                    was_win=(actual_finish == 1),
                    was_place=(actual_finish <= 2),
                    was_show=(actual_finish <= 3),
                    exacta_hit=exacta_hit,
                    trifecta_hit=trifecta_hit
                )
                updated += 1

        logger.info(
            f"Results recorded for {race_date}: "
            f"{updated} predictions updated"
        )
        return {
            'date': str(race_date),
            'predictions_updated': updated
        }

    def calculate_exacta_hit_rate(
        self, model_version_id: str
    ) -> float:
        """
        What % of races did our top 2 horses
        cover the actual exacta?

        TODO: Implement in evaluation session.
        """
        pass

    def calculate_trifecta_hit_rate(
        self, model_version_id: str
    ) -> float:
        """
        What % of races did our top 3 horses
        cover the actual trifecta?

        TODO: Implement in evaluation session.
        """
        pass

    def calculate_exotic_ev(
        self,
        predictions: list[Prediction],
        results: list[Result]
    ) -> float:
        """
        Expected value of recommended exotic bets.

        EV = (probability of hit * payout) - ticket_cost

        This is the P&L metric that matters.
        Not win rate. Not accuracy.

        TODO: Implement in evaluation session.
        """
        pass

    def should_retrain(
        self, model_version_id: str
    ) -> bool:
        """
        Check if model performance has degraded
        enough to trigger retraining.

        Criteria (TBD based on initial performance):
        - Exacta hit rate dropped below threshold
        - Trifecta hit rate dropped below threshold
        - EV trending negative over last 30 days

        TODO: Implement after first model trained.
        """
        pass
