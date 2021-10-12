import uvicorn
import os
from PIL import Image
import io
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from argparse import ArgumentParser, _get_action_name

from utilities.utilities import get_uptime
from utilities.logging.config import initialize_logging, initialize_logging_middleware

from static.render import render
from starlette.responses import HTMLResponse

from ml.emily import Emily

import routes.iq_test
import routes.movie_reviews
import routes.race_game
import routes.wheres_waldo

emily = Emily()

# --- Welcome to your Emily API! --- #
# See the README for guides on how to test it.

# Your API endpoints under http://yourdomain/api/...
# are accessible from any origin by default.
# Make sure to restrict access below to origins you
# trust before deploying your API to production.

parser = ArgumentParser()
parser.add_argument('-e', '--env', default='.env',
                    help='sets the environment file')
args = parser.parse_args()
dotenv_file = args.env
load_dotenv(dotenv_file)


app = FastAPI()
app.include_router(routes.iq_test.router)
app.include_router(routes.movie_reviews.router)
app.include_router(routes.race_game.router)
app.include_router(routes.wheres_waldo.router)


initialize_logging()
initialize_logging_middleware(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api')
def health_check():
    return {
        'uptime': get_uptime(),
        'status': 'UP',
        'port': os.environ.get("HOST_PORT"),
    }


@app.get('/')
def index():
    return HTMLResponse(
        render(
            'static/index.html',
            host=os.environ.get('HOST_IP'),
            port=os.environ.get('CONTAINER_PORT')
        )
    )


class PredictItem():
    def __init__(self, image):
        self.image: Image = image


@app.post('/api/predict')
def predict_image(image: UploadFile = File(...)):
    img = Image.open(io.BytesIO(image.file.read())).convert("RGB")
    request = PredictItem(img)
    return emily.predict(request)


if __name__ == '__main__':

    uvicorn.run(
        'api:app',
        host=os.environ.get('HOST_IP'),
        port=int(os.environ.get('CONTAINER_PORT'))
    )
