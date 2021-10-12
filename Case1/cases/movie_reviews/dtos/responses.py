from typing import List
from pydantic import BaseModel


class MovieReviewsPredictResponse(BaseModel):
    movie_review_ratings: List[int]
