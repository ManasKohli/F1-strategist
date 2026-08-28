from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = (
    BASE_DIR
    / "be"
    / "data"
    / "processed"
)

MODEL_DIR = (
    BASE_DIR
    / "be"
    / "trained_models"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# FILES
# ==========================================================

TRAIN_FILE = (
    PROCESSED_DATA_DIR
    / "train_dataset.csv"
)

MODEL_FILE = (
    MODEL_DIR
    / "pit_strategy_model.joblib"
)


# ==========================================================
# TARGET
# ==========================================================

TARGET = "laps_until_pit"


# ==========================================================
# MODEL FEATURES
# ==========================================================
#
# IMPORTANT:
# Only these columns are allowed into the model.
#
# This prevents accidental data leakage from columns
# that may exist in the training dataset.
#
# ==========================================================

MODEL_COLUMNS = [

    # ------------------------------------------------------
    # Race context
    # ------------------------------------------------------

    "race",
    "lap_number",
    "total_laps",
    "laps_remaining",
    "race_progress",

    # ------------------------------------------------------
    # Driver / team
    # ------------------------------------------------------

    "driver",
    "team",
    "position",

    # ------------------------------------------------------
    # Strategy / tyres
    # ------------------------------------------------------

    "stint",
    "stint_laps",
    "pit_stop_count",

    "compound",
    "tyre_age",
    "fresh_tyre",

    # ------------------------------------------------------
    # Pace
    # ------------------------------------------------------

    "lap_time_seconds",
    "previous_lap_time",

    "avg_lap_time_3",
    "avg_lap_time_5",
    "avg_lap_time_10",

    "lap_time_delta_3",
    "lap_time_delta_5",

    "pace_trend_5",

    # ------------------------------------------------------
    # Weather
    # ------------------------------------------------------

    "air_temperature",
    "track_temperature",
    "humidity",
    "pressure",
    "rainfall",
    "wind_speed",

    "air_temperature_change",
    "track_temperature_change",
    "humidity_change",

    # ------------------------------------------------------
    # Race conditions
    # ------------------------------------------------------

    "safety_car_active",
    "vsc_active",
    "yellow_flag",
    "red_flag_active",
]


# ==========================================================
# CATEGORICAL FEATURES
# ==========================================================

CATEGORICAL_COLUMNS = [

    "race",
    "driver",
    "team",
    "compound",
]


# ==========================================================
# LOAD TRAINING DATA
# ==========================================================

print("=" * 60)
print("LOADING TRAINING DATA")
print("=" * 60)

if not TRAIN_FILE.exists():

    raise FileNotFoundError(
        f"\nTraining file not found:\n"
        f"{TRAIN_FILE}\n\n"
        "Run build_dataset.py first."
    )


train_df = pd.read_csv(
    TRAIN_FILE
)


print(
    f"Training dataset shape: "
    f"{train_df.shape}"
)


# ==========================================================
# CHECK TARGET
# ==========================================================

if TARGET not in train_df.columns:

    raise ValueError(
        f"\nTarget column '{TARGET}' "
        "does not exist in the dataset."
    )


# ==========================================================
# CHECK MODEL FEATURES
# ==========================================================

missing_columns = [
    column
    for column in MODEL_COLUMNS
    if column not in train_df.columns
]


if missing_columns:

    raise ValueError(
        "\nThe following model features "
        "are missing from the dataset:\n\n"
        f"{missing_columns}\n\n"
        "Run the updated build_dataset.py first."
    )


# ==========================================================
# DISPLAY SEASONS
# ==========================================================

if "season" in train_df.columns:

    print(
        "\nTraining season(s):"
    )

    print(
        train_df["season"]
        .unique()
    )

    print(
        "\nRows by season:"
    )

    print(
        train_df
        .groupby("season")
        .size()
    )


# ==========================================================
# REMOVE ROWS WITHOUT TARGET
# ==========================================================

before_rows = len(train_df)

train_df = train_df.dropna(
    subset=[TARGET]
).copy()

after_rows = len(train_df)


print(
    f"\nRemoved rows without target: "
    f"{before_rows - after_rows}"
)


# ==========================================================
# TARGET
# ==========================================================

y_train = train_df[
    TARGET
].copy()


# ==========================================================
# FEATURES
# ==========================================================

X_train = train_df[
    MODEL_COLUMNS
].copy()


# ==========================================================
# LEAKAGE CHECK
# ==========================================================

FORBIDDEN_COLUMNS = [

    # ------------------------------------------------------
    # Target
    # ------------------------------------------------------

    "laps_until_pit",

    # ------------------------------------------------------
    # Direct future pit information
    # ------------------------------------------------------

    "next_pit_lap",
    "PitInTime",
    "PitOutTime",

    # ------------------------------------------------------
    # Other potential leakage
    # ------------------------------------------------------

    "pit_lap",
]


leakage_found = [
    column
    for column in FORBIDDEN_COLUMNS
    if column in X_train.columns
]


if leakage_found:

    raise ValueError(
        "\n"
        + "=" * 60
        + "\nLEAKAGE ERROR\n"
        + "=" * 60
        + "\n\n"
        "The following forbidden columns "
        "are being used by the model:\n\n"
        f"{leakage_found}\n"
    )


# ==========================================================
# CATEGORICAL FEATURES
# ==========================================================

print("\nCategorical features:")

for column in CATEGORICAL_COLUMNS:

    print(
        f"  - {column}"
    )


# ==========================================================
# NUMERIC FEATURES
# ==========================================================

NUMERIC_COLUMNS = [
    column
    for column in MODEL_COLUMNS
    if column not in CATEGORICAL_COLUMNS
]


print(
    "\nNumeric features:"
)

for column in NUMERIC_COLUMNS:

    print(
        f"  - {column}"
    )


print(
    "\n"
    + "=" * 60
)

print(
    "FEATURE SUMMARY"
)

print(
    "=" * 60
)

print(
    f"Categorical features: "
    f"{len(CATEGORICAL_COLUMNS)}"
)

print(
    f"Numeric features: "
    f"{len(NUMERIC_COLUMNS)}"
)

print(
    f"Total raw features: "
    f"{len(MODEL_COLUMNS)}"
)


# ==========================================================
# CATEGORICAL PIPELINE
# ==========================================================

categorical_pipeline = Pipeline(
    steps=[

        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),

        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        ),

    ]
)


