"""
The design of this comes from here:
http://outlace.com/Reinforcement-Learning-Part-3/
"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import Callback


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))


class Model(Sequential):
    def __init__(self):
        super().__init__()
        self.epsilon = 1

    def neural_net(self, num_sensors, params, load=''):

        # First layer.
        self.add(Dense(
            params[0], kernel_initializer='lecun_uniform', input_dim=num_sensors
        ))
        self.add(Activation('relu'))
        self.add(Dropout(0.2))

        # Second layer.
        self.add(Dense(params[1], kernel_initializer='lecun_uniform'))
        self.add(Activation('relu'))
        self.add(Dropout(0.2))

        # Output layer.
        self.add(Dense(3, kernel_initializer='lecun_uniform'))
        self.add(Activation('linear'))

        rms = RMSprop()
        self.compile(loss='mse', optimizer=rms)

        if load:
            self.load_weights(load)
