from typing import List
from pydantic import BaseModel


class MovieReviewsPredictRequest(BaseModel):
    movies_reviews: List[str]
