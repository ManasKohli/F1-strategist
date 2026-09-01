from fastapi import APIRouter

router = APIRouter(tags=["Health"], prefix="/health")


@router.get("/health")
def health_check():
    return {"status": "healthy"}


