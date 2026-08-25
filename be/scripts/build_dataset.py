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

def merge_weather_data(laps: pd.DataFrame, weather: pd.DataFrame) -> pd.DataFrame:

    df = laps.copy()
    weather_df = weather.copy()

    df["LapStartTime"] = pd.to_timedelta(
        df["LapStartTime"],
        errors="coerce"
    )

    weather_df["Time"] = pd.to_timedelta(
        weather_df["Time"],
        errors="coerce"
    )

    # Remove rows with invalid timestamps
    df = df.dropna(
        subset=["LapStartTime"]
    ).copy()

    weather_df = weather_df.dropna(
        subset=["Time"]
    ).copy()

    # ------------------------------------------------------
    # Sort before merge_asof
    # ------------------------------------------------------

    df = df.sort_values(
        "LapStartTime"
    )

    weather_df = weather_df.sort_values(
        "Time"
    )

    # ------------------------------------------------------
    # Rename weather columns
    # ------------------------------------------------------

    weather_df = weather_df.rename(
        columns={
            "AirTemp": "air_temperature",
            "Humidity": "humidity",
            "Pressure": "pressure",
            "Rainfall": "rainfall",
            "TrackTemp": "track_temperature",
            "WindDirection": "wind_direction",
            "WindSpeed": "wind_speed",
        }
    )

    # ------------------------------------------------------
    # Time-aware merge
    # ------------------------------------------------------

    df = pd.merge_asof(
        df,
        weather_df[
            [
                "Time",
                "air_temperature",
                "humidity",
                "pressure",
                "rainfall",
                "track_temperature",
                "wind_direction",
                "wind_speed",
            ]
        ],
        left_on="LapStartTime",
        right_on="Time",
        direction="backward",
    )

    return df

