# from tensorflow import keras
import sys as sys
sys.path.append(r'C:\Users\lasse\Documents\GitHub\DM-i-AI\wheres-waldo\keras-retinanet')
from utils.image import preprocess_image, resize_image
# from utils.visualization import draw_box, draw_caption
from keras_retinanet import models

# import miscellaneous modules
import cv2
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Model():
    def __init__(self):
        self.image = 0
        self.scale = 0
        self.mapping = [[0, 0], [300, 0], [600, 0], [900, 0], [1200, 0], [0, 300], [300, 300], [600, 300], [900, 300],
                        [1200, 300], [0, 600], [300, 600], [600, 600], [900, 600], [1200, 600], [0, 900], [300, 900],
                        [600, 900], [900, 900], [1200, 900], [0, 1200], [300, 1200], [600, 1200], [900, 1200],
                        [1200, 1200]]

    def _postprocess_data(self, samples):
        count = 0
        bstcount = 0
        bestpred = 0
        boxes = [0, 0, 0, 0]
        for sample in samples[1]:
            if sample[1] > bestpred:
                boxes = samples[0][count][0]
                bstcount = count
            count = count + 1

        print(boxes)
        print(bestpred)

        x_center = boxes[1] + (boxes[3] - boxes[1]) / 2
        y_center = boxes[0] + (boxes[2] - boxes[0]) / 2

        print(x_center)
        print(y_center)

        p = self.mapping[bstcount]
        print(p)
        point = int(p[0] + x_center), int(p[1] + y_center)
        return point

    def forward(self, sample):
        images = self._preprocess_data(sample)
        res = self.model.predict_on_batch(images)
        return self._postprocess_data(res)


    def _preprocess_data(self, data):
        # Split billeder i 15 billeder
        data = np.asarray(data)
        images = []
        r = 300
        for i in range(5):
            row = data[r * i: r * (i + 1), :, :]
            for j in range(5):
                images.append(row[:, r * j: r * (j + 1), :])

        result = []
        for image in images:
            draw = image.copy()
            draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
            labels_to_names = {1: 'Waldo'}
            image = preprocess_image(image)
            images, scales = resize_image(image)
            result.append(image)
        result = np.array(result)
        return result

    def save_model(self, save_path):
        pass


    def load_model(self, model_path):
        self.model = models.load_model('./WaldoModel/my_model.h5', backbone_name='resnet50')
