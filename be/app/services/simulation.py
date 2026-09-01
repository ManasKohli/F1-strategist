from app.schemas.simulation import SimulationRequest
from app.services.data import race_data_service
from app.services.predictor import predictor



class SimulationService:

    def run_simulation(
        self,
        request: SimulationRequest
    ) -> dict:

        race_state = race_data_service.get_race_state(
            race=request.race,
            driver=request.driver,
            lap_number=request.lap_number,
        )

        features = race_state.copy()

        features["position"] = request.position
        features["compound"] = request.compound
        features["tyre_age"] = request.tyre_age
        features["fresh_tyre"] = int(request.fresh_tyre)

        features["safety_car_active"] = int(
            request.safety_car_active
        )

        features["vsc_active"] = int(
            request.vsc_active
        )

        features["yellow_flag"] = int(
            request.yellow_flag
        )

        features["red_flag_active"] = int(
            request.red_flag_active
        )

        features.pop("laps_until_pit", None)
        features.pop("next_pit_lap", None)
        features.pop("pit_lap", None)

        prediction = predictor.predict(
            features
        ).rounnd()

        predicted_pit_lap = (
            request.lap_number + prediction
        )

        return {
            "race": request.race,
            "driver": request.driver,
            "current_lap": request.lap_number,
            "laps_until_pit": prediction,
            "predicted_pit_lap": predicted_pit_lap,
        }


simulation_service = SimulationService()