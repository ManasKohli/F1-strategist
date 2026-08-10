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

def clean_lap_data(laps: pd.DataFrame) -> pd.DataFrame:

    df = laps.copy()

    df = df[(~df["Deleted"]) & (df["IsAccurate"])].copy()

    df = df.dropna(
        subset=["LapTime"]
    ).copy()

    df["LapTime"] = pd.to_timedelta(
    df["LapTime"],
    errors="coerce"
    )

    df["lap_time_seconds"] = (
    df["LapTime"].dt.total_seconds()
    )
    
    df = df.sort_values(
        ["Driver", "LapNumber"]
    ).reset_index(drop=True)

    df["previous_lap_time"] = (
        df.groupby("Driver")["lap_time_seconds"]
        .shift(1)
    )

    df["avg_lap_time_3"] = (
        df.groupby("Driver")["lap_time_seconds"]
        .transform(
            lambda x: x.shift(1).rolling(3).mean()
        )
    )

    df["avg_lap_time_5"] = (
        df.groupby("Driver")["lap_time_seconds"]
        .transform(
            lambda x: x.shift(1).rolling(5).mean()
        )
    )

    # ------------------------------------------------------
    # Tire / stint features
    # ------------------------------------------------------

    df["tyre_age"] = df["TyreLife"]

    df["pit_stop_count"] = (
    df["Stint"] - 1
    )

    # ------------------------------------------------------
    # Rename columns to cleaner ML names
    # ------------------------------------------------------

    df = df.rename(
        columns={
            "Driver": "driver",
            "Team": "team",
            "LapNumber": "lap_number",
            "Position": "position",
            "Compound": "compound",
            "FreshTyre": "fresh_tyre",
            "Stint": "stint",
            "TrackStatus": "track_status",
        }
    )

    return df


if __name__ == "__main__":

    race_dir = (
        RAW_DATA_DIR
        / "2022"
        / "Monaco_Grand_Prix"
    )

    data = load_race_data(race_dir)

    laps = clean_lap_data(
        data["laps"]
    )

    print(
        "\nDataset shape:",
        laps.shape
    )

    print(
        "\nColumns:"
    )

    print(
        laps.columns.tolist()
    )

    print(
        "\nSample:"
    )
    print("\nSample:")

    print(
        laps[
            [
                "driver",
                "lap_number",
                "lap_time_seconds",
                "previous_lap_time",
                "avg_lap_time_3",
                "avg_lap_time_5",
                "tyre_age",
                "stint",
                "pit_stop_count",
            ]
        ].head(20)
    )