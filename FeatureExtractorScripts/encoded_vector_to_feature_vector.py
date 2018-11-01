# USE WORD EMBEDDING MATRIX TO COVERT ENCODED TWEET VECTOR TO FEATURE VECTOR
# SAVE FEATURE VECTORS

from keras.models import Sequential
from keras.layers import Flatten
from keras.layers import Embedding
import numpy as np
import pandas as pd
import pickle

ENCODED_VECTORS_PATH = '../Data/encoded_vectors.csv'
TOKENIZER_PATH = '../Data/tokenizer.pickle'
EMBEDDING_PATH = '../Data/FILTERED_EMBEDDING_MATRIX_glove.840B.300d.txt.word2vec.npy'
FEATURE_VECTOR_TARGET_PATH = '../Data/feature_vectors.csv'

def main():
    construct_feature_vectors()

def get_fitted_tokenizer():
    with open(TOKENIZER_PATH, 'rb') as handle:
        t = pickle.load(handle)
    return t

def construct_feature_vectors():
    tokenizer = get_fitted_tokenizer()
    print("Tokenizer loaded successfully. Vocabulary size = {}".format(len(tokenizer.word_index)+1))
    embedding_matrix = np.load(EMBEDDING_PATH)
    print("Embedding matrix loaded successfully. Shape = {}".format(embedding_matrix.shape))
    encoded_vectors = pd.read_csv(ENCODED_VECTORS_PATH, index_col=0)
    print("Encoded vectors loaded successfully")
    print(encoded_vectors)

    # MAKE A KERAS EMBEDDING LAYER MODEL FOR ENCODING TO FEATURE VECTOR CONVERSION
    model = Sequential()
    e = Embedding(len(tokenizer.word_index)+1, 300, weights=[embedding_matrix], input_length=34, trainable=False)
    model.add(e)
    model.add(Flatten())
    # COMPILE THE MODEL
    model.compile('adam', loss='binary_crossentropy')
    # SUMMARIZE THE MODEL
    model.summary()

    encoded_tweets = encoded_vectors.iloc[:,:34]
    embedded_tweets = model.predict(encoded_tweets)
    embedded_tweets = pd.DataFrame(embedded_tweets)
    feature_vectors = pd.concat([embedded_tweets, encoded_vectors.iloc[:,34:]], axis=1)
    print("Feature vectors constructed...")
    print(feature_vectors)
    feature_vectors.to_csv(FEATURE_VECTOR_TARGET_PATH)
    print("Feature vectors saved")

main()
