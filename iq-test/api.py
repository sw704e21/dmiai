
import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse, Response

import middleware.cors
import middleware.logging
from dtos.requests import PredictRequest
from dtos.responses import PredictResponse

from settings import Settings, load_env
from static.render import render
from utilities.utilities import get_uptime
import random
import csv
from model import Model

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

    # You receive image in base64 encoding.
    image = request.image_base64
    choices = request.image_choices_base64

    # with open("data/data/train.csv", 'a', newline='') as file:
    #     writer = csv.writer(file, delimiter=',')
    #     row = [image]
    #     row.extend(choices)
    #     writer.writerow(row)

    # Process the first two images, and predict the next correct image
    # from the list of image choices
    # Dummy prediction - chooses a random image from the list of choices
    #next_image_index = random.choice([index for index in range(len(choices))])

    model = Model()
    res = model.forward((image, choices))

    return Response()


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

    uvicorn.run(
        'api:app',
        host=settings.HOST_IP,
        port=settings.CONTAINER_PORT
    )
