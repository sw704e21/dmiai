# Where's Waldo?
Find Waldo in a series of images, each image contains only one Waldo. Below you can see an example image, together with a bounding box enclosing Waldo. You have to predict a point within this bounding box to gain a point. <br> <br>
<img src="images/waldo.jpg" width=450> <img src="images/waldo_bbox.jpg" width=450>

During evaluation, you are given a .jpg image of size 1500x1500. Your model has 10 seconds to return the (x, y) coordinates to a point where Waldo is visible. All methods are allowed. The testing dataset consists of images from "Where's Waldo?" books that have been split into tiles and put together again randomly.
There is no training dataset. Your model should be robust to changes in scale and image quality.

Scores are binary - if the point given by your model is within a close-cropped rectangular bounding box of Waldo, a point is given.

You can only submit your model once! We encourage you to test your code using the docs for this task before you submit your final model.

After evaluation, your final score will be provided. This score can be seen on the [leaderboard for this task] within 5 minutes.

Upon completion of the contest, the top 5 highest ranking teams will be asked to submit their training code and the trained models for validation. The final ranking is announced on [date]. <br> <br>
<img src="images/coordinates.jpg" width=450 align="middle">


## Getting started using Emily
Once the repository is cloned, navitage to the folder containing use case 1, using a terminal and type:
```
emily open .
```
To open the Emily template for use case 1, and select an editor of your choice. First time, this might take a while, because content needs to be downloaded.

Fill in the code in bla bla bla.py

Look at this guide for further detail




## Submission
When you are ready for submission, head over to the official <a href="https://dmiai.dk/">DM i AI website</a> and submit your model by providing the host address for your API and your UUID obtained during sign up. Make sure that you have tested your connection to the API before you submit!
