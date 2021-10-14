from loguru import logger

from ml.model import Model


class Trainer:

    def train(self, model: Model, dataset_path: str) -> Model:
        """
        Trains and returns the model provided using the dataset located at the provided path.
        """
        logger.info(f'Training model using dataset at {dataset_path}...')

        # TODO 1) Load your data
        # TODO 2) Train your model

        return model  # Return the trained model (to be stored by Emily)
