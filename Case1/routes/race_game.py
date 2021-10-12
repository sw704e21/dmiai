from fastapi import APIRouter
from loguru import logger


router = APIRouter(prefix='/race-game', tags=['race-game'])

@router.get('/health', status_code=204)
async def health_check():
  logger.info('Health check')


@router.post('/predict')
async def predict():
  pass