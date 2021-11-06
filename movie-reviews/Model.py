import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
import numpy as np

class Model(Sequential):

    def new(self, vocab_size, maxlen):
        self.vocab_size = vocab_size
        self.maxlen = maxlen
        embedding_dim = 64
        dropout_rate = 0.3
        self.add(layers.Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=maxlen))
        self.add(layers.GlobalMaxPool1D())
        self.add(layers.Dense(512, activation='relu'))
        self.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
                                           beta_initializer="zeros", gamma_initializer="ones",
                                           moving_mean_initializer="zeros", moving_variance_initializer="ones"))
        self.add(layers.Dense(1024, activation='relu'))
        self.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
                                           beta_initializer="zeros", gamma_initializer="ones",
                                           moving_mean_initializer="zeros", moving_variance_initializer="ones"))
        self.add(layers.Dense(512, activation='relu'))
        self.add(layers.BatchNormalization(axis=-1, momentum=0.99, epsilon=0.001, center=True, scale=True,
                                           beta_initializer="zeros", gamma_initializer="ones",
                                           moving_mean_initializer="zeros", moving_variance_initializer="ones"))
        self.add(layers.Dense(10, activation='sigmoid'))
        opt = Adam(learning_rate=0.02)
        # loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True)
        self.compile(loss="absolute_square_error", optimizer=opt, metrics=['accuracy'])
        self.summary()

    def _postprocess_data(self, sample):
        scores = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        return [scores[np.argmax(x)] for x in sample]

    def forward(self, sample):
        sample = self._preprocess_data(sample)
        result = self.predict(sample)
        return self._postprocess_data(result)


    def _preprocess_data(self, data):
        data = self.tokenizer.texts_to_sequences(data)
        data = pad_sequences(data, padding='post', maxlen=self.maxlen)
        return data

    def save_model(self, save_path):
        with open(save_path + "/vocabsize", 'wb') as fp:
            pickle.dump(self.vocab_size, fp)
        with open(save_path + "/maxlen", 'wb') as fp:
            pickle.dump(self.maxlen, fp)
        with open(save_path + "/tokenizer", 'wb') as fp:
            pickle.dump(self.tokenizer.to_json(), fp)
        self.save_weights(save_path + "/weights.json")


    def load_model(self, model_path):
        with open(model_path + "/vocabsize", 'rb') as fp:
            vocab_size = pickle.load(fp)
        with open(model_path + "/maxlen", 'rb') as fp:
            maxlen = pickle.load(fp)
        with open(model_path + "/tokenizer", 'rb') as fp:
            ts = pickle.load(fp)
            self.tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(ts)
        self.new(vocab_size, maxlen)
        self.load_weights(model_path + "/weights.json")

