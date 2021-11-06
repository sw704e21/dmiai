from model import Model
import pandas as pd
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Trainer():

    def train(self, data_path, save_path):
        self.model = Model()
        train_x, train_y = self._pre_process_data(data_path)
        self.model.history = self.model.fit(train_x, train_y, epochs=32, verbose=True, batch_size=16)
        self.model.save_model(save_path)
        train_loss, train_accuracy = self.model.evaluate(train_x, train_y, verbose=True)
        print(f'loss: {train_loss}, accuracy: {train_accuracy}')

    def _pre_process_data(self, data_path):
        df = pd.read_csv(data_path)
        x = []
        y = []
        for row in df.values[::, :5]:
            x.append(self.model.pre_process_data((row[0], [row[i] for i in range(1, 5)])))
        for v in df['truth']:
            a = np.zeros((4))
            a[v] = 1
            y.append(a)
        return np.asarray(x), np.asarray(y)
