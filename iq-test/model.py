from tensorflow.keras import Sequential
from tensorflow.keras import layers
import tensorflow as tf
import pickle
import base64
from scipy import misc
from PIL import Image
import io
import numpy as np


class Model(Sequential):

    def __init__(self):
        super().__init__()
        dropout_rate = 0.01
        self.add(layers.Conv3D(4, 8, activation='relu',
                               input_shape=[115, 115, 12, 3]))
        self.add(layers.MaxPooling3D())
        self.add(layers.Dropout(0.2))
        self.add(layers.Flatten())
        self.add(layers.Dense(256, activation="relu"))
        self.add(layers.Dense(4, activation='relu'))
        self.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), optimizer='adam',
                     metrics=['accuracy'])

    def forward(self, sample):
        sample = self.pre_process_data(sample)
        #result = self.predict(sample)
        #result = self.post_process_data(result)
        return sample

    def pre_process_data(self, data):
        image = data[0]
        imagepng = base64.b64decode(image)
        imagebytes = io.BytesIO(imagepng)
        imageopen = Image.open(imagebytes)
        result = np.asarray(imageopen)
        print(result.shape)
        data = np.zeros((8, 110, 110, 3))
        r = 110
        for i in range(4):
            for j in range(5):
                None

        return result

    def post_process_data(self, data):
        return data

    def save_model(self, save_path):
        self.save_weights(save_path + '/weights')

    def load_model(self, model_path):
        self.load_weights(model_path + "/weights")
