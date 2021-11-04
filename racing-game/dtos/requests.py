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

    def to_list(self):
        self.left_side = 1000 if self.left_side is None else self.left_side
        self.left_front = 1000 if self.left_front is None else self.left_front
        self.front = 1000 if self.front is None else self.front
        self.right_front = 1000 if self.right_front is None else self.right_front
        self.right_side = 1000 if self.right_side is None else self.right_side
        self.right_back = 1000 if self.right_back is None else self.right_back
        self.back = 1000 if self.back is None else self.back
        self.left_back = 1000 if self.left_back is None else self.left_back

        return [self.left_side, self.left_front, self.front, self.right_front, self.right_side, self.right_back,
                self.back, self.left_back]


class PredictRequest(BaseModel):
    elapsed_time_ms: int
    distance: int
    velocity: Velocity
    sensors: SensorReadings
    did_crash: bool
