from typing import Literal

from pydantic import BaseModel, Field


class SimulationRequest(BaseModel):
    race: str
    driver: str
    lap_number: int = Field(ge=1)

    position: int = Field(ge=1, le=99)

    compound: str
    tyre_age: int = Field(ge=0, le=100)
    fresh_tyre: bool

    rain_condition: Literal["", "light_rain", "heavy_rain"] = ""

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
    total_laps: int
    pit_before_finish: bool

    


