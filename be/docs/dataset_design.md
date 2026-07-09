# Dataset Design

# F1 Strategist

## Overview

This document describes the design of the machine learning dataset used in **F1 Strategist**, an end-to-end machine learning application that predicts the number of laps remaining until a driver's next pit stop during a Formula 1 race.

Rather than predicting the absolute pit lap, the model predicts **Laps Until Next Pit Stop**, which creates a more consistent regression problem across races and allows the frontend to compute the recommended pit lap dynamically.

---

# Machine Learning Problem

## Objective

Predict how many laps remain until a driver's next pit stop based on the current race state.

Example

Current Lap: 18

Prediction:

```
Laps Until Pit Stop = 4
```

Frontend computes:

```
Predicted Pit Lap = 18 + 4 = 22
```

---

# Unit of Observation

Each row in the dataset represents:

> **One driver's state during one lap of one Formula 1 race.**

Example

| Season | Race | Driver | Lap | Compound | Tyre Age | Position | Target |
|---------|------|---------|-----|-----------|-----------|------------|---------|
|2024|Canadian GP|VER|18|Medium|16|P2|4|

---

# Target Variable

| Name | Description |
|------|-------------|
| laps_until_pit | Number of laps remaining until the driver's next pit stop |

This is the value our regression model will predict.

---

# Feature Categories

## Driver Features

| Feature | Source | Type | Notes |
|----------|--------|------|------|
| Driver | Results | Categorical | Driver abbreviation |
| Constructor | Results | Categorical | Team name |
| Starting Position | Results | Numerical | Grid position |
| Qualifying Position | Results | Numerical | Qualifying result |

---

## Race Features

| Feature | Source | Type |
|----------|--------|------|
| Season | Session | Numerical |
| Circuit | Session | Categorical |
| Lap Number | Laps | Numerical |

---

## Tire Features

| Feature | Source | Type |
|----------|--------|------|
| Compound | Laps | Categorical |
| Tyre Age | Laps | Numerical |
| Stint Number | Derived | Numerical |
| Number of Previous Pit Stops | Derived | Numerical |

These are expected to be among the most important features.

---

## Pace Features

| Feature | Source | Type |
|----------|--------|------|
| Previous Lap Time | Laps | Numerical |
| Average Lap Time (Last 3 Laps) | Derived | Numerical |
| Average Lap Time (Last 5 Laps) | Derived | Numerical |
| Fastest Lap So Far | Derived | Numerical |

These features help estimate tire degradation.

---

## Position Features

| Feature | Source | Type |
|----------|--------|------|
| Current Position | Laps | Numerical |
| Gap Ahead | Derived | Numerical |
| Gap Behind | Derived | Numerical |

---

## Weather Features

| Feature | Source | Type |
|----------|--------|------|
| Air Temperature | Weather | Numerical |
| Track Temperature | Weather | Numerical |
| Humidity | Weather | Numerical |
| Rainfall | Weather | Boolean |

---

## Race Status Features

| Feature | Source | Type |
|----------|--------|------|
| Track Status | Track Status | Categorical |
| Safety Car Active | Derived | Boolean |
| Virtual Safety Car Active | Derived | Boolean |
| Yellow Flag | Derived | Boolean |

---

# Raw Data Sources

Historical race information will be collected using the FastF1 Python library.

For every race we plan to store:

```
raw/

    2024/

        CanadianGP/

            laps.csv

            weather.csv

            results.csv

            track_status.csv

            race_control.csv
```

The raw data will never be modified.

---

# Processed Dataset

Feature engineering will combine all raw data into a single training dataset.

```
processed/

    training_dataset.csv
```

Each row will contain all engineered features required for model training.

---

# Machine Learning Pipeline

```
FastF1

↓

Download Raw Race Data

↓

Feature Engineering

↓

Training Dataset

↓

Model Training

↓

Model Evaluation

↓

Model Serialization

↓

FastAPI Inference API

↓

React Dashboard
```

---

# Initial Model Candidates

The following models will be evaluated.

- Linear Regression (Baseline)
- Random Forest Regressor
- XGBoost Regressor
- LightGBM Regressor
- CatBoost Regressor

Performance will be compared using regression metrics.

---

# Evaluation Metrics

The following metrics will be used.

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R² Score

Feature importance and prediction explainability will be analyzed using SHAP.

---

# Future Improvements

Potential improvements include:

- Telemetry-based features
- Historical driver performance
- Tire degradation modeling
- Monte Carlo race simulation
- Reinforcement learning strategy optimization
- Live race predictions
- AWS-based MLOps pipeline for automatic model retraining

---

# Current Project Stage

✅ Dataset Design

⬜ Data Collection

⬜ Feature Engineering

⬜ Dataset Construction

⬜ Model Training

⬜ Model Evaluation

⬜ FastAPI Backend

⬜ React Dashboard

⬜ AWS Deployment