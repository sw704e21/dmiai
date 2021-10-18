from pydantic import BaseModel
from enum import Enum

class ActionType(str, Enum):
    ACCELERATE = 'ACCELERATE'
    STEER_RIGHT = 'STEER_RIGHT'
    STEER_LEFT = 'STEER_LEFT'
    BRAKE = 'BRAKE'

class PredictResponse(BaseModel):
    action: ActionType
