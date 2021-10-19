# Racing Track Simulation
In this use case you should implement a model, that can control a car on a highway to avoid obstracles and drive as far as possible within 5000 time steps. You'll recive sensory information from the car and you should predict the next action to perform.
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
The car speed describes the speed of the car in either horizontal or vertical direction and the sensor readings states how close other objects are to the car from either right, left or front of the car `did_crash` is a boolean telling if the car crashed or not. Following actions can be performed `ACCELERATE`, `STEER_RIGHT`, `STEER_LEFT` and `BRAKE` as a response to the sensory information.

## Evaluation


## Getting started using Emily


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

## Submission
