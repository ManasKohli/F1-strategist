from fastapi import APIRouter
from app.services.data import race_data_service
from app.services.predictor import predictor

router = APIRouter(tags=["Health"], prefix="/health")


@router.get("")
@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": predictor.model is not None,
        "dataset_rows": len(race_data_service.data),
    }


