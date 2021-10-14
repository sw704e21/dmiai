from typing import Any, List
from pydantic import BaseModel


class IqTestPredictRequest(BaseModel):
    first_image: Any
    second_image: Any
    third_image_choices: List[Any]
