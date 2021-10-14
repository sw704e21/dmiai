import io
from typing import Dict, Tuple

from PIL import Image

from ml.model import Model


class Predictor:
    """
    Predictors are used to wrap internal models in client request/response appropriate processing middleware.
    """

    def predict(self, image: Image, model: Model) -> Dict[str, str]:
        """
        Loads the input image into memory, passes it through the model
        to get a prediction, and returns the prediction as a dictionary object.
        """
        input = self._preprocess(image)
        output = model(input)
        return self._postprocess(output)

    def _preprocess(self, image: Image) -> Image:
        """
        Reads and converts the uploaded image file to an RBG image object
        """
        return Image.open(io.BytesIO(image.file.read())).convert("RGB")

    def _postprocess(self, prediction: Tuple[int, int]) -> Dict[str, int]:
        """
        Converts a prediction tuple (x, y) into its corresponding dictionary representation
        """

        x, y = prediction

        return {
            'x': x,
            'y': y
        }
