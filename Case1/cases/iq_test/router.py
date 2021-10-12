from fastapi import APIRouter
from loguru import logger

from cases.iq_test.dtos.requests import IqTestPredictRequest
from cases.iq_test.dtos.responses import IqTestPredictResponse


path = APIRouter(prefix='/iq-test', tags=['iq-test'])


@path.get('/health', status_code=204)
async def health_check():
    logger.info('Health check')


@path.post('/predict', response_model=IqTestPredictResponse)
async def predict(request: IqTestPredictRequest) -> IqTestPredictResponse:
    pass
