from typing import List
from pydantic import BaseModel

class PredictRequest(BaseModel):
    game_tick: int
    car_speed_horizontal: float
    car_speed_vertical: float
    front_sensor_reading: float
    left_sensor_reading: float
    right_sensor_reading: float
    did_crash: bool


