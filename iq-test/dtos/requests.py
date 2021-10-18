from typing import List
from pydantic import BaseModel

class PredictRequest(BaseModel):
    image_1_base64: str
    image_2_base64: str
    image_3_choices_base64: List[str]

