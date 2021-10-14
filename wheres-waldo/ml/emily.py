
from datetime import datetime
from os import path
from typing import Any, Dict

from dtos.requests import PredictRequest

from ml.model import Model
from ml.predictor import Predictor
from ml.trainer import Trainer


class Emily:

    def __init__(self, model_path: str, dataset_path: str):
        self.model_path = model_path
        self.dataset_path = dataset_path

        self.model = Model()
        self.trainer = Trainer()
        self.predictor = Predictor()

        if model_path is not None and path.exists(model_path):
            self.model.load(model_path)

    def predict(self, request: PredictRequest) -> Dict[str, int]:
        return self.predictor.predict(request, model=self.model)

    def train(self) -> Dict[str, Any]:
        start_time = datetime.now()

        self.model = self.trainer.train(self.model, self.dataset_path)
        self.model.save(self.model_path)

        end_time = datetime.now()

        return {
            'model_path': self.model_path,
            'time_elapsed': end_time - start_time,
        }
