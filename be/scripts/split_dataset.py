from pathlib import Path

import pandas as pd


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


# ==========================================================
# FILES
# ==========================================================

INPUT_FILE = (
    PROCESSED_DATA_DIR
    / "training_dataset.csv"
)

TRAIN_FILE = (
    PROCESSED_DATA_DIR
    / "train_dataset.csv"
)

TEST_FILE = (
    PROCESSED_DATA_DIR
    / "test_dataset.csv"
)


# ==========================================================
# LOAD DATASET
# ==========================================================

print("=" * 60)
print("DATASET SPLIT")
print("=" * 60)


if not INPUT_FILE.exists():

    raise FileNotFoundError(
        f"\nTraining dataset not found:\n"
        f"{INPUT_FILE}\n\n"
        "Run build_dataset.py first."
    )


df = pd.read_csv(
    INPUT_FILE
)


print(
    "\nFull dataset:"
)

print(
    f"Rows: {len(df)}"
)

print(
    f"Columns: {len(df.columns)}"
)


# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

REQUIRED_COLUMNS = [
    "season",
    "race",
    "driver",
    "lap_number",
    "laps_until_pit",
]


missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]


if missing_columns:

    raise ValueError(
        "\nMissing required columns:\n"
        f"{missing_columns}"
    )


# ==========================================================
# SEASON CHECK
# ==========================================================

print(
    "\n"
    + "=" * 60
)

print(
    "ROWS BY SEASON"
)

print(
    "=" * 60
)

season_counts = (
    df.groupby("season")
    .size()
)


print(
    season_counts
)


# ==========================================================
# CHECK 2024 / 2025
# ==========================================================

available_seasons = set(
    df["season"].dropna().unique()
)


if 2024 not in available_seasons:

    raise ValueError(
        "\n2024 data was not found."
    )


if 2025 not in available_seasons:

    raise ValueError(
        "\n2025 data was not found."
    )


# ==========================================================
# TRAIN / TEST SPLIT
# ==========================================================
#
# 2024 = TRAIN
# 2025 = TEST
#
# NO RANDOM SPLIT.
#
# This gives us a realistic "future season"
# evaluation.
#
# ==========================================================

train_df = df[
    df["season"] == 2024
].copy()


test_df = df[
    df["season"] == 2025
].copy()


# ==========================================================
# VALIDATE SPLIT
# ==========================================================

if train_df.empty:

    raise ValueError(
        "\nTraining dataset is empty."
    )


if test_df.empty:

    raise ValueError(
        "\nTest dataset is empty."
    )


# ==========================================================
# SORT DATA
# ==========================================================

train_df = (
    train_df
    .sort_values(
        [
            "race",
            "driver",
            "lap_number",
        ]
    )
    .reset_index(drop=True)
)


test_df = (
    test_df
    .sort_values(
        [
            "race",
            "driver",
            "lap_number",
        ]
    )
    .reset_index(drop=True)
)


# ==========================================================
# FINAL SEASON VALIDATION
# ==========================================================

train_seasons = set(
    train_df["season"].unique()
)

test_seasons = set(
    test_df["season"].unique()
)


if train_seasons != {2024}:

    raise ValueError(
        "\nTRAINING LEAKAGE ERROR!\n"
        f"Training contains: {train_seasons}\n"
        "Expected: {2024}"
    )


if test_seasons != {2025}:

    raise ValueError(
        "\nTEST DATA ERROR!\n"
        f"Test contains: {test_seasons}\n"
        "Expected: {2025}"
    )


# ==========================================================
# SAVE TRAINING DATA
# ==========================================================

train_df.to_csv(
    TRAIN_FILE,
    index=False
)


# ==========================================================
# SAVE TEST DATA
# ==========================================================

test_df.to_csv(
    TEST_FILE,
    index=False
)


# ==========================================================
# TRAINING SUMMARY
# ==========================================================

print(
    "\n"
    + "=" * 60
)

print(
    "TRAINING DATA — 2024"
)

print(
    "=" * 60
)

print(
    f"Rows: {len(train_df)}"
)

print(
    f"Races: "
    f"{train_df['race'].nunique()}"
)

print(
    f"Drivers: "
    f"{train_df['driver'].nunique()}"
)

print(
    f"Season: "
    f"{train_df['season'].unique()}"
)

print(
    "\nTarget:"
)

print(
    train_df[
        "laps_until_pit"
    ].describe()
)


# ==========================================================
# TEST SUMMARY
# ==========================================================

print(
    "\n"
    + "=" * 60
)

print(
    "TEST DATA — 2025"
)

print(
    "=" * 60
)

print(
    f"Rows: {len(test_df)}"
)

print(
    f"Races: "
    f"{test_df['race'].nunique()}"
)

print(
    f"Drivers: "
    f"{test_df['driver'].nunique()}"
)

print(
    f"Season: "
    f"{test_df['season'].unique()}"
)

print(
    "\nTarget:"
)

print(
    test_df[
        "laps_until_pit"
    ].describe()
)


# ==========================================================
# FILE VALIDATION
# ==========================================================

if not TRAIN_FILE.exists():

    raise RuntimeError(
        "Training file was not created."
    )


if not TEST_FILE.exists():

    raise RuntimeError(
        "Test file was not created."
    )


# ==========================================================
# COMPLETE
# ==========================================================

print(
    "\n"
    + "=" * 60
)

print(
    "SPLIT COMPLETE"
)

print(
    "=" * 60
)

print(
    "\n2024 → TRAIN"
)

print(
    "2025 → TEST"
)

print(
    "\nTraining file:"
)

print(
    TRAIN_FILE
)

print(
    "\nTest file:"
)

print(
    TEST_FILE
)

print(
    "\n✓ No 2025 data is included "
    "in the training dataset."
)

print(
    "✓ No 2024 data is included "
    "in the test dataset."
)