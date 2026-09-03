from app.schemas.simulation import SimulationRequest
from app.services.data import race_data_service
from app.services.predictor import predictor


DRY_COMPOUNDS = {"SOFT", "MEDIUM", "HARD"}


def get_override_laps_until_pit(request: SimulationRequest) -> int | None:
    if request.red_flag_active or request.safety_car_active:
        return 0

    if request.vsc_active:
        return 1

    if (
        request.compound in DRY_COMPOUNDS
        and request.rain_condition in {"light_rain", "heavy_rain"}
    ):
        return 1

    return None



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

        total_laps = int(race_state["total_laps"])
        if request.lap_number > total_laps:
            raise ValueError(
                f"Lap {request.lap_number} is beyond the {total_laps}-lap race."
            )

        features = race_state.copy()

        features["position"] = request.position
        features["compound"] = request.compound
        features["tyre_age"] = request.tyre_age
        features["fresh_tyre"] = int(request.fresh_tyre)
        features["lap_number"] = request.lap_number

        rainfall_by_condition = {
            "": 0,
            "light_rain": 0.5,
            "heavy_rain": 1,
        }
        features["rainfall"] = rainfall_by_condition[request.rain_condition]

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

        override_laps_until_pit = get_override_laps_until_pit(request)
        prediction = (
            override_laps_until_pit
            if override_laps_until_pit is not None
            else round(predictor.predict(features))
        )

        remaining_laps = total_laps - request.lap_number
        laps_until_pit = min(max(0, prediction), remaining_laps)
        predicted_pit_lap = request.lap_number + laps_until_pit
        should_pit = predicted_pit_lap < total_laps

        return {
            "race": request.race,
            "driver": request.driver,
            "current_lap": request.lap_number,
            "laps_until_pit": laps_until_pit,
            "predicted_pit_lap": predicted_pit_lap,
            "total_laps": total_laps,
            "should_pit": should_pit,
            "pit_before_finish": should_pit,
        }


simulation_service = SimulationService()