from pydantic import BaseModel


class PredictResponse(BaseModel):
    next_image_index: int
