from Model import Model
import pandas
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

class Trainer:

    def __init__(self, model_path=None):
        if model_path is not None:
            self.model.load_model(model_path)
        else:
            self.model = Model()

    def _load_train_data(self, dataset_path):
        train_dataset = pandas.read_csv(dataset_path)
        train_dataset = train_dataset.drop(columns=['Unnamed: 0'])
        train_dataset = train_dataset[train_dataset['score'] <= 5]
        return train_dataset

    def _preprocess_train_data(self, train_data):
        reviews = train_data['review_content'].values
        scores = train_data['score'].values
        reviews_train, reviews_test, scores_train, scores_test = train_test_split(
            reviews, scores, test_size=0.1, random_state=1000)

        tokenizer = Tokenizer(num_words=4096)
        tokenizer.fit_on_texts(reviews_train)
        X_train = tokenizer.texts_to_sequences(reviews_train)
        X_test = tokenizer.texts_to_sequences(reviews_test)

        scores_train = self._vectorize(scores_train)
        scores_test = self._vectorize(scores_test)

        vocab_size = len(tokenizer.word_index) + 1

        maxlen = 256
        X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)
        X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)

        self.model.new(vocab_size, maxlen)
        self.model.tokenizer = tokenizer

        self.test_data = X_test, scores_test
        return X_train, scores_train

    def _vectorize(self, ys):
        result = []
        for y in ys:
            a = np.zeros((10))
            a[int((y - 0.5) * 2)] = 1
            result.append(a)
        return np.asarray(result)


    def train(self, data_path, save_path):
        data = self._load_train_data(data_path)
        x, y = self._preprocess_train_data(data)
        history = self.model.fit(x, y, epochs=32, verbose=True, validation_data=self.test_data, batch_size=1024)
        self.model.save_model(save_path)
        train_loss, train_accuracy = self.model.evaluate(x, y, verbose=True)
        test_loss, test_accuracy = self.model.evaluate(self.test_data[0], self.test_data[1], verbose=True)
        return {'train_loss': train_loss, 'train_accuracy': train_accuracy,
                'test_loss': test_loss, 'test_accuracy': test_accuracy}
