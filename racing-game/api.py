
from loguru import logger
from numpy.lib.function_base import vectorize
import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse, Response

import middleware.cors
import middleware.logging
from dtos.requests import PredictRequest, Velocity
from dtos.responses import PredictResponse, ActionType

from settings import Settings, load_env
from static.render import render
from utilities.utilities import get_uptime
import nn
import learning
import random
import numpy as np
import csv
import os
import pickle

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

load_env()

# --- Welcome to your Emily API! --- #
# See the README for guides on how to test it.

# Your API endpoints under http://yourdomain/api/...
# are accessible from any origin by default.
# Make sure to restrict access below to origins you
# trust before deploying your API to production.

app = FastAPI()
settings = Settings()

middleware.logging.setup(app, exclude_paths=['/api/predict'])
middleware.cors.setup(app)

replay = []  # stores tuples of (S, A, R, S').
data_collect = []
loss_log = []
model = None
NUM_SENSORS = 11
GAMMA = 0.9  # Forgetting
TUNING = False  # If False, just use arbitrary, pre-selected params
nn_param = [128, 128]
params = {
    "batchSize": 64,
    "buffer": 500,
    "nn": nn_param
}
observe = 75  # Number of rames to observe before training

train_frames = 5000
batchSize = params['batchSize']
buffer = params['buffer']


@app.get('/api/save')
def save():
    model = settings.MODEL
    # Save the model every frames.
    model.save_weights('results/saved-models/' + "hej" +
                       '.h5', overwrite=True)
    with open("results/saved-models/epsilon", 'wb') as fp:
        pickle.dump(model.epsilon, fp)
    # print("saving model %s - %d" % (filename, request.elapsed_time_ms))
    with open("results/saved-models/state", 'wb') as fp:
        pickle.dump(model.state, fp)
    return Response()


@app.get('/api/load')
def load():
    model = nn.Model()
    model.neural_net(NUM_SENSORS, params['nn'])
    model.load_weights("results/saved-models/hej.h5")
    with open("results/saved-models/epsilon", 'rb') as fp:
        model.epsilon = pickle.load(fp)
    with open("results/saved-models/state", 'rb') as fp:
        model.state = pickle.load(fp)
    settings.MODEL = model
    return Response()


@app.get('/api/reset')
def reset():
    model = nn.Model()
    model.neural_net(NUM_SENSORS, params['nn'])
    settings.MODEL = model


