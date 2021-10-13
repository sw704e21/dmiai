from fastapi import APIRouter
from loguru import logger

from cases.movie_reviews.dtos.requests import MovieReviewsPredictRequest
from cases.movie_reviews.dtos.responses import MovieReviewsPredictResponse


path = APIRouter(prefix='/movie-reviews', tags=['movie-reviews'])


@path.get('/health', status_code=204)
async def health_check():
    logger.info('Health check')


@path.post('/predict', response_model=MovieReviewsPredictResponse)
async def predict(request: MovieReviewsPredictRequest) -> MovieReviewsPredictResponse:
    pass
