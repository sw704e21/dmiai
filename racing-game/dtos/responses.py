from pydantic import BaseModel
from enum import Enum


class ActionType(str, Enum):
    ACCELERATE = 'ACCELERATE'
    DECELERATE = 'DECELERATE'
    STEER_RIGHT = 'STEER_RIGHT'
    STEER_LEFT = 'STEER_LEFT'
    NOTHING = 'NOTHING'

    def to_int(self):
        if self == 'ACCELERATE':
            return 0
        if self == 'DECELERATE':
            return 1
        if self == 'STEER_RIGHT':
            return 2
        if self == 'STEER_LEFT':
            return 3
        if self == 'NOTHING':
            return 4


class PredictResponse(BaseModel):
    action: ActionType
