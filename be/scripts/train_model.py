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
# LOAD TRAINING DATA
# ==========================================================

print("=" * 60)
print("LOADING TRAINING DATA")
print("=" * 60)

train_df = pd.read_csv(
    TRAIN_FILE
)

print(
    f"Training dataset shape: {train_df.shape}"
)

print(
    f"Training season(s): "
    f"{train_df['season'].unique()}"
)


# ==========================================================
# REMOVE ROWS WITHOUT TARGET
# ==========================================================

train_df = train_df.dropna(
    subset=[TARGET]
).copy()


# ==========================================================
# TARGET
# ==========================================================

y_train = train_df[TARGET]


# ==========================================================
# REMOVE TARGET + DATA LEAKAGE COLUMNS
# ==========================================================

FORBIDDEN_COLUMNS = [
    # Target
    "laps_until_pit",

    # Direct future pit information
    "next_pit_lap",
    "PitInTime",
    "PitOutTime",
]


X_train = train_df.drop(
    columns=FORBIDDEN_COLUMNS,
    errors="ignore"
)


# ==========================================================
# REMOVE IDENTIFIER / NON-PREDICTIVE COLUMNS
# ==========================================================

IDENTIFIER_COLUMNS = [
    "DriverNumber",
    "Deleted",
    "DeletedReason",
    "FastF1Generated",
    "IsAccurate",
    "LapStartDate",

    # Season is not useful because training is only 2024
    "season",
]


X_train = X_train.drop(
    columns=IDENTIFIER_COLUMNS,
    errors="ignore"
)


# ==========================================================
# REMOVE RAW TIME COLUMNS
# ==========================================================

RAW_TIME_COLUMNS = [
    "Time_x",
    "LapTime",
    "PitOutTime",
    "PitInTime",
    "Sector1Time",
    "Sector2Time",
    "Sector3Time",
    "Sector1SessionTime",
    "Sector2SessionTime",
    "Sector3SessionTime",
    "LapStartTime",
    "Time_y",
    "Time",
]


X_train = X_train.drop(
    columns=RAW_TIME_COLUMNS,
    errors="ignore"
)


# ==========================================================
# REMOVE RAW TEXT STATUS COLUMNS
# ==========================================================

STATUS_COLUMNS = [
    "track_status",
    "Status",
    "race_status",
]


X_train = X_train.drop(
    columns=STATUS_COLUMNS,
    errors="ignore"
)


# ==========================================================
# CATEGORICAL FEATURES
# ==========================================================

categorical_columns = [
    "driver",
    "team",
    "compound",
    "race",
]


# ==========================================================
# NUMERIC FEATURES
# ==========================================================

numeric_columns = [
    column
    for column in X_train.columns
    if column not in categorical_columns
]


# ==========================================================
# DISPLAY FEATURES
# ==========================================================

print("\nCategorical features:")
print(categorical_columns)

print("\nNumeric features:")
print(numeric_columns)

print(
    f"\nTotal model features: "
    f"{len(categorical_columns) + len(numeric_columns)}"
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
        )
    ]
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
# PREPROCESSOR
# ==========================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_columns
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_columns
        ),
    ]
)


# ==========================================================
# RANDOM FOREST MODEL
# ==========================================================

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)


# ==========================================================
# COMPLETE ML PIPELINE
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
# TRAIN MODEL
# ==========================================================

print("\n" + "=" * 60)
print("TRAINING MODEL")
print("=" * 60)

print(
    f"Training rows: {len(X_train)}"
)

print(
    f"Number of raw features: "
    f"{X_train.shape[1]}"
)

print("\nTarget:")
print(
    y_train.describe()
)


# ==========================================================
# FIT
# ==========================================================

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
# COMPLETE
# ==========================================================

print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print(
    f"Model saved to:\n{MODEL_FILE}"
)
