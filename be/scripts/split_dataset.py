from pathlib import Path
import pandas as pd

#paths
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

TRAIN_FILE = (
    PROCESSED_DATA_DIR
    / "train_dataset.csv"
)

TEST_FILE = (
    PROCESSED_DATA_DIR
    / "test_dataset.csv"
)


df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("DATASET SPLIT")
print("=" * 60)

print("\nFull dataset:")
print(df.shape)


print("\nRows by season:")
print(
    df.groupby("season").size()
)

train_df = df[df["season"] == 2024].copy()

test_df = df[
    df["season"] == 2025
].copy()


if train_df.empty:
    raise ValueError(
        "Training dataset is empty."
    )

if test_df.empty:
    raise ValueError(
        "Test dataset is empty."
    )


train_df.to_csv(
    TRAIN_FILE,
    index=False
)

test_df.to_csv(
    TEST_FILE,
    index=False
)
print("\n" + "=" * 60)
print("TRAINING DATA")
print("=" * 60)

print(
    f"Rows: {len(train_df)}"
)

print(
    f"Races: {train_df['race'].nunique()}"
)

print(
    f"Season: {train_df['season'].unique()}"
)


print("\n" + "=" * 60)
print("TEST DATA")
print("=" * 60)

print(
    f"Rows: {len(test_df)}"
)

print(
    f"Races: {test_df['race'].nunique()}"
)

print(
    f"Season: {test_df['season'].unique()}"
)


print("\n" + "=" * 60)
print("FILES SAVED")
print("=" * 60)

print(TRAIN_FILE)
print(TEST_FILE)