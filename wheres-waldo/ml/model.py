import pickle
from typing import Any, Tuple

from loguru import logger
from PIL.Image import Image


class Model():

    def __init__(self):
        super().__init__()  # Inherit methods from the super class which this class extends from

    def forward(self, image: Image) -> Tuple[int, int]:
        """
        Processes the input image and produces a prediction tuple of shape (x, y)
        where x and y denote the predicted coordinates of Waldo
        """

        # TODO: Process the image here to produce a prediction of where Waldo is

        x = 176  # Waldo's X-coordinate
        y = 165  # Waldo's Y-coordinate

        return x, y

    def load(self, model_path: str) -> Any:
        logger.info(f'Loading model from {model_path}')

        with open(model_path, 'rb') as fp:
            return pickle.load(fp)

    def save(self, model_path: str) -> None:
        logger.info(f'Saving model to {model_path}')

        with open(model_path, 'wb') as fp:
            pickle.dump(self, fp)

    def __call__(self, image: Image):
        return self.forward(image)
