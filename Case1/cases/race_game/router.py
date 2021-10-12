from fastapi import APIRouter
from loguru import logger

from cases.race_game.dtos.requests import RaceGamePredictRequest
from cases.race_game.dtos.responses import RaceGamePredictResponse


path = APIRouter(prefix='/race-game', tags=['race-game'])


@path.get('/health', status_code=204)
async def health_check():
    logger.info('Health check')


@path.post('/predict', response_model=RaceGamePredictResponse)
async def predict(request: RaceGamePredictRequest) -> RaceGamePredictResponse:
    pass
