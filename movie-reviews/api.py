
import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse

import middleware.cors
import middleware.logging
from dtos.requests import PredictRequest
from dtos.responses import PredictResponse
from dtos.requests import TrainRequest
from dtos.responses import TrainResponse

from Trainer import Trainer
from Model import Model

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

middleware.logging.setup(app)
middleware.cors.setup(app)


@app.post('/api/predict', response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:

    # You receive all reviews as plaintext in the request.
    # Return a list of predicted ratings between 1-5 (inclusive).
    # You must return the same number of ratings as there are reviews, and each
    # rating will be associated with the review at the same index in the request list.
    m = Model()
    m.load_model('results')
    ratings = m.forward(request.reviews)
    return PredictResponse(ratings=list(ratings))

@app.post('/api/train', response_model=TrainResponse)
def train(request: TrainRequest) -> TrainResponse:
    print(request)
    t = Trainer()
    result = t.train(request.data_path, request.save_path)
    return TrainResponse(train_loss=result['train_loss'], train_accuracy=result['train_accuracy'], test_loss=result['test_loss'], test_accuracy=result['test_accuracy'])


@app.get('/api')
def hello():
    return {
        "uptime": get_uptime(),
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

    print('Hey hey, got update')
    uvicorn.run(
        'api:app',
        host=settings.HOST_IP,
        port=settings.CONTAINER_PORT
    )
