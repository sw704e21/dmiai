# Movie Review Prediction
In this use case you will be presented with unique 1000 reviews of various movies found on <a href="https://www.rottentomatoes.com/">Rotten Tomatoes</a>. Your task is to predict the amount of stars this review ended up given the respective movie. See image below for illustration of the concept.

<p align="center">
  <img src="images/example.png" width=550>
</p>

The stars given are in the interval 0.5, 1, ..., 4.5, 5. Your model needs to round to the nearest half.


## Evaluation
TBD


## Getting started using Emily
Once the repository is cloned, navigate to the folder called Case2 using a terminal and type:
```
emily open .
```
then select an editor of your choice to open the Emily template for use case number 1. A Docker container with a Python environment will be opened. Some content needs to be downloaded the first time a project is opened, this might take a bit of time. 

To take full advantage of Emily and the template, your code for prediction should go in ml/predictor.py:
```
  def predict(self, request):
      # Unpack request
      sentence = request.sentence
      
      """
      Insert your prediction code here
      """

      prediction = 3.5  # Should be replaced with the prediction
      return prediction
```
For further details about the recommended structure, see <a href="https://dmiai.dk/guide/">this guide</a>.
You can add new packages to the Python environment by adding the names of the package to requirements.txt and restarting the project.


## Getting started without using Emily
TBD

## Testing the connection to the API
See <a href="https://dmiai.dk/guide/">this guide</a> for details on how to test your setup before final submission.

## Submission
When you are ready for submission, head over to the official <a href="https://dmiai.dk/">DM i AI website</a> and submit your model by providing the host address for your API and your UUID obtained during sign up. Make sure that you have tested your connection to the API before you submit!
