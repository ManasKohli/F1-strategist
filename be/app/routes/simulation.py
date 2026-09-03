from fastapi import APIRouter, HTTPException, Query
from app.schemas.simulation import SimulationRequest, SimulationResponse
from app.services.simulation import simulation_service
from app.services.data import race_data_service

router = APIRouter(tags=["Simulation"])


@router.get("/drivers")
def get_drivers(race: str = Query(...), lap_number: int | None = Query(None, ge=1)):
    return {"drivers": race_data_service.get_drivers(race, lap_number)}


@router.post("/simulate", response_model=SimulationResponse)
@router.post("/simulation/simulate", response_model=SimulationResponse)
def run_simulation(request: SimulationRequest):

    try:
        result = simulation_service.run_simulation(request)
        return result

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))




