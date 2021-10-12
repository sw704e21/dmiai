import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse

import cases.iq_test.router
import cases.movie_reviews.router
import cases.race_game.router
import cases.wheres_waldo.router

import middleware.cors
import middleware.logging

import routing

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

# Middleware
middleware.logging.setup(app)
middleware.cors.setup(app)

# Routing
routing.setup(
    app,
    prefix='/api',
    routers=[
        cases.iq_test.router.path,
        cases.movie_reviews.router.path,
        cases.race_game.router.path,
        cases.wheres_waldo.router.path,
    ]
)


@app.get('/api')
def hello():
    return {
        "service": settings.COMPOSE_PROJECT_NAME,
        "uptime": get_uptime()
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
