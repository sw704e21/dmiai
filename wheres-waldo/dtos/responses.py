from pydantic import BaseModel


class PredictResponse(BaseModel):
    x: int
    y: int
