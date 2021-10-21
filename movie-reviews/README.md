# Movie Review Prediction
In this use case you will be presented with 1000 unique reviews of various movies found on <a href="https://www.rottentomatoes.com/">Rotten Tomatoes</a>. Your task is to predict the amount of stars for the given review. See image below for illustration of the concept.

<p align="center">
  <img src="../images/example.png" width=550>
</p>

The stars given are in the interval 0, 0.5, 1, ..., 4.5, 5.


## Evaluation
During the week of competition, you will be able to upload your model and test it against a testset of reviews. The most recent score your model achieves on the testset will be displayed on the scoreboard.

Before the deadline, you will submit your final model, and we will evaluate your model with a set of reviews which is **_DIFFERENT_ FROM THE TESTSET!** It will not be possible to test your model against this final evaluation dataset during the week.

Your model will be evaluated on how close to the accual ratings your predictions are. To be exact, your score is measured as the distance between your prediction and the actual rating. An average for all the 1000 test reviews is calculated and used as your score, the lowest score will grant the most points. i.e. the evaluation metric is mean absolute error.


## Getting started using Emily
Once the repository is cloned, navigate to the folder using a terminal and type:
```
emily open movie-reviews
```
You will be prompted for selecting application. For this use case it might be beneficial to use a Natural Language Processing image, where you can select your prefered deep learning framework. Afterwards you will be asked to mount a data folder for your project. This folder should include your data, for the first run it can empty and you can add data later. Then select an editor of your choice to open the Emily template for the use case. A Docker container with a Python environment will be opened. Some content needs to be downloaded the first time a project is opened, this might take a bit of time.

To take full advantage of Emily and the template, your code for prediction should go in api.py:
```
@app.post('/api/predict', response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:

    # You receive all reviews as plaintext in the request.
    # Return a list of predicted ratings between 1-5 (inclusive).
    # You must return the same number of ratings as there are reviews, and each
    # rating will be associated with the review at the same index in the request list.

    ratings = [random.randint(1, 5) for review in request.reviews]

    return PredictResponse(ratings=ratings)
```
For further details about the recommended structure, see <a href="https://dmiai.dk/guide/">this guide</a>.
You can add new packages to the Python environment by adding the names of the packages to requirements.txt and restarting the project.

## Testing the connection to the API
See <a href="https://dmiai.dk/guide/">this guide</a> for details on how to test your setup before final submission.

## Submission
When you are ready for submission, <a href="https://dmiai.dk/guide/deploy">click here</a> for instructions on how to deploy. Then, head over to the official <a href="https://dmiai.dk/">DM i AI website</a> and submit your model by providing the host address for your API and your UUID obtained during sign up. Make sure that you have tested your connection to the API before you submit!
