from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
import pickle
from sklearn.feature_extraction.text import CountVectorizer

class Model(Sequential):

    def new(self, input_dim):
        self.input_dim = input_dim
        self.add(layers.Dense(10, input_dim=input_dim, activation='relu'))
        self.add(layers.Dense(64, activation='relu'))
        self.add(layers.Dense(128, activation='relu'))
        self.add(layers.Dense(64, activation='relu'))
        self.add(layers.Dense(1, activation='relu'))
        self.compile(loss='mean_absolute_error', optimizer='adam', metrics=['accuracy'])


    def forward(self, sample):
        sample = self._preprocess_data(sample)
        return self.predict(sample)


    def _preprocess_data(self, data):
        data = self.vectorizer.transform(data)
        return data

    def save_model(self, save_path):
        with open(save_path + "/input_dim", 'wb') as fp:
            pickle.dump(self.input_dim, fp)
        with open(save_path + "/vocabulary", 'wb') as fp:
            pickle.dump(self.vectorizer.vocabulary_, fp)
        self.save_weights(save_path + "/weights.json")


    def load_model(self, model_path):
        with open(model_path + "/input_dim", 'rb') as fp:
            input_dim = pickle.load(fp)
        with open(model_path + "/vocabulary", 'rb') as fp:
            v = pickle.load(fp)
            self.vectorizer = CountVectorizer(vocabulary=v)
        self.new(input_dim)
        self.load_weights(model_path + "/weights.json")

