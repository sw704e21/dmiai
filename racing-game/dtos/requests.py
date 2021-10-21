from typing import Optional
from pydantic import BaseModel


class Velocity(BaseModel):
    x: int
    y: int


class SensorReadings(BaseModel):
    left_side: Optional[int]
    left_front: Optional[int]
    front: Optional[int]
    right_front: Optional[int]
    right_side: Optional[int]
    right_back: Optional[int]
    back: Optional[int]
    left_back: Optional[int]


class PredictRequest(BaseModel):
    elapsed_time_ms: int
    distance: int
    velocity: Velocity
    sensors: SensorReadings
    did_crash: bool
