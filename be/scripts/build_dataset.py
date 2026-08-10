from pathlib import Path
import pandas as pd

BACKEND_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BACKEND_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def load_race_data(race_dir: Path) -> dict:

    data = {
        "laps": pd.read_csv(
            race_dir / "laps.csv"
        ),

        "weather": pd.read_csv(
            race_dir / "weather.csv"
        ),

        "results": pd.read_csv(
            race_dir / "results.csv"
        ),

        "track_status": pd.read_csv(
            race_dir / "track_status.csv"
        ),

        "race_control": pd.read_csv(
            race_dir / "race_control.csv"
        ),
    }
    return data


if __name__ == "__main__":

    race_dir = (
        RAW_DATA_DIR
        / "2022"
        / "Monaco_Grand_Prix"
    )

    data = load_race_data(race_dir)

    for name, dataframe in data.items():

        print(
            f"{name}: "
            f"{dataframe.shape}"
        )
        