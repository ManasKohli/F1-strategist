from pathlib import Path

import pandas as pd


# ======================================================
# PATHS
# ======================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "be" / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ======================================================
# LOAD RACE DATA
# ======================================================

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


# ======================================================
# CLEAN LAP DATA
# ======================================================

def clean_lap_data(
    laps: pd.DataFrame
) -> pd.DataFrame:

    df = laps.copy()

    # --------------------------------------------------
    # Keep accurate laps
    # --------------------------------------------------

    df = df[
        (~df["Deleted"]) &
        (df["IsAccurate"])
    ].copy()

    # --------------------------------------------------
    # Remove laps without lap time
    # --------------------------------------------------

    df = df.dropna(
        subset=["LapTime"]
    ).copy()

    # --------------------------------------------------
    # Convert lap time
    # --------------------------------------------------

    df["LapTime"] = pd.to_timedelta(
        df["LapTime"],
        errors="coerce"
    )

    df["lap_time_seconds"] = (
        df["LapTime"]
        .dt.total_seconds()
    )

    # --------------------------------------------------
    # Sort chronologically
    # --------------------------------------------------

    df = df.sort_values(
        ["Driver", "LapNumber"]
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------
    # Previous lap
    # --------------------------------------------------

    df["previous_lap_time"] = (
        df.groupby("Driver")[
            "lap_time_seconds"
        ].shift(1)
    )

    # --------------------------------------------------
    # Rolling pace
    #
    # IMPORTANT:
    # shift(1) prevents the current/future lap
    # from being used to calculate the feature.
    # --------------------------------------------------

    df["avg_lap_time_3"] = (
        df.groupby("Driver")[
            "lap_time_seconds"
        ]
        .transform(
            lambda x:
            x.shift(1)
             .rolling(
                 3,
                 min_periods=1
             )
             .mean()
        )
    )

    df["avg_lap_time_5"] = (
        df.groupby("Driver")[
            "lap_time_seconds"
        ]
        .transform(
            lambda x:
            x.shift(1)
             .rolling(
                 5,
                 min_periods=1
             )
             .mean()
        )
    )

    df["avg_lap_time_10"] = (
        df.groupby("Driver")[
            "lap_time_seconds"
        ]
        .transform(
            lambda x:
            x.shift(1)
             .rolling(
                 10,
                 min_periods=1
             )
             .mean()
        )
    )

    # --------------------------------------------------
    # Pace deltas
    # --------------------------------------------------

    df["lap_time_delta_3"] = (
        df["lap_time_seconds"]
        - df["avg_lap_time_3"]
    )

    df["lap_time_delta_5"] = (
        df["lap_time_seconds"]
        - df["avg_lap_time_5"]
    )

    # --------------------------------------------------
    # Pace trend
    #
    # Positive = getting slower
    # Negative = getting faster
    # --------------------------------------------------

    df["pace_trend_5"] = (
        df.groupby("Driver")[
            "lap_time_seconds"
        ]
        .transform(
            lambda x:
            x.shift(1)
             .rolling(
                 5,
                 min_periods=2
             )
             .apply(
                 lambda y:
                 y[-1] - y[0],
                 raw=True
             )
        )
    )

    # --------------------------------------------------
    # Tyre / stint features
    # --------------------------------------------------

    df["tyre_age"] = df["TyreLife"]

    df["pit_stop_count"] = (
        df["Stint"] - 1
    )

    # --------------------------------------------------
    # Rename columns
    # --------------------------------------------------

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


# ======================================================
# WEATHER
# ======================================================

def merge_weather_data(
    laps: pd.DataFrame,
    weather: pd.DataFrame
) -> pd.DataFrame:

    df = laps.copy()

    weather_df = weather.copy()

    # --------------------------------------------------
    # Convert timestamps
    # --------------------------------------------------

    df["LapStartTime"] = pd.to_timedelta(
        df["LapStartTime"],
        errors="coerce"
    )

    weather_df["Time"] = pd.to_timedelta(
        weather_df["Time"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["LapStartTime"]
    ).copy()

    weather_df = weather_df.dropna(
        subset=["Time"]
    ).copy()

    # --------------------------------------------------
    # Sort
    # --------------------------------------------------

    df = df.sort_values(
        "LapStartTime"
    )

    weather_df = weather_df.sort_values(
        "Time"
    )

    # --------------------------------------------------
    # Rename weather columns
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Time-aware merge
    # --------------------------------------------------

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


# ======================================================
# TRACK STATUS
# ======================================================

def merge_track_status(
    laps: pd.DataFrame,
    track_status: pd.DataFrame
) -> pd.DataFrame:

    df = laps.copy()

    status_df = track_status.copy()

    # --------------------------------------------------
    # Convert timestamps
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Sort
    # --------------------------------------------------

    df = df.sort_values(
        "LapStartTime"
    )

    status_df = status_df.sort_values(
        "Time"
    )

    # --------------------------------------------------
    # Rename
    # --------------------------------------------------

    status_df = status_df.rename(
        columns={
            "Message": "race_status"
        }
    )

    # --------------------------------------------------
    # Time-aware merge
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Race condition features
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Fill missing status
    # --------------------------------------------------

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


# ======================================================
# PIT EVENTS
# ======================================================

def identify_pit_laps(
    raw_laps: pd.DataFrame
) -> pd.DataFrame:

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


# ======================================================
# NEXT PIT
# ======================================================

def add_next_pit_lap(
    laps: pd.DataFrame,
    pit_events: pd.DataFrame
) -> pd.DataFrame:

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

    laps["next_pit_lap"] = (
        laps.apply(
            find_next_pit,
            axis=1
        )
    )

    return laps


# ======================================================
# TARGET
# ======================================================

def calculate_laps_until_pit(
    laps: pd.DataFrame
) -> pd.DataFrame:

    laps = laps.copy()

    laps["laps_until_pit"] = (
        laps["next_pit_lap"]
        - laps["lap_number"]
    )

    return laps


# ======================================================
# RACE FEATURES
# ======================================================

def add_race_features(
    laps: pd.DataFrame
) -> pd.DataFrame:

    df = laps.copy()

    # --------------------------------------------------
    # Total laps in race
    # --------------------------------------------------

    df["total_laps"] = (
        df.groupby("race")[
            "lap_number"
        ].transform("max")
    )

    # --------------------------------------------------
    # Remaining laps
    # --------------------------------------------------

    df["laps_remaining"] = (
        df["total_laps"]
        - df["lap_number"]
    )

    # --------------------------------------------------
    # Race progress
    # --------------------------------------------------

    df["race_progress"] = (
        df["lap_number"]
        / df["total_laps"]
    )

    return df


# ======================================================
# STINT FEATURES
# ======================================================

def add_stint_features(
    laps: pd.DataFrame
) -> pd.DataFrame:

    df = laps.copy()

    # --------------------------------------------------
    # Laps since start of current stint
    # --------------------------------------------------

    df["stint_laps"] = (
        df.groupby(
            ["race", "driver", "stint"]
        )["lap_number"]
        .transform(
            lambda x:
            x - x.min() + 1
        )
    )

    return df


# ======================================================
# WEATHER CHANGE FEATURES
# ======================================================

def add_weather_change_features(
    laps: pd.DataFrame
) -> pd.DataFrame:

    df = laps.copy()

    # --------------------------------------------------
    # Weather changes
    #
    # Shift is used so current value is compared
    # with previous available observation.
    # --------------------------------------------------

    df["track_temperature_change"] = (
        df.groupby("race")[
            "track_temperature"
        ].diff()
    )

    df["air_temperature_change"] = (
        df.groupby("race")[
            "air_temperature"
        ].diff()
    )

    df["humidity_change"] = (
        df.groupby("race")[
            "humidity"
        ].diff()
    )

    return df


# ======================================================
# REMOVE ROWS WITHOUT TARGET
# ======================================================

def remove_missing_targets(
    laps: pd.DataFrame
) -> pd.DataFrame:

    laps = laps.copy()

    laps = laps[
        laps["laps_until_pit"].notna()
    ].copy()

    return laps


# ======================================================
# MAIN
# ======================================================

if __name__ == "__main__":

    # ==================================================
    # SEASONS
    # ==================================================

    SEASONS = [
        2024,
        2025
    ]

    all_races = []

    # ==================================================
    # PROCESS SEASONS
    # ==================================================

    for season in SEASONS:

        season_dir = (
            RAW_DATA_DIR
            / str(season)
        )

        print("\n" + "=" * 60)
        print(
            f"Processing {season} season"
        )
        print("=" * 60)

        if not season_dir.exists():

            print(
                f"WARNING: {season_dir} "
                "does not exist."
            )

            continue

        race_directories = sorted(
            [
                race_dir
                for race_dir
                in season_dir.iterdir()
                if race_dir.is_dir()
            ]
        )

        print(
            f"Found "
            f"{len(race_directories)} races"
        )

        # ==================================================
        # PROCESS EACH RACE
        # ==================================================

        for race_dir in race_directories:

            race_name = race_dir.name

            print(
                f"\nProcessing "
                f"{season} - {race_name}"
            )

            try:

                # ------------------------------------------
                # Load
                # ------------------------------------------

                data = load_race_data(
                    race_dir
                )

                # ------------------------------------------
                # Clean laps
                # ------------------------------------------

                laps = clean_lap_data(
                    data["laps"]
                )

                # ------------------------------------------
                # Weather
                # ------------------------------------------

                laps = merge_weather_data(
                    laps,
                    data["weather"]
                )

                # ------------------------------------------
                # Track status
                # ------------------------------------------

                laps = merge_track_status(
                    laps,
                    data["track_status"]
                )

                # ------------------------------------------
                # Race metadata
                # ------------------------------------------

                laps["season"] = season

                laps["race"] = race_name

                # ------------------------------------------
                # Pit events
                # ------------------------------------------

                pit_events = identify_pit_laps(
                    data["laps"]
                )

                # ------------------------------------------
                # Next pit
                # ------------------------------------------

                laps = add_next_pit_lap(
                    laps,
                    pit_events
                )

                # ------------------------------------------
                # Target
                # ------------------------------------------

                laps = calculate_laps_until_pit(
                    laps
                )

                # ------------------------------------------
                # Race features
                # ------------------------------------------

                laps = add_race_features(
                    laps
                )

                # ------------------------------------------
                # Stint features
                # ------------------------------------------

                laps = add_stint_features(
                    laps
                )

                # ------------------------------------------
                # Weather changes
                # ------------------------------------------

                laps = add_weather_change_features(
                    laps
                )

                # ------------------------------------------
                # Remove rows without target
                # ------------------------------------------

                laps = remove_missing_targets(
                    laps
                )

                # ------------------------------------------
                # Store
                # ------------------------------------------

                all_races.append(
                    laps
                )

                print(
                    f"✓ {race_name}: "
                    f"{len(laps)} rows"
                )

            except Exception as e:

                print(
                    f"✗ Failed "
                    f"{race_name}: {e}"
                )

    # ==================================================
    # COMBINE
    # ==================================================

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

    # ==================================================
    # SORT
    # ==================================================

    training_dataset = (
        training_dataset
        .sort_values(
            [
                "season",
                "race",
                "driver",
                "lap_number",
            ]
        )
        .reset_index(drop=True)
    )

    # ==================================================
    # SAVE
    # ==================================================

    output_path = (
        PROCESSED_DATA_DIR
        / "training_dataset.csv"
    )

    training_dataset.to_csv(
        output_path,
        index=False
    )

    # ==================================================
    # SUMMARY
    # ==================================================

    print("\n" + "=" * 60)
    print("FINAL TRAINING DATASET")
    print("=" * 60)

    print(
        f"Total rows: "
        f"{len(training_dataset)}"
    )

    print(
        f"Total columns: "
        f"{len(training_dataset.columns)}"
    )

    print(
        f"Total races: "
        f"{training_dataset[['season', 'race']]}"
        ".drop_duplicates().shape[0]}"
    )

    print(
        "\nRows by season:"
    )

    print(
        training_dataset
        .groupby("season")
        .size()
    )

    print(
        "\nTarget summary:"
    )

    print(
        training_dataset[
            "laps_until_pit"
        ].describe()
    )

    print(
        "\nNew features:"
    )

    print(
        [
            "total_laps",
            "laps_remaining",
            "race_progress",
            "avg_lap_time_10",
            "lap_time_delta_3",
            "lap_time_delta_5",
            "pace_trend_5",
            "stint_laps",
            "track_temperature_change",
            "air_temperature_change",
            "humidity_change",
        ]
    )

    print(
        f"\n✓ Dataset saved to:"
        f"\n{output_path}"
    )