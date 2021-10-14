from pydantic import BaseModel


class IqTestPredictResponse(BaseModel):
    third_image_index: int
