from typing import List
from pydantic import BaseModel

class PredictRequest(BaseModel):
    image_base64: str
    image_choices_base64: List[str]

