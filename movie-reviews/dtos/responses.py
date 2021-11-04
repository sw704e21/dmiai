from typing import List
from pydantic import BaseModel

class PredictResponse(BaseModel):
    ratings: List[float]

class TrainResponse(BaseModel):
    train_loss: float
    train_accuracy: float
    test_loss: float
    test_accuracy: float
