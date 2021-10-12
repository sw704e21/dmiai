from pydantic import BaseModel


class RaceGamePredictResponse(BaseModel):
    action: int
