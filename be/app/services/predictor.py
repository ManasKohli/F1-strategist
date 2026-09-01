from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "trained_models"
    / "pit_strategy_model.joblib"
)



MODEL_COLUMNS = [
    "race",
    "lap_number",
    "total_laps",
    "laps_remaining",
    "race_progress",
    "driver",
    "team",
    "position",
    "stint",
    "stint_laps",
    "pit_stop_count",
    "compound",
    "tyre_age",
    "fresh_tyre",
    "lap_time_seconds",
    "previous_lap_time",
    "avg_lap_time_3",
    "avg_lap_time_5",
    "avg_lap_time_10",
    "lap_time_delta_3",
    "lap_time_delta_5",
    "pace_trend_5",
    "air_temperature",
    "track_temperature",
    "humidity",
    "pressure",
    "rainfall",
    "wind_speed",
    "air_temperature_change",
    "track_temperature_change",
    "humidity_change",
    "safety_car_active",
    "vsc_active",
    "yellow_flag",
    "red_flag_active",
]


class Predictor:

    def __init__(self):

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}"
            )

        self.model = joblib.load(
            MODEL_PATH
        )

    def predict(self, features:dict) -> float:

        missing_features = [
            column
            for column in MODEL_COLUMNS
            if column not in features
        ]

        if missing_features:
            raise ValueError(
                f"Missing model features: "
                f"{missing_features}"
            )
        input_data = pd.DataFrame(
            [
                {
                    column: features[column]
                    for column in MODEL_COLUMNS
                }
            ]
        )

        prediction = self.model.predict(
            input_data
        )[0]

        return float(prediction)


predictor = Predictor()
