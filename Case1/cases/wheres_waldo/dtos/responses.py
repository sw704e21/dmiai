from pydantic import BaseModel


class WheresWaldoPredictResponse(BaseModel):
    x: int
    y: int
