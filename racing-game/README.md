# Racing Track Simulation
In this use case, you should implement a model, that can control a car on a highway to avoid obstacles and drive as far as possible within 5000 time steps. You'll receive sensory information from the car and you should predict the next action to perform. An illustration of the game can be seen in the image below:


<img src="../images/raw.jpg" width=450> <img src="../images/raw_with_drawings.jpg" width=450>


You get the following information in every time step, these are specified in `dtos/requests.py`:
```
game_tick: int
car_speed_horizontal: float
car_speed_vertical: float
front_sensor_reading: float
left_sensor_reading: float
right_sensor_reading: float
did_crash: bool
```
The car speed describes the speed of the car in either horizontal or vertical direction and the sensor readings state how close other objects are to the car from either right, left or front of the car `did_crash` is a boolean telling if the car crashed or not. Following actions can be performed `ACCELERATE`, `STEER_RIGHT`, `STEER_LEFT` and `BRAKE` as a response to the sensory information.

## Evaluation
You'll be rewarded based on how far your model drives your car without crashing into obstacles. We will run the game for a fixed amount of game ticks and based on how far and how long your car survive, you will be granted points.

## Getting started using Emily
Once the repository is cloned, navigate to the folder using a terminal and type:
```
emily open racing-game
```
You'll be prompted for selecting application, and you can select your prefered deep learning framework. Afterwards you will be asked to mount a data folder for your project. This folder should include your data, for the first run it can empty and you can add images later.
Then select an editor of your choice to open the Emily template for use case.  A Docker container with a Python environment will be opened. Some content needs to be downloaded the first time a project is opened, this might take a bit of time.

To take full advantage of Emily and the template, your code for prediction should go in `api.py`:

```
@app.post('/api/predict', response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:

    action = None

    # You receive the entire game state in the request object.
    # Read the game state and decide what to do in the next game tick.

    if request.car_speed_horizontal > 9000:
        action = ActionType.BRAKE
    else:
        action = ActionType.ACCELERATE

    return PredictResponse(
        action=action
    )
```

## Getting started without using Emily



## Testing the connection to the API
See <a href="https://dmiai.dk/guide/">this guide</a> for details on how to test your setup before final submission.

## Submission
When you are ready for submission, <a href="https://dmiai.dk/guide/deploy">click here</a> for instructions on how to deploy. Then, head over to the official <a href="https://dmiai.dk/">DM i AI website</a> and submit your model by providing the host address for your API and your UUID obtained during sign up. Make sure that you have tested your connection to the API before you submit!

