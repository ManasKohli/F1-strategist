from pathlib import Path

import pandas as pd
from sklearn.preprocessing import OneHotEncoder


# ======================================================
# Paths
# ======================================================

BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_DATA_DIR = BASE_DIR / "be" / "data" / "processed"

INPUT_FILE = PROCESSED_DATA_DIR / "training_dataset.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "model_ready_dataset.csv"


# ======================================================
# Load dataset
# ======================================================

df = pd.read_csv(INPUT_FILE)

print("Original dataset shape:")
print(df.shape)


# ======================================================
# Target
# ======================================================

TARGET = "laps_until_pit"


# ======================================================
# Columns that MUST NOT be used as model features
# ======================================================

FORBIDDEN_COLUMNS = [
    "next_pit_lap",
    "PitInTime",
    "PitOutTime",
]


# ======================================================
# Select ONLY model features
# ======================================================

MODEL_COLUMNS = [
    "driver",
    "team",
    "lap_number",
    "stint",
    "position",
    "pit_stop_count",
    "compound",
    "tyre_age",
    "fresh_tyre",
    "lap_time_seconds",
    "previous_lap_time",
    "avg_lap_time_3",
    "avg_lap_time_5",
    "air_temperature",
    "track_temperature",
    "humidity",
    "pressure",
    "rainfall",
    "wind_speed",
    "safety_car_active",
    "vsc_active",
    "yellow_flag",
    "red_flag_active",
]


# ======================================================
# Safety checks
# ======================================================

if TARGET not in df.columns:
    raise ValueError(
        f"Target column '{TARGET}' not found."
    )


for column in FORBIDDEN_COLUMNS:

    if column in MODEL_COLUMNS:

        raise ValueError(
            f"LEAKAGE ERROR: '{column}' "
            "is being used as a model feature."
        )


# ======================================================
# Create features and target
# ======================================================

X = df[MODEL_COLUMNS].copy()

y = df[TARGET].copy()


# ======================================================
# Handle missing categorical values
# ======================================================

X["compound"] = X["compound"].fillna(
    "UNKNOWN"
)


# ======================================================
# Handle missing numerical values
# ======================================================

# Missing stint means the driver is at the
# beginning of a stint.
X["stint"] = X["stint"].fillna(1)


# Missing pit stop count means no recorded
# pit stop has occurred yet.
X["pit_stop_count"] = X["pit_stop_count"].fillna(0)


# Other numerical features use median imputation.
numeric_columns = [
    "tyre_age",
    "previous_lap_time",
    "avg_lap_time_3",
    "avg_lap_time_5",
]


for column in numeric_columns:

    X[column] = X[column].fillna(
        X[column].median()
    )


# ======================================================
# Convert boolean columns to integers
# ======================================================

boolean_columns = [
    "fresh_tyre",
    "safety_car_active",
    "vsc_active",
    "yellow_flag",
    "red_flag_active",
]


for column in boolean_columns:

    X[column] = X[column].astype(int)


# ======================================================
# Encode categorical columns
# ======================================================

categorical_columns = [
    "driver",
    "team",
    "compound",
]


encoder = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)


encoded = encoder.fit_transform(
    X[categorical_columns]
)


encoded_columns = encoder.get_feature_names_out(
    categorical_columns
)


encoded_df = pd.DataFrame(
    encoded,
    columns=encoded_columns,
    index=X.index
)


# ======================================================
# Remove original categorical columns
# ======================================================

X = X.drop(
    columns=categorical_columns
)


# ======================================================
# Combine numerical + encoded features
# ======================================================

X = pd.concat(
    [X, encoded_df],
    axis=1
)


# ======================================================
# Add target
# ======================================================

model_ready = pd.concat(
    [X, y],
    axis=1
)


# ======================================================
# Final leakage check
# ======================================================

forbidden_remaining = [
    column
    for column in FORBIDDEN_COLUMNS
    if column in model_ready.columns
]


if forbidden_remaining:

    raise ValueError(
        "LEAKAGE ERROR: forbidden columns found "
        f"in model-ready dataset: "
        f"{forbidden_remaining}"
    )


# ======================================================
# Final missing-value check
# ======================================================

missing_count = model_ready.isna().sum().sum()


if missing_count > 0:

    print(
        "\nWARNING: Missing values remain:"
    )

    print(
        model_ready.isna().sum()[
            model_ready.isna().sum() > 0
        ]
    )


# ======================================================
# Save
# ======================================================

model_ready.to_csv(
    OUTPUT_FILE,
    index=False
)


# ======================================================
# Diagnostics
# ======================================================

print("\nModel-ready dataset shape:")
print(model_ready.shape)

print("\nRemaining missing values:")
print(missing_count)

print("\nTarget:")
print(TARGET)

print("\nTarget statistics:")
print(y.describe())

print(
    "\nForbidden columns successfully excluded:"
)

print(FORBIDDEN_COLUMNS)

print("\nColumns:")
print(model_ready.columns.tolist())

print("\nFirst 5 rows:")
print(model_ready.head())

print("\nSaved to:")
print(OUTPUT_FILE)