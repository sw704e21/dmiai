from tensorflow import keras

# import keras_retinanet
from keras_retinanet import models
import sys as sys
sys.path.append(r'C:\Users\lasse\Documents\GitHub\DM-i-AI\wheres-waldo\keras-retinanet')
from utils.image import read_image_bgr, preprocess_image, resize_image
from utils.visualization import draw_box, draw_caption
from utils.colors import label_color
from utils.gpu import setup_gpu
from keras_retinanet.models import load_model

# import miscellaneous modules
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time
import image_slicer
import PIL

class Model():
    
    def __init__(self):
        self.image = 0
        self.scale = 0
        self.draw = []
        self.labels_to_name = {}
        self.mapping = [[0, 0], [300, 0], [600, 0], [900, 0], [1200, 0], [0, 300],  [300, 300],  [600, 300],  [900, 300],  [1200, 300], [0, 600],  [300, 600],  [600, 600],  [900, 600],  [1200, 600], [0, 900],  [300, 900],  [600, 900],  [900, 900],  [1200, 900], [0, 1200], [300, 1200], [600, 1200], [900, 1200], [1200, 1200]]
    
    def _postprocess_data(self, samples):
        count = 0
        bstcount = 0
        bestpred = 0
        
        boxes = samples[0]
        preds = samples[1]
        
        print(len(boxes))
        print(len(preds))
        
        print(boxes[0].shape)
        print(preds[0].shape)
        
        print(boxes)
        print(preds)
        
        print("##########")
        
        for sample in samples[1]:
            if sample[1] > bestpred:
                boxes = samples[0][count][0]
                bstcount = count
            count = count + 1
            
        print(boxes)    
        
        x_center = boxes[1] + (boxes[3] - boxes[1]) / 2
        y_center = boxes[0] + (boxes[2] - boxes[0]) / 2

        print(x_center)
        print(y_center)
        
        p = self.mapping[10]
        print(p)
        point = p[0] + x_center, p[1] + y_center
        return point

    def forward(self, sample):
        sample = self._preprocess_data(sample)
        result = self.predict(sample)
        return result

    def predict(self, data):
        labels_to_names = {1: 'Waldo'}
        b = [0, 0, 0, 0]
        for image in data:
            self.draw = image.copy()
            self.draw = cv2.cvtColor(self.draw, cv2.COLOR_BGR2RGB)
            image = preprocess_image(image)
            image, scale = resize_image(image)
            boxes, scores, labels = self.model.predict_on_batch(np.expand_dims(image, axis=0))
            #print("processing time: ", time.time() - start)
            # correct for image scale
            boxes /= scale
            fin = 0
            count = 0

            for box, score, label in zip(boxes[0], scores[0], labels[0]):
                # scores are sorted so we can break
                count = count + 1
                if score < 0.5:
                    break
                color = label_color(label)
                b = box.astype(int)
                sc = score
                box = draw_box(self.draw, b, color=color)

                caption = "{} {:.3f}".format(labels_to_names[label], score)
                draw_caption(self.draw, b, caption)
                
        y_center = b[1] + (b[3] - b[1]) / 2
        x_center = b[0] + (b[2] - b[0]) / 2
        print(sc)
        p = self.mapping[10]
        point = p[0] + x_center, p[1] + y_center
        
        return point
    
    def _preprocess_data(self, data):
        data = np.asarray(data)
        images = []
        r = 300
        #print(data)
        for i in range(5):
            row = data[r * i: r * (i + 1), :, :]
            for j in range(5):
                images.append(row[:, r * j: r * (j + 1), :])
        result = []
        for image in images:
            labels_to_names = {1: 'Waldo'}
            image = preprocess_image(image)
            images, scales = resize_image(image)
            result.append(image)   
        result = np.array(result)
        return result

    def save_model(self, save_path):
        model = load_model(r'\WaldoModel\my_model.h5', backbone_name = 'resnet50')


    def load_model(self, model_path):
        self.model = load_model('./WaldoModel/my_model.h5', backbone_name='resnet50')
