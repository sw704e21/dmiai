import io
from PIL import Image
from fastapi import APIRouter, File
from loguru import logger
from cases.wheres_waldo.ml.emily import Emily

from cases.wheres_waldo.dtos.requests import WheresWaldoPredictRequest
from cases.wheres_waldo.dtos.responses import WheresWaldoPredictResponse


emily = Emily()
path = APIRouter(prefix='/wheres-waldo', tags=['wheres-waldo'])


@path.get('/health', status_code=204)
async def health_check():
    logger.info('Health check')


@path.post('/predict', response_model=WheresWaldoPredictResponse)
async def predict(image: WheresWaldoPredictRequest = File(...)) -> WheresWaldoPredictResponse:
    img = Image.open(io.BytesIO(image.file.read())).convert("RGB")
    prediction = emily.predict(img)
    return WheresWaldoPredictResponse(**prediction)
