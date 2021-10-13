from typing import List
from fastapi import FastAPI
from fastapi.routing import APIRouter


def setup(api: FastAPI, routers: List[APIRouter] = [], prefix='/api'):
    for router in routers:
        api.include_router(router, prefix=prefix)
