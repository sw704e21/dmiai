from typing import List
from fastapi import Request, Response
from fastapi.applications import FastAPI
from loguru import logger
import re

from utilities.logging.config import initialize_logging


def _configure_logging_middleware(exclude_paths: List[str]):
    path_regexes = [re.compile(path) for path in exclude_paths]

    async def _http_request_logging_middleware(request: Request, call_next) -> Response:
        """
        Intercepts all HTTP requests and responses to log rudimentary information.
        The request and response objects are assigned to the record.extra dict.
        """

        # Check if this path is exempted from logging
        for regex in path_regexes:
            if regex.search(request.url.path):
                return await call_next(request)

        # Log request, do work, log response
        logger.info(
            f'HTTP {request.method} for {request.url}', request=request)
        response: Response = await call_next(request)
        logger.info(f'HTTP {response.status_code} for {request.url}',
                    request=request, response=response)

        return response
    return _http_request_logging_middleware


def setup(api: FastAPI, exclude_paths: List[str] = []):
    '''
    Configures logging (loguru.logger) and initialized middleware.
    @param exclude_paths: Path patterns to exclude from logging middleware.
                          For example, exclude_paths=['/api/'] will exempt
                          all requests for http://HOST:PORT/api/* from logging.
    '''
    initialize_logging()
    api.middleware("http")(_configure_logging_middleware(exclude_paths))
