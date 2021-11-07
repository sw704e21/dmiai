from model import Model
import pandas as pd
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Trainer():

    def train(self, data_path, save_path):
        self.model = Model()
        train_x, train_y = self._pre_process_data(data_path)
        self.model.history = self.model.fit(train_x, train_y, epochs=32, verbose=True, batch_size=4)
        self.model.save_model(save_path)
        train_loss, train_accuracy = self.model.evaluate(train_x, train_y, verbose=True)
        print(f'loss: {train_loss}, accuracy: {train_accuracy}')

    def _pre_process_data(self, data_path):
        df = pd.read_csv(data_path)
        x = []
        for row in df.values[::, :2]:
            a = self.model.split_image(self.model.b64toarray(row[0]))
            a[11] = self.model.b64toarray(row[1])
            x.append(a)
        y = df['truth']
        return np.asarray(x), np.asarray(y)
