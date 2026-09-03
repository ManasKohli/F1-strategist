# F1 Strategist

F1 Strategist is an end-to-end machine learning application for Formula 1
pit-stop strategy. Given a driver's current race state, the system predicts
the number of laps until the next pit stop and presents the recommendation in
an interactive simulator.

The project combines historical race data, feature engineering, model
training, a FastAPI inference service, and a React frontend. It is designed to
make the full path from raw motorsport data to a usable ML product visible and
reproducible.

## Project Status

| Area | Status |
| --- | --- |
| Feature engineering and dataset pipeline | Complete |
| Random Forest training and evaluation | Complete |
| FastAPI inference API | Complete |
| React strategy simulator | Complete |
| Vercel frontend deployment | Planned |
| Google Cloud Run backend deployment | Planned |

## How It Works

1. Historical Formula 1 race data is transformed into race-state features.
2. A Random Forest Regressor learns patterns in pit-stop timing.
3. The FastAPI service combines historical context with the requested race
	 state and runs the trained model.
4. The React simulator renders the predicted pit lap, remaining laps, and
	 strategy timeline.

The current target is `laps_until_pit`. The model is intentionally scoped to
pit-stop timing and does not yet optimize tyre selection, number of stops, or
expected finishing position.

## Tech Stack

- **Modeling:** Python, pandas, scikit-learn, joblib
- **Data:** FastF1 race data and engineered historical race-state features
- **Backend:** FastAPI, Pydantic, Uvicorn
- **Frontend:** React, Vite, React Router
- **Deployment target:** Vercel for the frontend, Google Cloud Run for the API

## Repository Structure

```text
be/
	app/              FastAPI application, routes, schemas, and services
	data/             Raw and processed datasets
	scripts/          Dataset, training, and evaluation workflow
	trained_models/   Serialized production model
fe/f1/
	src/              React application and simulator components
```

## Run Locally

### Backend

```bash
cd be
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API is available at `http://localhost:8000`. Useful endpoints:

```text
GET  /api/health
GET  /api/drivers?race=Monaco_Grand_Prix&lap_number=25
POST /api/simulate
```

`/api/health` reports model readiness and the number of dataset rows loaded by
the inference service.

### Frontend

```bash
cd fe/f1
npm install
npm run dev
```

The frontend uses `http://localhost:8000` by default. Configure another API
origin with Vite's environment variable:

```bash
VITE_API_URL=https://your-cloud-run-service.run.app npm run dev
```

Production checks:

```bash
npm run build
npm run lint
```

## Reproduce the ML Workflow

From the `be` directory:

```bash
python scripts/build_dataset.py
python scripts/preprocess_training_data.py
python scripts/split_dataset.py
python scripts/train_model.py
python scripts/evaluate_model.py
```

The evaluation script reports MAE, RMSE, and R² on the held-out dataset. The
trained artifact is saved to `be/trained_models/pit_strategy_model.joblib` and
loaded by the API at startup.

### Held-Out Performance

The current model was evaluated on 13,193 held-out 2025 race-state samples
using a model trained on 2024 data:

| Metric | Result |
| --- | ---: |
| Mean absolute error (MAE) | 5.97 laps |
| Root mean squared error (RMSE) | 8.19 laps |
| R² | 0.279 |
| Predictions within ±3 laps | 35.06% |
| Predictions within ±5 laps | 56.02% |
| Predictions within ±10 laps | 83.65% |

Because this is a regression problem, traditional classification accuracy is
not the right measure. The tolerance figures show how often the predicted pit
timing falls within a practical number of laps of the observed target. These
results are a transparent baseline for future feature, model, and strategy
improvements rather than a claim of race-winning optimization.

## Deployment Plan

Deployment is intentionally kept as the next project step rather than being
represented as complete in this repository.

### Frontend: Vercel

1. Import the repository into Vercel.
2. Set the project root to `fe/f1`.
3. Use `npm run build` as the build command.
4. Set the output directory to `dist`.
5. Add `VITE_API_URL` with the deployed Cloud Run service URL.

### Backend: Google Cloud Run

The backend includes a production container definition in `be/Dockerfile`.
From the repository root, a future deployment can follow this shape:

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/f1-strategist-api ./be
gcloud run deploy f1-strategist-api \
	--image gcr.io/PROJECT_ID/f1-strategist-api \
	--platform managed \
	--region REGION \
	--allow-unauthenticated
```

Before going live, update the backend CORS allowlist with the final Vercel
origin, deploy the API, then set that Cloud Run URL as `VITE_API_URL` in Vercel.

## Engineering Notes

- Inference uses the same feature ordering as the trained model contract.
- API validation protects against invalid positions, tyre ages, and race laps.
- Late-race requests use the latest available historical state for the driver
	when an exact lap is not present in the dataset.
- Predictions are constrained to the race distance and explicitly report when
	no pit stop is predicted before the finish.

## Future Work

- Add prediction intervals or calibrated uncertainty.
- Track model versions and evaluation metrics in the UI.
- Compare the model against simple strategy baselines.
- Expand from pit timing to compound choice, pit windows, and expected race
	outcome.
- Add automated backend tests and CI checks.
