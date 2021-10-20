# Where's Waldo?
Find Waldo in a series of images. Each image contains only one Waldo. Below you can see an example image, together with a bounding box enclosing Waldo. Your task is to predict a point within this bounding box to gain a point. Below you can see an example of what kind of image you can expect together with an image showing the prediction area. <br> <br>
<img src="../images/waldo.jpg" width=450> <img src="../images/waldo_bbox_arrow.jpg" width=450>

During evaluation, you are given a image of size 1500x1500px. Your model then has 10 seconds to return the (x, y) coordinates representing a point where Waldo is visible. All methods for predicting the location of Waldo is allowed in this use case. <br>
The images used for evaluating your final model, consists of images from "Where's Waldo?" books that have been split into 300x300px tiles and put together again randomly. Your model should be robust to changes in scale and image quality! Below you can see how the coordinate system used to determine Waldo's position are oriented. <br>
No training data will be supplied for this use case.
<br><br>

<p align="center">
  <img src="../images/coordinates.jpg" width=500>
</p>


## Evaluation
You will be granted points based on how many images you correctly detect Waldo within the bounding box. The scores are binary meaning that 1 point is given if the prediction is correct and 0 if not. No measure of the exactness of the prediction is used during evaluation. To verify if the prediction is correct, the point should be inside the bounding box, which enclose Waldo.

Notice that you can only submit once for this use case! We encourage you to test your code and API before you submit your final model. You can find the documentation of your API where you can _try out_ images and verify the prediction. <br>
The documentation is by default found at `0.0.0.0:4242/docs`, and then find the prediction endpoint for the use case. <br>

After evaluation, your final score will be provided. This score can be seen on the [leaderboard for this task] within 5 minutes.

Upon completion of the contest, the top 5 highest ranking teams will be asked to submit their training code and the trained models for validation. The final ranking is announced on 30/11. <br> <br>

## Getting started using Emily
Once the repository is cloned, navigate to the folder using a terminal and type:
```
emily open wheres-waldo
```
You'll be prompted for selecting application. For this use case it might be beneficial to use a Computer Vision image, where you can select your prefered deep learning framework. Afterwards you will be asked to mount a data folder for your project. This folder should include your data, for the first run it can be empty and you can add images later.
Then select an editor of your choice to open the Emily template for the use case.  A Docker container with a Python environment will be opened. Some content needs to be downloaded the first time a project is opened, this might take a bit of time.

To take full advantage of Emily and the template, your code for prediction should go in `api.py`:
```
@app.post('/api/predict', response_model=PredictResponse)
def predict(request: PredictRequest = File(...)) -> PredictResponse:

    # This is the Where's Waldo image as an RGB matrix
    image = Image.open(io.BytesIO(request.file.read())).convert("RGB")

    # This is a dummy prediction - compute a real one
    prediction = {
        'x': 130,
        'y': 850
    }

    return PredictResponse(**prediction)
```
For further details about the recommended structure, see <a href="https://dmiai.dk/guide/">this guide</a>.
You can add new packages to the Python environment by adding the names of the packages to requirements.txt and restarting the project.

## Getting started without using Emily
To submit results you need to set up your own API. Somehow idk.
Your API should be set up to return the coordinates with format like:
```
{'x': x, 'y': y}
```

## Testing the connection to the API
See <a href="https://dmiai.dk/guide/">this guide</a> for details on how to test your setup before final submission.

## Submission
When you are ready for submission, <a href="https://dmiai.dk/guide/deploy">click here</a> for instructions on how to deploy. Then, head over to the official <a href="https://dmiai.dk/">DM i AI website</a> and submit your model by providing the host address for your API and your UUID obtained during sign up. Make sure that you have tested your connection to the API before you submit!
