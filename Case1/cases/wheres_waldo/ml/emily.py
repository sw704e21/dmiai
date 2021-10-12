from cases.wheres_waldo.ml.predictor import Predictor


class Emily:
    """
    The Emily class is simply a wrapper class which creates instances of:
    - The Predictor class (see ml.predictor.py)  # Used for making predictions with a trained model

    """

    def __init__(self):
        self.predictor = Predictor()    # Creates instance of the Predictor class

    def predict(self, request):
        """
        This function calls the __call__ function from the Predictor class in ml.predictor.py.
        Make sure the __call__ method is implemented correctly
        """
        return self.predictor(request)