# ==========================================================
# NUMERIC PIPELINE
# ==========================================================

numeric_pipeline = Pipeline(
    steps=[

        (
            "imputer",
            SimpleImputer(
                strategy="median"
            )
        ),

    ]
)


# ==========================================================
# PREPROCESSOR
# ==========================================================

preprocessor = ColumnTransformer(
    transformers=[

        (
            "numeric",
            numeric_pipeline,
            NUMERIC_COLUMNS
        ),

        (
            "categorical",
            categorical_pipeline,
            CATEGORICAL_COLUMNS
        ),

    ]
)


# ==========================================================
# RANDOM FOREST
# ==========================================================
#
# Start with this model as our baseline.
#
# We can later compare it against:
#
# - HistGradientBoosting
# - XGBoost
# - LightGBM
# - CatBoost
#
# ==========================================================

model = RandomForestRegressor(

    n_estimators=5000,

    max_depth=20,

    min_samples_leaf=2,

    max_features="sqrt",

    random_state=42,

    n_jobs=-1,
)


# ==========================================================
# COMPLETE PIPELINE
# ==========================================================

pipeline = Pipeline(
    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            model
        ),

    ]
)


# ==========================================================
# TRAINING INFORMATION
# ==========================================================

print(
    "\n"
    + "=" * 60
)

print(
    "TRAINING MODEL"
)

print(
    "=" * 60
)

print(
    f"Training rows: "
    f"{len(X_train)}"
)

print(
    f"Raw model features: "
    f"{X_train.shape[1]}"
)

print(
    "\nTarget:"
)

print(
    y_train.describe()
)


# ==========================================================
# TARGET SANITY CHECK
# ==========================================================

if (y_train < 0).any():

    negative_count = (
        y_train < 0
    ).sum()

    raise ValueError(
        f"\nFound {negative_count} "
        "negative laps_until_pit values."
    )


print(
    "\nTarget range:"
)

print(
    f"Minimum: "
    f"{y_train.min():.2f}"
)

print(
    f"Maximum: "
    f"{y_train.max():.2f}"
)

print(
    f"Mean: "
    f"{y_train.mean():.2f}"
)


# ==========================================================
# FIT
# ==========================================================

print(
    "\nFitting model..."
)

pipeline.fit(
    X_train,
    y_train
)


# ==========================================================
# SAVE MODEL
# ==========================================================

joblib.dump(
    pipeline,
    MODEL_FILE
)


# ==========================================================
# VERIFY MODEL FILE
# ==========================================================

if not MODEL_FILE.exists():

    raise RuntimeError(
        "Model file was not created."
    )


# ==========================================================
# COMPLETE
# ==========================================================

print(
    "\n"
    + "=" * 60
)

print(
    "TRAINING COMPLETE"
)

print(
    "=" * 60
)

print(
    f"\nModel saved to:"
)

print(
    MODEL_FILE
)

print(
    "\nModel configuration:"
)

print(
    "  Algorithm: Random Forest Regressor"
)

print(
    "  Trees: 500"
)

print(
    "  Max depth: 20"
)

print(
    "  Min samples leaf: 2"
)

print(
    "  Max features: sqrt"
)

print(
    "\nNo future pit information "
    "was included in the model."
)