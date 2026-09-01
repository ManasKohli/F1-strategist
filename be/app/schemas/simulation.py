from pydantic import BaseModel


class SimulationRequest(BaseModel):
    race: str
    driver: str
    lap_number: int

    position: int

    compound: str
    tyre_age: int
    fresh_tyre: bool

    safety_car_active: bool
    vsc_active: bool
    yellow_flag: bool
    red_flag_active: bool

class SimulationResponse(BaseModel):
    race: str
    driver: str
    current_lap: int
    laps_until_pit: int
    predicted_pit_lap: int

    


