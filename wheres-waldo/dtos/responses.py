from pydantic import BaseModel
from datetime import timedelta


class PredictResponse(BaseModel):
    x: int
    y: int


class TrainResponse(BaseModel):
    model_path: str
    time_elapsed: timedelta
