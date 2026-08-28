from pathlib import Path

import pandas as pd


# ======================================================
# PATHS
# ======================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = (
    BASE_DIR
    / "be"
    / "data"
    / "processed"
)

INPUT_FILE = (
    PROCESSED_DATA_DIR
    / "training_dataset.csv"
)

OUTPUT_FILE = (
    PROCESSED_DATA_DIR
    / "model_ready_dataset.csv"
)


# ======================================================
# LOAD DATASET
# ======================================================

print("=" * 60)
print("LOADING TRAINING DATASET")
print("=" * 60)

df = pd.read_csv(
    INPUT_FILE
)

print(
    f"Original dataset shape: "
    f"{df.shape}"
)


# ======================================================
# TARGET
# ======================================================

TARGET = "laps_until_pit"


# ======================================================
# MODEL FEATURES
# ======================================================

MODEL_COLUMNS = [

    # ----------------------------------------------
    # Race
    # ----------------------------------------------

    "race",
    "lap_number",
    "total_laps",
    "laps_remaining",
    "race_progress",

    # ----------------------------------------------
    # Driver / team
    # ----------------------------------------------

    "driver",
    "team",
    "position",

    # ----------------------------------------------
    # Strategy
    # ----------------------------------------------

    "stint",
    "stint_laps",
    "pit_stop_count",

    "compound",
    "tyre_age",
    "fresh_tyre",

    # ----------------------------------------------
    # Pace
    # ----------------------------------------------

    "lap_time_seconds",
    "previous_lap_time",

    "avg_lap_time_3",
    "avg_lap_time_5",
    "avg_lap_time_10",

    "lap_time_delta_3",
    "lap_time_delta_5",

    "pace_trend_5",

    # ----------------------------------------------
    # Weather
    # ----------------------------------------------

    "air_temperature",
    "track_temperature",
    "humidity",
    "pressure",
    "rainfall",
    "wind_speed",

    "air_temperature_change",
    "track_temperature_change",
    "humidity_change",

    # ----------------------------------------------
    # Race conditions
    # ----------------------------------------------

    "safety_car_active",
    "vsc_active",
    "yellow_flag",
    "red_flag_active",
]


# ======================================================
# SAFETY CHECKS
# ======================================================

if TARGET not in df.columns:

    raise ValueError(
        f"Target '{TARGET}' "
        "not found in dataset."
    )


missing_features = [
    column
    for column in MODEL_COLUMNS
    if column not in df.columns
]


if missing_features:

    raise ValueError(
        "\nMissing model features:\n"
        f"{missing_features}"
    )


# ======================================================
# FORBIDDEN / LEAKAGE COLUMNS
# ======================================================

FORBIDDEN_COLUMNS = [

    "laps_until_pit",
    "next_pit_lap",

    "PitInTime",
    "PitOutTime",

    "pit_lap",
]


# ======================================================
# CHECK LEAKAGE
# ======================================================

for column in FORBIDDEN_COLUMNS:

    if column in MODEL_COLUMNS:

        raise ValueError(
            "\nLEAKAGE ERROR:\n"
            f"'{column}' is being used "
            "as a model feature."
        )


# ======================================================
# CREATE X / Y
# ======================================================

X = df[
    MODEL_COLUMNS
].copy()

y = df[
    TARGET
].copy()


# ======================================================
# CATEGORICAL VALUES
# ======================================================

X["driver"] = (
    X["driver"]
    .fillna("UNKNOWN")
)

X["team"] = (
    X["team"]
    .fillna("UNKNOWN")
)

X["compound"] = (
    X["compound"]
    .fillna("UNKNOWN")
)

X["race"] = (
    X["race"]
    .fillna("UNKNOWN")
)


# ======================================================
# BOOLEAN COLUMNS
# ======================================================

BOOLEAN_COLUMNS = [

    "fresh_tyre",

    "safety_car_active",
    "vsc_active",
    "yellow_flag",
    "red_flag_active",
]


for column in BOOLEAN_COLUMNS:

    X[column] = (
        X[column]
        .fillna(False)
        .astype(int)
    )


# ======================================================
# NUMERIC COLUMNS
# ======================================================

NUMERIC_COLUMNS = [

    "lap_number",
    "total_laps",
    "laps_remaining",
    "race_progress",

    "position",

    "stint",
    "stint_laps",
    "pit_stop_count",

    "tyre_age",

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
]


# ======================================================
# CONVERT NUMERIC DATA
# ======================================================

for column in NUMERIC_COLUMNS:

    X[column] = pd.to_numeric(
        X[column],
        errors="coerce"
    )


# ======================================================
# DO NOT MEDIAN-FILL HERE
# ======================================================
#
# The train_model.py pipeline already has:
#
# SimpleImputer(strategy="median")
#
# so we let the training pipeline handle
# numerical missing values.
#
# ======================================================


# ======================================================
# FINAL LEAKAGE CHECK
# ======================================================

remaining_forbidden = [
    column
    for column in FORBIDDEN_COLUMNS
    if column in X.columns
]


if remaining_forbidden:

    raise ValueError(
        "\nLEAKAGE ERROR:\n"
        f"{remaining_forbidden}"
    )


# ======================================================
# COMBINE
# ======================================================

model_ready = pd.concat(
    [
        X,
        y
    ],
    axis=1
)


# ======================================================
# FINAL DIAGNOSTICS
# ======================================================

print("\n" + "=" * 60)
print("MODEL-READY DATASET")
print("=" * 60)

print(
    f"Shape: "
    f"{model_ready.shape}"
)

print(
    f"\nFeatures: "
    f"{len(MODEL_COLUMNS)}"
)

print(
    "\nCategorical features:"
)

print(
    [
        "race",
        "driver",
        "team",
        "compound",
    ]
)

print(
    "\nTarget statistics:"
)

print(
    y.describe()
)

print(
    "\nRows by season:"
)

if "season" in df.columns:

    print(
        df.groupby("season").size()
    )

print(
    "\nMissing values:"
)

missing = (
    model_ready
    .isna()
    .sum()
)

print(
    missing[
        missing > 0
    ]
)

# ======================================================
# SAVE
# ======================================================

model_ready.to_csv(
    OUTPUT_FILE,
    index=False
)

print(
    f"\n✓ Saved to:"
    f"\n{OUTPUT_FILE}"
)

print(
    "\nPreprocessing complete."
)