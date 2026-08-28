import pandas as pd
import joblib
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_FILE = BASE_DIR / "be" / "trained_models" / "pit_strategy_model.joblib"
DATA_FILE = BASE_DIR / "be" / "data" / "processed" / "test_dataset.csv"

print("Loading 2024-trained model...")
pipeline = joblib.load(MODEL_FILE)

print("Loading 2025 data...")
df = pd.read_csv(DATA_FILE)

print(f"2025 samples: {len(df)}")

TARGET = "laps_until_pit"
x_2025 = df.drop(columns=[TARGET])
y_2025 = df[TARGET]

print("Running predictions...")
y_pred = pipeline.predict(x_2025)

print("Evaluating predictions...")

mae = mean_absolute_error(y_2025, y_pred)
rmse = mean_squared_error(y_2025, y_pred) ** 0.5
r2 = r2_score(y_2025, y_pred)

print("\n" + "=" * 60)
print("2025 MODEL EVALUATION")
print("=" * 60)

print(f"\nMAE:  {mae:.4f} laps")
print(f"RMSE: {rmse:.4f} laps")
print(f"R²:   {r2:.4f}")