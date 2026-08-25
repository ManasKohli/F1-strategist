from pathlib import Path
import pandas as pd


# ==========================================================
# Paths
# ==========================================================

BACKEND_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    BACKEND_DIR
    / "data"
    / "processed"
    / "training_dataset.csv"
)


# ==========================================================
# Load dataset
# ==========================================================

df = pd.read_csv(DATA_PATH)

print("\n" + "=" * 60)
print("DATASET CHECK")
print("=" * 60)

print(f"\nShape: {df.shape}")


# ==========================================================
# Target
# ==========================================================

TARGET = "laps_until_pit"

print("\nTarget:")
print(TARGET)

print("\nTarget statistics:")
print(df[TARGET].describe())


# ==========================================================
# Check suspicious columns
# ==========================================================

suspicious_keywords = [
    "next",
    "future",
    "final",
    "finish",
    "result",
    "pitin",
    "pitout",
    "position",
]


print("\nPotentially suspicious columns:")

for column in df.columns:

    column_lower = column.lower()

    if any(
        keyword in column_lower
        for keyword in suspicious_keywords
    ):

        print(f"  - {column}")


# ==========================================================
# Check target leakage
# ==========================================================

print("\nColumns containing pit information:")

for column in df.columns:

    if "pit" in column.lower():

        print(f"  - {column}")


# ==========================================================
# Check missing values
# ==========================================================

print("\nMissing values:")

missing = df.isnull().sum()

print(
    missing[missing > 0]
)


# ==========================================================
# Check target range
# ==========================================================

print("\nTarget range:")

print(
    f"Minimum: {df[TARGET].min()}"
)

print(
    f"Maximum: {df[TARGET].max()}"
)


# ==========================================================
# Check extreme targets
# ==========================================================

print("\nRows with laps_until_pit > 40:")

extreme = df[
    df[TARGET] > 40
]

print(
    extreme[
        [TARGET]
    ].head(20)
)


print("\nDataset check complete.")