def merge_track_status(
    laps: pd.DataFrame,
    track_status: pd.DataFrame
) -> pd.DataFrame:
    """
    Adds time-aware race-condition features to each lap.
    """

    df = laps.copy()
    status_df = track_status.copy()

    # ------------------------------------------------------
    # Convert timestamps
    # ------------------------------------------------------

    df["LapStartTime"] = pd.to_timedelta(
        df["LapStartTime"],
        errors="coerce"
    )

    status_df["Time"] = pd.to_timedelta(
        status_df["Time"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["LapStartTime"]
    ).copy()

    status_df = status_df.dropna(
        subset=["Time"]
    ).copy()

    # ------------------------------------------------------
    # Sort by time
    # ------------------------------------------------------

    df = df.sort_values(
        "LapStartTime"
    )

    status_df = status_df.sort_values(
        "Time"
    )

    # ------------------------------------------------------
    # Rename status message
    # ------------------------------------------------------

    status_df = status_df.rename(
        columns={
            "Message": "race_status"
        }
    )

    # ------------------------------------------------------
    # Time-aware merge
    # ------------------------------------------------------

    df = pd.merge_asof(
        df,
        status_df[
            [
                "Time",
                "Status",
                "race_status",
            ]
        ],
        left_on="LapStartTime",
        right_on="Time",
        direction="backward",
    )

    # ------------------------------------------------------
    # Convert status codes into model features
    # ------------------------------------------------------

    df["safety_car_active"] = (
        df["Status"] == 4
    )

    df["vsc_active"] = (
        df["Status"] == 6
    )

    df["yellow_flag"] = (
        df["Status"] == 2
    )

    df["red_flag_active"] = (
        df["Status"] == 5
    )

    # ------------------------------------------------------
    # Fill missing status
    # ------------------------------------------------------

    df["Status"] = (
        df["Status"]
        .fillna(1)
        .astype(int)
    )

    df["race_status"] = (
        df["race_status"]
        .fillna("AllClear")
    )

    return df

def identify_pit_laps(
    raw_laps: pd.DataFrame
) -> pd.DataFrame:
    """
    Extracts pit-in events from the raw FastF1 lap data.

    Pit events are taken from the raw dataset rather than the
    cleaned feature dataset because pit-in laps may be marked
    as inaccurate by FastF1.
    """

    pit_events = raw_laps[
        raw_laps["PitInTime"].notna()
    ].copy()

    pit_events = pit_events[
        [
            "Driver",
            "LapNumber",
            "PitInTime",
            "Stint",
        ]
    ].copy()

    pit_events = pit_events.rename(
        columns={
            "Driver": "driver",
            "LapNumber": "lap_number",
        }
    )

    pit_events["pit_lap"] = True

    return pit_events

def add_next_pit_lap(
    laps: pd.DataFrame,
    pit_events: pd.DataFrame
) -> pd.DataFrame:
    """
    Adds the next known pit lap for each driver.

    For every lap, finds the next pit stop that occurs
    after the current lap.
    """

    laps = laps.copy()

    pit_laps_by_driver = (
        pit_events
        .groupby("driver")["lap_number"]
        .apply(list)
        .to_dict()
    )

    def find_next_pit(row):
        driver = row["driver"]
        current_lap = row["lap_number"]

        pit_laps = pit_laps_by_driver.get(
            driver,
            []
        )

        future_pits = [
            pit_lap
            for pit_lap in pit_laps
            if pit_lap > current_lap
        ]

        if not future_pits:
            return None

        return min(future_pits)

    laps["next_pit_lap"] = laps.apply(
        find_next_pit,
        axis=1
    )

    return laps

def calculate_laps_until_pit(
    laps: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculates the number of laps until the driver's
    next pit stop.

    This becomes the target variable for the ML model.
    """

    laps = laps.copy()

    laps["laps_until_pit"] = (
        laps["next_pit_lap"]
        - laps["lap_number"]
    )

    return laps

def remove_missing_targets(
    laps: pd.DataFrame
) -> pd.DataFrame:
    """
    Removes rows where the driver has no future pit stop.

    These rows cannot be used for supervised training because
    there is no known target value.
    """

    laps = laps.copy()

    laps = laps[
        laps["laps_until_pit"].notna()
    ].copy()

    return laps

if __name__ == "__main__":

    # ======================================================
    # Seasons to process
    # ======================================================

    SEASONS = [2024, 2025]

    all_races = []

    # ======================================================
    # Loop through every season
    # ======================================================

    for season in SEASONS:

        season_dir = RAW_DATA_DIR / str(season)

        print("\n" + "=" * 60)
        print(f"Processing {season} season")
        print("=" * 60)

        # --------------------------------------------------
        # Find every downloaded race
        # --------------------------------------------------

        race_directories = sorted(
            [
                race_dir
                for race_dir in season_dir.iterdir()
                if race_dir.is_dir()
            ]
        )

        print(
            f"Found {len(race_directories)} races"
        )

        # ==================================================
        # Process each race
        # ==================================================

        for race_dir in race_directories:

            race_name = race_dir.name

            print(
                f"\nProcessing {season} - {race_name}"
            )

            try:

                # ------------------------------------------
                # Load raw race data
                # ------------------------------------------

                data = load_race_data(
                    race_dir
                )

                # ------------------------------------------
                # Clean lap data
                # ------------------------------------------

                laps = clean_lap_data(
                    data["laps"]
                )

                # ------------------------------------------
                # Add weather
                # ------------------------------------------

                laps = merge_weather_data(
                    laps,
                    data["weather"]
                )

                # ------------------------------------------
                # Add track status
                # ------------------------------------------

                laps = merge_track_status(
                    laps,
                    data["track_status"]
                )

                # ------------------------------------------
                # Extract pit events from RAW laps
                # ------------------------------------------

                pit_events = identify_pit_laps(
                    data["laps"]
                )

                # ------------------------------------------
                # Add next pit lap
                # ------------------------------------------

                laps = add_next_pit_lap(
                    laps,
                    pit_events
                )

                # ------------------------------------------
                # Calculate target
                # ------------------------------------------

                laps = calculate_laps_until_pit(
                    laps
                )

                # ------------------------------------------
                # Remove rows without target
                # ------------------------------------------

                laps = remove_missing_targets(
                    laps
                )

                # ------------------------------------------
                # Add race metadata
                # ------------------------------------------

                laps["season"] = season
                laps["race"] = race_name

                # ------------------------------------------
                # Store race dataset
                # ------------------------------------------

                all_races.append(
                    laps
                )

                print(
                    f"✓ {race_name}: "
                    f"{len(laps)} training rows"
                )

            except Exception as e:

                print(
                    f"✗ Failed {race_name}: {e}"
                )

    # ======================================================
    # Combine all races
    # ======================================================

    print("\n" + "=" * 60)
    print("Combining all races")
    print("=" * 60)

    if not all_races:

        raise RuntimeError(
            "No race datasets were successfully processed."
        )

    training_dataset = pd.concat(
        all_races,
        ignore_index=True
    )

    # ======================================================
    # Sort dataset
    # ======================================================

    training_dataset = training_dataset.sort_values(
        [
            "season",
            "race",
            "driver",
            "lap_number"
        ]
    ).reset_index(
        drop=True
    )

    # ======================================================
    # Save dataset
    # ======================================================

    output_path = (
        PROCESSED_DATA_DIR
        / "training_dataset.csv"
    )

    training_dataset.to_csv(
        output_path,
        index=False
    )

    # ======================================================
    # Final summary
    # ======================================================

    print("\n" + "=" * 60)
    print("FINAL TRAINING DATASET")
    print("=" * 60)

    print(
        f"Total rows: {len(training_dataset)}"
    )

    print(
        f"Total columns: "
        f"{len(training_dataset.columns)}"
    )

    print(
        f"Total races: "
        f"{training_dataset[['season', 'race']].drop_duplicates().shape[0]}"
    )

    print(
        "\nRows by season:"
    )

    print(
        training_dataset.groupby("season").size()
    )

    print(
        "\nTarget summary:"
    )

    print(
        training_dataset["laps_until_pit"].describe()
    )

    print(
        f"\n✓ Training dataset saved to:"
        f"\n{output_path}"
    )