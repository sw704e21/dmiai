# Movie Review Prediction
In this use case, you will be presented with 1000 unique reviews of various movies found on <a href="https://www.rottentomatoes.com/">Rotten Tomatoes</a>. Your task is to predict the number of stars for the given review. See the image below for an illustration of the concept.

<p align="center">
  <img src="../images/example.png" width=550>
</p>

The stars given are in the interval 0.5, 1, ..., 4.5, 5. You'll receive a list of 1000 strings, containing a review each. You should return the ratings as a list of floats corresponding to a rating for each review.


## Evaluation
During the week of the competition, you will be able to test your model and test it against a test set of reviews. The most recent score your model achieves on the test set will be displayed on the scoreboard.

Before the deadline, you will submit your final model, and we will evaluate your model with a set of reviews which is **_DIFFERENT_ FROM THE TESTSET!** It will not be possible to test your model against this final evaluation dataset during the week.

Your model will be evaluated on how close to the actual ratings your predictions are. To be exact, your score is measured as the distance between your prediction and the actual rating. An average for all the 1000 test reviews is calculated and used as your score, the lowest score will grant the most points. i.e. the evaluation metric is mean absolute error. The mean absolute error will be scaled such that an MAE score of 4.5 leads to 0 points, and an MAE of 0 gives 100 points.

After evaluation, your final score will be provided. This score can be seen on the <a href="https://amboltio.github.io/DM-i-AI-client/#/leaderboard">leaderboard</a> within 5 minutes.

## Getting started using Emily
Once the repository is cloned, navigate to the folder using a terminal and type:
```
emily open movie-reviews
```
You will be prompted for selecting an application. For this use case, it might be beneficial to use a Natural Language Processing image, where you can select your prefered deep learning framework. Afterwards, you will be asked to mount a data folder for your project. This folder should include your data, for the first run it can empty and you can add data later. Then select an editor of your choice to open the Emily template for the use case. A Docker container with a Python environment will be opened. Some content needs to be downloaded the first time a project is opened, this might take a bit of time.

To take full advantage of Emily and the template, your code for prediction should go in api.py:
```
@app.post('/api/predict', response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:

    # You receive all reviews as plaintext in the request.
    # Return a list of predicted ratings between 0.5-5 (inclusive).
    # You must return the same number of ratings as there are reviews and each
    # rating will be associated with the review at the same index in the request list.

    ratings = [random.randint(1, 5) for review in request.reviews]

    return PredictResponse(ratings=ratings)
```
For further details about the recommended structure, see <a href="https://dmiai.dk/guide/">this guide</a>.
You can add new packages to the Python environment by adding the names of the packages to requirements.txt and restarting the project, or by using pip install on a terminal within the container which will result in the package being installed temporarily i.e. it is not installed if the project is restarted. <br>
In case you need additional debian packages inside your container, for instance, Git, CMAKE, gcc or similar, check <a href="https://github.com/amboltio/emily-cli/wiki/How-to-add-Debian-packages-to-your-project">this guide</a> for installing extra packages.

## Testing the connection to the API
See <a href="https://dmiai.dk/guide/">this guide</a> for details on how to test your setup before final submission.

## Submission
When you are ready for submission, <a href="https://dmiai.dk/guide/deploy">click here</a> for instructions on how to deploy. Then, head over to the <a href="https://amboltio.github.io/DM-i-AI-client/">Submission Form</a> and submit your model by providing the host address for your API and your UUID obtained during sign up. Make sure that you have tested your connection to the API before you submit!<br>
