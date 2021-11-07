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
        dropout_rate = 0.1
        self.add(layers.Conv3D(16, 1, activation='relu', name="input_layer", input_shape=(12, 110, 110, 3)))
        self.add(layers.MaxPooling3D((1, 2, 2)))
        self.add(layers.Dropout(dropout_rate))

        self.add(layers.Conv3D(32, 3, activation='relu', padding='same'))
        self.add(layers.MaxPooling3D((1, 2, 2)))
        self.add(layers.Dropout(dropout_rate))

        self.add(layers.Conv3D(64, 3, activation='relu', padding='same'))
        self.add(layers.MaxPooling3D((1, 2, 2)))
        self.add(layers.Dropout(dropout_rate))

        #self.add(layers.Conv3D(32, 3, activation='relu', padding='same'))
        #self.add(layers.MaxPooling3D((1, 2, 2)))
        #self.add(layers.Dropout(dropout_rate))

        #self.add(layers.Conv3D(64, 3, activation='relu', padding='same'))
        #self.add(layers.MaxPooling3D((1, 2, 2)))
        #self.add(layers.Dropout(dropout_rate))

        self.add(layers.Flatten())

        self.add(layers.Dense(128, activation="relu", name="hidden_layer1"))
        self.add(layers.Dropout(dropout_rate))

        self.add(layers.Dense(256, activation="relu", name="hidden_layer2"))
        self.add(layers.Dropout(dropout_rate))

        self.add(layers.Dense(512, activation="relu", name="hidden_layer3"))
        self.add(layers.Dropout(dropout_rate))

        self.add(layers.Dense(256, activation="relu", name="hidden_layer4"))
        self.add(layers.Dropout(dropout_rate))

        self.add(layers.Dense(128, activation="relu", name="hidden_layer5"))
        self.add(layers.Dropout(dropout_rate))

        self.add(layers.Dense(1, activation='sigmoid', name="output_layer"))
        self.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True), optimizer='adam',
                     metrics=['accuracy'])
        self.summary()

    def forward(self, sample):
        sample = self.pre_process_data(sample)
        result = [self.predict(np.asarray([s])) for s in sample]
        result = self.post_process_data(result)
        return result

    def pre_process_data(self, data):
        image = data[0]
        image = self.b64toarray(image)
        result = np.zeros((4, 12, 110, 110, 3))
        resi = 0
        for img in data[1]:
            res = self.split_image(image)
            res[11] = self.b64toarray(img)
            result[resi] = res
            resi += 1
        return result

    def b64toarray(self, b64str):
        image = base64.b64decode(b64str)
        image = io.BytesIO(image)
        image = Image.open(image)
        image = np.asarray(image)
        return image

    def split_image(self, image):
        res = np.zeros((12, 110, 110, 3))
        r = 110
        for i in range(4):
            d = image[r * i: r * (i + 1), :, :]
            k = 0
            for j in range(5):
                if j % 2 == 0 and not (j == 4 and i == 3):
                    res[i * 3 + k] = d[:, r * j: r * (j + 1), :]
                    k += 1
        return res

    def post_process_data(self, data):
        print(data)
        return np.argmax(data)

    def save_model(self, save_path):
        self.save_weights(save_path + '/weights')

    def load_model(self, model_path):
        self.load_weights(model_path + "/weights")
