from typing import Optional
from numpy.lib.function_base import vectorize
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

    def to_list_side(self):
        self.left_side = 1000 if self.left_side is None else self.left_side
        self.right_side = 1000 if self.right_side is None else self.right_side

        return [self.left_side, self.left_front, self.right_front, self.right_side, self.right_back,
                self.left_back]

    def to_list_front_and_back(self):

        self.front = 1000 if self.front is None else self.front
        self.back = 1000 if self.back is None else self.back

        return [self.front, self.back]

    def to_list_left_right_front(self):
        self.left_front = 1000 if self.left_front is None else self.left_front
        self.right_front = 1000 if self.right_front is None else self.right_front

        return [self.left_front, self.right_front]

    def to_list_left_right_back(self):
        self.left_back = 1000 if self.left_back is None else self.left_back
        self.right_back = 1000 if self.right_back is None else self.right_back

        return [self.left_back, self.right_back]


class PredictRequest(BaseModel):
    elapsed_time_ms: int
    distance: int
    velocity: Velocity
    sensors: SensorReadings
    did_crash: bool

    def to_list_with_velocity(self):
        self.sensors.left_side = 1000 if self.sensors.left_side is None else self.sensors.left_side
        self.sensors.left_front = 1000 if self.sensors.left_front is None else self.sensors.left_front
        self.sensors.front = 1000 if self.sensors.front is None else self.sensors.front
        self.sensors.right_front = 1000 if self.sensors.right_front is None else self.sensors.right_front
        self.sensors.right_side = 1000 if self.sensors.right_side is None else self.sensors.right_side
        self.sensors.right_back = 1000 if self.sensors.right_back is None else self.sensors.right_back
        self.sensors.back = 1000 if self.sensors.back is None else self.sensors.back
        self.sensors.left_back = 1000 if self.sensors.left_back is None else self.sensors.left_back

        return [self.sensors.left_side, self.sensors.left_front, self.sensors.front,
                self.sensors.right_front, self.sensors.right_side, self.sensors.right_back,
                self.sensors.back, self.sensors.left_back, self.velocity.x, self.velocity.y, self.did_crash]
