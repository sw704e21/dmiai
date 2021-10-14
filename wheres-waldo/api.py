
import uvicorn
from fastapi import FastAPI, File
from starlette.responses import HTMLResponse

import middleware.cors
import middleware.logging

from dtos.requests import PredictRequest
from dtos.responses import PredictResponse, TrainResponse

from ml.emily import Emily
from settings import Settings, load_env
from static.render import render
from utilities.utilities import get_uptime

load_env()

# --- Welcome to your Emily API! --- #
# See the README for guides on how to test it.

# Your API endpoints under http://yourdomain/api/...
# are accessible from any origin by default.
# Make sure to restrict access below to origins you
# trust before deploying your API to production.


app = FastAPI()
settings = Settings()
emily = Emily(
    model_path='wheres-waldo.model.pickle',
    dataset_path='./images'
)


middleware.logging.setup(app)
middleware.cors.setup(app)


@app.post('/api/predict', response_model=PredictResponse)
def predict(request: PredictRequest = File(...)) -> PredictResponse:
    response = emily.predict(request)
    return PredictResponse(**response)


@app.post('/api/train', response_model=TrainResponse)
def train() -> TrainResponse:
    response = emily.train()
    return TrainResponse(**response)


@app.get('/api')
def hello():
    return {
        "uptime": get_uptime(),
        "usecase": "wheres-waldo",
        "service": settings.COMPOSE_PROJECT_NAME,
    }


@app.get('/')
def index():
    return HTMLResponse(
        render(
            'static/index.html',
            host=settings.HOST_IP,
            port=settings.CONTAINER_PORT
        )
    )


if __name__ == '__main__':

    uvicorn.run(
        'api:app',
        host=settings.HOST_IP,
        port=settings.CONTAINER_PORT
    )
