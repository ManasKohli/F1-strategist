from fastapi import APIRouter
from app.schemas.simulation import SimulationRequest
from app.services.simulation import simulation_service

router = APIRouter(tags=["Simulation"])


@router.post("/simulate")
def run_simulation(request: SimulationRequest):
    result = simulation_service.run_simulation(request)

    return {"result": result}




