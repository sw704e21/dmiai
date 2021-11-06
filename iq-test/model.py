from tensorflow.keras import Sequential
from tensorflow.keras import layers
from tensorflow.keras.preprocessing import image as kerasimage
import tensorflow as tf
import base64
from PIL import Image
import io
import numpy as np


class Model(Sequential):

    def __init__(self):
        super().__init__()
        self.add(layers.Conv3D(4, 8, activation='relu',
                               input_shape=[15, 110, 110, 3], name="input_layer"))
        self.add(layers.MaxPooling3D())
        self.add(layers.Dropout(0.2))
        self.add(layers.Flatten())
        self.add(layers.Dense(256, activation="relu", name="hidden_layer1"))
        self.add(layers.Dense(4, activation='sigmoid', name="output_layer"))
        self.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True), optimizer='adam',
                     metrics=['accuracy'])

    def forward(self, sample):
        sample = self.pre_process_data(sample)
        result = self.predict(np.asarray([sample]))
        result = self.post_process_data(result)
        return result

    def pre_process_data(self, data):
        image = data[0]
        image = base64.b64decode(image)
        image = io.BytesIO(image)
        image = Image.open(image)
        image = np.asarray(image)
        result = np.zeros((15, 110, 110, 3))
        r = 110
        for i in range(4):
            d = image[r * i: r * (i + 1), :, :]
            k = 0
            for j in range(5):
                if j % 2 == 0 and not (j == 4 and i == 3):
                    result[i * 3 + k] = d[:, r * j: r * (j + 1), :]
                    k += 1
        i = 11
        for image in data[1]:
            image = base64.b64decode(image)
            image = io.BytesIO(image)
            image = Image.open(image)
            image = np.asarray(image)
            result[i] = image
            i += 1
        i = 0
        for image in result:
            img = kerasimage.array_to_img(image)
            img.save("data/test" + str(i) + ".jpg")
            i += 1
        return result

    def post_process_data(self, data):
        return np.argmax(data)

    def save_model(self, save_path):
        self.save_weights(save_path + '/weights')

    def load_model(self, model_path):
        self.load_weights(model_path + "/weights")
