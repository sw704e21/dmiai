from tensorflow.keras import Sequential
from tensorflow.keras import layers
import tensorflow as tf
import pickle

class Model(Sequential):

    def __init__(self):
        super().__init__()
        dropout_rate = 0.01
        self.add(layers.Conv3D(4, 8, activation='relu', input_shape=[115, 115, 12, 3]))
        self.add(layers.MaxPooling3D())
        self.add(layers.Dropout(0.2))
        self.add(layers.Flatten())
        self.add(layers.Dense(256, activation="relu"))
        self.add(layers.Dense(4, activation='relu'))
        self.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer='adam',
                     metrics=['accuracy'])


    def forward(self, sample):
        sample = self.pre_process_data(sample)
        result = self.predict(sample)
        result = self.post_process_data(result)
        return result

    def pre_process_data(self, data):
        return data

    def post_process_data(self, data):
        return data

    def save_model(self, save_path):
        self.save_weights(save_path + '/weights')

    def load_model(self, model_path):
        self.load_weights(model_path + "/weights")
