# Movie Review Prediction
In this use case you will be presented with unique 1000 reviews of various movies found on <a href="https://www.rottentomatoes.com/">Rotten Tomatoes</a>. Your task is to predict the amount of stars this review ended up given the respective movie.

<p align="center">
  <img src="images/example.png" width=550>
</p>




## Evaluation
You will be granted point based on how many images you correctly find Waldo within, the scores are binary meaning that 1 point is given if the prediction is correct and 0 if not. No measure of the exactness of the prediction is used during evaluation. To verify if the prediction is correct, the point should be inside the bounding box, which enclose Waldo.


## Getting started using Emily
Once the repository is cloned, navigate to the folder called Case1 using a terminal and type:
```
emily open .
```
then select an editor of your choice to open the Emily template for use case number 1. A Docker container with a Python environment will be opened. Some content needs to be downloaded the first time a project is opened, this might take a bit of time. 

To take full advantage of Emily and the template, your code for prediction should go in ml/predictor.py:
```
def predict(self, request):
        sample = request.image

        """
        Insert your prediction code here
        """

        x = 176  # Should be replaced with the prediction
        y = 165  # Should be replaced with the prediction

        # Leave this to ensure standardized submission format
        prediction = {'x': x, 'y': y}

        return prediction
```
For further details about the recommended structure, see <a href="https://dmiai.dk/guide/">this guide</a>.
You can add new packages to the Python environment by adding the names of the package to requirements.txt and restarting the project.


## Getting started without using Emily
To submit results you need to set up your own API. Somehow idk.
Your API should be set up to return the coordinates with format like:
```
{'x': x, 'y': y}
```

## Testing the connection to the API
See <a href="https://dmiai.dk/guide/">this guide</a> for details on how to test your setup before final submission.

## Submission
When you are ready for submission, head over to the official <a href="https://dmiai.dk/">DM i AI website</a> and submit your model by providing the host address for your API and your UUID obtained during sign up. Make sure that you have tested your connection to the API before you submit!
