import typing
from fastapi import UploadFile


class PredictRequest(UploadFile):
    def __init__(self, filename: str, file: typing.IO = None, content_type: str = "") -> None:
        super().__init__(filename, file=file, content_type=content_type)
