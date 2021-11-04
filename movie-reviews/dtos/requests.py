from typing import List
from pydantic import BaseModel

class PredictRequest(BaseModel):
    reviews: List[str]


class TrainRequest(BaseModel):
    data_path: str
    save_path: str