@app.post('/api/predict', response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    # You receive the entire game state in the request object.
    # Read the game state and decide what to do in the next game tick.

    if request.did_crash:
        logger.info(f'Crashed after {request.elapsed_time_ms} ms')
        logger.info(f'Traveled {request.distance} distance')

    actions = [ActionType.ACCELERATE, ActionType.DECELERATE,
               ActionType.STEER_RIGHT, ActionType.STEER_LEFT,
               ActionType.NOTHING]

    return train(request=request)
    # return PredictResponse(action=ActionType.ACCELERATE)


@app.post('/api/train', response_model=PredictResponse)
def train(request: PredictRequest):
    model = settings.MODEL
    # params = get_params()
    filename = learning.params_to_filename(params)

    actions = [ActionType.ACCELERATE, ActionType.DECELERATE,
               ActionType.STEER_RIGHT, ActionType.STEER_LEFT,
               ActionType.NOTHING]
    # Variables used
    max_car_distance = 0
    print(model.epsilon)
    # Choose an action.
    if random.random() < model.epsilon:
        print("Random action")
        print("startStateCheck: ", model.startStateCheck)
        action = random.choice(actions)
        print(action)
    else:
        print("Decision made")

        # get Q values of reach action.
        qval = model.predict(model.state, batch_size=1)
        print("qval: ", qval)
        action = actions[np.argmax(qval)]
        print("action: ", action)

    # Take action, observe new state and get reward.
    reward, new_state = update_state_and_reward(request=request, model=model)
    print("state: ", model.state, "new state: ", new_state, "reward: ", reward)
    replay.append((model.state, action.to_int(), reward, new_state))
    print("Size of replay: ", len(replay))
    # If we're done observing, start training.
    # if we've stored enough in our buffer, pop the oldest.
    if len(replay) > buffer - 1:
        replay.pop(0)
        print("Training..")
        # randomly sample our experience replay memory
        minibatch = random.sample(replay, batchSize)

        # get training values.
        X_train, y_train = process_minibatch2(minibatch, model)

        # train the model on this batch
        history = nn.LossHistory()
        model.fit(X_train, y_train, batch_size=batchSize,
                  epochs=1, verbose=0, callbacks=[history])
        loss_log.append(history.losses)
    else:
        print("Not training...")

    # Update the starting state S'.
    model.state = new_state

    # Decrement epsilon over time.
    if model.epsilon > 0.1:
        model.epsilon -= (1.0 / train_frames)

    # Car crashed
    if(reward == -500):
        data_collect.append([request.elapsed_time_ms, request.distance])

        if request.distance > max_car_distance:
            max_car_distance = request.distance

            # Time it.
            tot_time = request.elapsed_time_ms

            # Output
            print(
                f'Max: {max_car_distance} at {tot_time, model.epsilon} and distance: {request.distance}')

    # Log results after w're done all frames.
    log_results(filename, data_collect, loss_log)
    settings.MODEL = model
    return get_predicted_response(action)


def get_predicted_response(state):
    return PredictResponse(action=state)


def sum_readings(readings):
    """Sum the number of non-zero readings."""
    tot = 0
    for i in readings:
        tot += i
    return tot


def speed_reward(velocity):
    return velocity * 1


def side_sensors_penalty(sensors):
    sensor_reward_negative = 150
    sensor_close_towall_check = np.any(sensors < sensor_reward_negative)
    p = 3

    print("Is sensor close to wall?: ", sensor_close_towall_check)
    if(sensor_close_towall_check):

        for i in sensors:
            if(i < sensor_reward_negative):
                print(i, ": ", ((sensor_reward_negative - i) * p * -1) / 10)
                return ((150 - i) * p * -1) / 10

            else:
                continue

        return 0
    else:
        return 0


def frontandback_sensors_penalty(sensors):
    tot = 0
    sensor = []
    sensor_reward_negative = 1000
    sensor_close_towall_check = np.any(sensors < sensor_reward_negative)
    p = 1

    print("Is sensor detecting car in front or back?: ", sensor_close_towall_check)
    if(sensor_close_towall_check):

        for i in sensors:
            if(i < sensor_reward_negative):
                print(i, ": ", ((sensor_reward_negative - i) * p * -1) / 10)
                return ((sensor_reward_negative - i) * p * -1) / 10
            else:
                continue

        return 0
    else:
        return 0


@app.post('/api/reward', response_model=PredictResponse)
def update_state_and_reward(request: PredictRequest, model):
    # Get the current location and the readings there.
    sensorsnew = np.array(request.sensors.to_list())
    sensors = np.array([request.sensors.to_list()])
    state = np.array([request.to_list_with_velocity()])
    sensor_sides = np.array(request.sensors.to_list_side())
    sensor_front_and_back = np.array(request.sensors.to_list_front_and_back())
    sensor_left_right_front = np.array(
        request.sensors.to_list_left_right_front())
    sensor_left_right_back = np.array(
        request.sensors.to_list_left_right_back())

    # Set the reward.
    # Car crashed when any reading == 1
    if request.did_crash:
        reward = -500
        model.startStateCheck = True
    else:
        reward = speed_reward(request.velocity.x) + (frontandback_sensors_penalty(sensor_front_and_back) +
                                                     side_sensors_penalty(sensor_sides) +
                                                     side_sensors_penalty(sensor_left_right_front) +
                                                     side_sensors_penalty(sensor_left_right_back))
    # elif request.velocity.x > 10 and request.velocity.x < 20:
    #     reward = 1
    # elif request.velocity.x >= 20 and request.velocity.x < 30:
    #     reward = 2
    # elif request.velocity.x >= 30 and request.velocity.x < 40:
    #     reward = 3
    # elif request.velocity.x >= 40 and request.velocity.x < 50:
    #     reward = 4
    # elif request.velocity.x >= 50 and request.velocity.x < 60:
    #     reward = 5
    # elif request.velocity.x >= 60 and request.velocity.x < 70:
    #     reward = 6
    # elif request.velocity.x > 70:
    #     reward = 7
    # elif request.velocity.x < 10:
    #     reward = -1
    # elif request.velocity.x == 0:
    #     reward = -10
    # else:
    #     reward = -20
    return reward, state


@ app.post('/api/reward', response_model=PredictResponse)
def update_start_state(request: PredictRequest):
    if(request.elapsed_time_ms < 100):
        state = np.array([request.sensors.to_list()])
        return state


def log_results(filename, data_collect, loss_log):
    # Save the results to a file so we can graph it later.
    with open('results/saved-models/' + filename + '.csv', 'w') as data_dump:
        wr = csv.writer(data_dump)
        wr.writerows(data_collect)

    with open('results/saved_models' + filename + '.csv', 'w') as lf:
        wr = csv.writer(lf)
        for loss_item in loss_log:
            wr.writerow(loss_item)


def process_minibatch2(minibatch, model):
    # by Microos, improve this batch processing function
    #   and gain 50~60x faster speed (tested on GTX 1080)
    #   significantly increase the training FPS

    # instead of feeding data to the model one by one,
    #   feed the whole batch is much more efficient

    mb_len = len(minibatch)

    old_states = np.zeros(shape=(mb_len, 11))
    actions = np.zeros(shape=(mb_len,))
    rewards = np.zeros(shape=(mb_len,))
    new_states = np.zeros(shape=(mb_len, 11))

    for i, m in enumerate(minibatch):
        old_state_m, action_m, reward_m, new_state_m = m
        old_states[i, :] = old_state_m[...]
        actions[i] = action_m
        rewards[i] = reward_m
        new_states[i, :] = new_state_m[...]

    old_qvals = model.predict(old_states, batch_size=mb_len)
    new_qvals = model.predict(new_states, batch_size=mb_len)

    maxQs = np.max(new_qvals, axis=1)
    y = old_qvals
    non_term_inds = np.where(rewards != -500)[0]
    term_inds = np.where(rewards == -500)[0]

    y[non_term_inds, actions[non_term_inds].astype(
        int)] = rewards[non_term_inds] + (GAMMA * maxQs[non_term_inds])
    y[term_inds, actions[term_inds].astype(int)] = rewards[term_inds]

    X_train = old_states
    y_train = y
    return X_train, y_train


def process_minibatch(minibatch, model):
    """This does the heavy lifting, aka, the training. It's super jacked."""
    X_train = []
    y_train = []
    # Loop through our batch and create arrays for X and y
    # so that we can fit our model at every step.
    for memory in minibatch:
        # Get stored values.
        old_state_m, action_m, reward_m, new_state_m = memory
        # Get prediction on old state.
        old_qval = model.predict(old_state_m, batch_size=1)
        # Get prediction on new state.
        newQ = model.predict(new_state_m, batch_size=1)
        # Get our predicted best move.
        maxQ = np.max(newQ)
        y = np.zeros((1, 5))
        y[:] = old_qval[:]
        # Check for terminal state.
        if reward_m != -500:  # non-terminal state
            update = (reward_m + (GAMMA * maxQ))
        else:  # terminal state
            update = reward_m
        # Update the value for the action we took.
        y[0][action_m] = update
        X_train.append(old_state_m.reshape(NUM_SENSORS,))
        y_train.append(y.reshape(5,))

    X_train = np.array(X_train)
    y_train = np.array(y_train)

    return X_train, y_train


@ app.get('/api')
def hello():
    return {
        "uptime": get_uptime(),
        "service": settings.COMPOSE_PROJECT_NAME,
    }


@ app.get('/')
def index():
    return HTMLResponse(
        render(
            'static/index.html',
            host=settings.HOST_IP,
            port=settings.CONTAINER_PORT
        )
    )


if __name__ == '__main__':
    uvicorn.run(
        'api:app',
        host=settings.HOST_IP,
        port=settings.CONTAINER_PORT
    )
