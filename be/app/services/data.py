from pathlib import Path

import pandas as pd


DATA_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "processed"
    / "training_dataset.csv"
)


class RaceDataService:

    def __init__(self):

        if not DATA_PATH.exists():
            raise FileNotFoundError(
                f"Training dataset not found at {DATA_PATH}"
            )

        self.data = pd.read_csv(DATA_PATH)

    def get_race_state(
        self,
        race: str,
        driver: str,
        lap_number: int
    ) -> dict:

        matches = self.data[
            (self.data["race"] == race)
            & (self.data["driver"] == driver)
            & (self.data["lap_number"] == lap_number)
        ]

        if matches.empty:
            raise ValueError(
                "No race data found for "
                f"{driver} at {race}, lap {lap_number}."
            )

        row = matches.iloc[0]

        return row.to_dict()


race_data_service = RaceDataService()