# Where's Waldo?
Find Waldo in a series of images, each image contains only one Waldo. Below you can see an example image, together with a bounding box enclosing Waldo. You have to predict a point within this bounding box to gain a point. <br> <br>
<img src="images/waldo.jpg" width=450> <img src="images/waldo_bbox.jpg" width=450>

During evaluation, you are given a .jpg image of size 1500x1500px. Your model has 10 seconds to return the (x, y) coordinates to a point where Waldo is visible (see image below). All methods are allowed. The testing dataset consists of images from "Where's Waldo?" books that have been split into 300x300px tiles and put together again randomly.
There is no training dataset. Your model should be robust to changes in scale and image quality.
<br><br>
<img src="images/coordinates.jpg" width=450 align="middle">

Scores are binary - if the point given by your model is within a close-cropped rectangular bounding box of Waldo, a point is given. One point can be given per test image.

You can only submit your model once! We encourage you to test your code using the docs for this task before you submit your final model.

After evaluation, your final score will be provided. This score can be seen on the [leaderboard for this task] within 5 minutes.

Upon completion of the contest, the top 5 highest ranking teams will be asked to submit their training code and the trained models for validation. The final ranking is announced on [date]. <br> <br>



## Getting started using Emily
Once the repository is cloned, navigate to the folder called Case1 using a terminal and type:
```
emily open .
```
then select an editor of your choice to open the Emily template for use case 1. A Docker container with a Python environment will be opened. Some content needs to be downloaded the first time a project is opened, this might take a bit of time. 

To take full advantage of Emily and the template, your prediction code should go in ml/predictor.py:
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
You can add new packages to the Python environment by adding the names to requirements.txt and restarting the project.

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
