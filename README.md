# F1 Strategist

F1 Strategist is a production-deployed machine learning application for
predicting Formula 1 pit-stop timing. A user enters a driver's current race
state and receives a predicted pit window, projected pit lap, and strategy
summary through an interactive simulator.

The project demonstrates the complete path from motorsport data and feature
engineering to model training, API design, containerization, and cloud
deployment.

## Live Application

- **Frontend:** [f1-strategist-one.vercel.app](https://f1-strategist-one.vercel.app/)
- **Backend API:** [Cloud Run service](https://f1-strategist-api-6fxa5vsapa-uc.a.run.app)
- **API health check:** [/api/health](https://f1-strategist-api-6fxa5vsapa-uc.a.run.app/api/health)

The production API currently reports a loaded model and 25,653 dataset rows.

## Product Overview

The simulator combines:

- Historical race-state data from Formula 1 sessions
- Engineered pace, tyre, weather, race-progress, and safety-car features
- A scikit-learn Random Forest regression model
- A FastAPI inference service with validation and CORS support
- A React/Vite interface for exploring race scenarios

The current prediction target is `laps_until_pit`. The model is intentionally
scoped to pit-stop timing; it does not claim to optimize tyre compound choice,
the number of stops, or final finishing position.

## Architecture

```text
Historical race data
        |
        v
Feature engineering and preprocessing
        |
        v
Random Forest model (.joblib)
        |
        v
FastAPI inference service + training dataset
        |
        v
React/Vite simulator
```

The frontend is deployed on Vercel and the containerized backend is deployed
on Google Cloud Run. The frontend receives the API origin through the
`VITE_API_URL` environment variable. The backend receives the allowed frontend
origins through `FRONTEND_URLS`.

## Technical Highlights

- End-to-end ML workflow with reproducible dataset and training scripts
- Explicit model feature contract shared by training and inference
- Request validation with Pydantic constraints for race state inputs
- Fallback to the latest earlier race state when an exact lap is unavailable
- Race-distance-aware predictions that prevent pit laps beyond the finish
- Rule-based overrides for red flags, safety cars, VSCs, and wet conditions
- Dockerized FastAPI service with a health endpoint for deployment checks
- Responsive React simulator with loading, error, and result states

## Model Evaluation

The current baseline was evaluated on 13,193 held-out 2025 race-state samples
using a model trained on 2024 data:

| Metric | Result |
| --- | ---: |
| Mean absolute error (MAE) | 5.97 laps |
| Root mean squared error (RMSE) | 8.19 laps |
| R² | 0.279 |
| Predictions within ±3 laps | 35.06% |
| Predictions within ±5 laps | 56.02% |
| Predictions within ±10 laps | 83.65% |

These results are presented as a transparent baseline for future model and
strategy improvements, not as a claim of race-winning optimization.

## Repository Structure

```text
be/
  app/
    main.py                 FastAPI application and CORS configuration
    routes/                 Health, driver, and simulation endpoints
    schemas/                Pydantic request and response models
    services/               Data loading, prediction, and simulation logic
  data/                     Raw, cached, and processed datasets
  scripts/                  Dataset, training, and evaluation scripts
  trained_models/           Serialized model artifact
  Dockerfile                Cloud Run container definition
fe/f1/
  src/
    components/             Landing page and simulator components
    pages/                  Project, model, and simulator pages
    styles/                 Page and component styles
  package.json              Frontend scripts and dependencies
  vite.config.js            Vite configuration
```

## Run Locally

### Backend

From the repository root:

```bash
cd be
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API runs at `http://localhost:8000`.

### Frontend

In a second terminal:

```bash
cd fe/f1
npm install
npm run dev
```

The frontend defaults to `http://localhost:8000` for its API. To use another
API origin, create `fe/f1/.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

Production frontend checks:

```bash
npm run build
npm run lint
```

## API

### Health

```http
GET /api/health
```

Example response:

```json
{
  "status": "healthy",
  "model_loaded": true,
  "dataset_rows": 25653
}
```

### Drivers

```http
GET /api/drivers?race=Monaco_Grand_Prix&lap_number=25
```

### Simulate

```http
POST /api/simulate
Content-Type: application/json
```

Example request:

```json
{
  "race": "Monaco_Grand_Prix",
  "driver": "LEC",
  "lap_number": 25,
  "position": 3,
  "compound": "HARD",
  "tyre_age": 3,
  "fresh_tyre": false,
  "rain_condition": "",
  "safety_car_active": false,
  "vsc_active": false,
  "yellow_flag": false,
  "red_flag_active": false
}
```

The response includes `laps_until_pit`, `predicted_pit_lap`, `total_laps`, and
whether a pit stop is recommended before the finish.

## Reproduce the ML Workflow

From the `be` directory:

```bash
python scripts/build_dataset.py
python scripts/preprocess_training_data.py
python scripts/split_dataset.py
python scripts/train_model.py
python scripts/evaluate_model.py
```

The trained artifact is written to:

```text
be/trained_models/pit_strategy_model.joblib
```

## Deployment

### Frontend: Vercel

Configure the Vercel project with:

```text
Root directory: fe/f1
Build command: npm run build
Output directory: dist
Environment: Production
Variable: VITE_API_URL
Value: https://f1-strategist-api-6fxa5vsapa-uc.a.run.app
```

`VITE_API_URL` is a public frontend configuration value, not a secret. Vite
embeds `VITE_*` variables in the browser bundle, so credentials must never be
stored in them.

### Backend: Google Cloud Run

From the repository root:

```bash
gcloud config set project YOUR_GCP_PROJECT_ID
gcloud run deploy f1-strategist-api \
  --source ./be \
  --region us-central1 \
  --port 8000 \
  --memory 1Gi \
  --allow-unauthenticated
```

The backend uses `1Gi` of memory because loading pandas, the processed dataset,
and the serialized model exceeds Cloud Run's default `512Mi` limit.

After the frontend is deployed, configure its origin for backend CORS:

```bash
gcloud run services update f1-strategist-api \
  --region us-central1 \
  --update-env-vars FRONTEND_URLS=https://f1-strategist-one.vercel.app
```

Multiple origins can be provided as a comma-separated value. Local Vite ports
remain allowed automatically.

## Project Status

| Area | Status |
| --- | --- |
| Data pipeline and feature engineering | Complete |
| Model training and evaluation | Complete |
| FastAPI inference API | Complete |
| React simulator | Complete |
| Vercel frontend deployment | Complete |
| Google Cloud Run backend deployment | Complete |

## Next Iterations

- Add prediction intervals or calibrated uncertainty
- Compare model predictions with simple strategy baselines
- Expand from pit timing to compound choice and pit-window optimization
- Track model versions and evaluation metrics in the UI
- Add automated backend integration tests and CI checks
