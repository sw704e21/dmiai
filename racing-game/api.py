
from loguru import logger
import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse

import middleware.cors
import middleware.logging
from dtos.requests import PredictRequest
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
NUM_SENSORS = 8
GAMMA = 0.9  # Forgetting
TUNING = False  # If False, just use arbitrary, pre-selected params


@app.post('/api/predict', response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    # You receive the entire game state in the request object.
    # Read the game state and decide what to do in the next game tick.

    if request.did_crash:
        logger.info(f'Crashed after {request.elapsed_time_ms} ms')
        logger.info(f'Traveled {request.distance} distance')

    actions = [ActionType.ACCELERATE, ActionType.DECELERATE,
               ActionType.STEER_LEFT, ActionType.STEER_RIGHT,
               ActionType.NOTHING]

    return train(request=request)
    # return PredictResponse(action=ActionType.ACCELERATE)


@app.post('/api/train', response_model=PredictResponse)
def train(request: PredictRequest):
    nn_param = [128, 128]
    params = {
        "batchSize": 32,
        "buffer": 1000,
        "nn": nn_param
    }
    model = nn.Model()
    model.neural_net(NUM_SENSORS, params['nn'])
    # params = get_params()
    filename = learning.params_to_filename(params)
    observe = 50  # Number of rames to observe before training
    model.load_weights("results/saved-models/hej.h5")
    with open("results/saved-models/epsilon", 'rb') as fp:
        model.epsilon = pickle.load(fp)
    train_frames = 800
    batchSize = params['batchSize']
    buffer = params['buffer']

    if(model.startStateCheck is True):
        _, state = update_state_and_reward(request=request, model=model)
        model.startStateCheck = False

    # Variables used
    max_car_distance = 0

    actions = [ActionType.ACCELERATE, ActionType.DECELERATE,
               ActionType.STEER_LEFT, ActionType.STEER_RIGHT,
               ActionType.NOTHING]

    print(model.epsilon)
    # Choose an action.
    if random.random() < model.epsilon:
        print("Random action")
        action = random.choice([random.choice(actions), actions[0]])
        print(action)
    else:
        print("Decision made")
        print("state: ", state)
        # get Q values of reach action.
        qval = model.predict(state, batch_size=1)
        print("qval: ", qval)
        action = actions[np.argmax(qval)]
        print("action: ", action)

    # Take action, observe new state and get reward.
    reward, new_state = update_state_and_reward(request=request, model=model)

    replay.append((state, action.to_int(), reward, new_state))
    print("Size of replay: ", len(replay))
    # If we're done observing, start training.
    if request.elapsed_time_ms > observe:
        # if we've stored enough in our buffer, pop the oldest.
        if len(replay) > buffer:
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
    state = new_state

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

    # Save the model every frames.
    model.save_weights('results/saved-models/' + "hej" +
                       '.h5', overwrite=True)
    with open("results/saved-models/epsilon", 'wb') as fp:
        pickle.dump(model.epsilon, fp)
    print("saving model %s - %d" % (filename, request.elapsed_time_ms))

    # Log results after w're done all frames.
    log_results(filename, data_collect, loss_log)

    return get_predicted_response(action)


def get_predicted_response(state):
    return PredictResponse(action=state)


@app.post('/api/reward', response_model=PredictResponse)
def update_state_and_reward(request: PredictRequest, model):
    # Get the current location and the readings there.
    state = np.array([request.sensors.to_list()])
    # Set the reward.
    # Car crashed when any reading == 1
    if request.distance <= 1:
        model.epsilon = 1
    if request.did_crash:
        model.epsilon = 1
        reward = -500
    elif request.velocity.x > 10:
        reward = 1
    elif request.velocity.x > 20:
        reward = 2
    elif request.velocity.x > 30:
        reward = 3
    elif request.velocity.x == 0:
        reward = -2
    else:
        reward = -1

    return reward, state


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

    old_states = np.zeros(shape=(mb_len, 8))
    actions = np.zeros(shape=(mb_len,))
    rewards = np.zeros(shape=(mb_len,))
    new_states = np.zeros(shape=(mb_len, 8))

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
