from fastapi import APIRouter, HTTPException
from app.schemas.simulation import SimulationRequest, SimulationResponse
from app.services.simulation import simulation_service

router = APIRouter(tags=["Simulation"], prefix="/simulation")


@router.post("/simulate", response_model=SimulationResponse)
def run_simulation(request: SimulationRequest):

    try:
        result = simulation_service.run_simulation(request)
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))




