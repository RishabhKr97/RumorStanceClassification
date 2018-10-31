# CHANGE TWEET TEXT TO ENCODED FORMAT
# SAVE WORD EMBEDDING MATRIX

import gc
import numpy as np
import pandas as pd
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

EMBEDDING_NAME = 'GoogleNews-vectors-negative300.bin'
EMBEDDING_PATH = '../WordEmbedding/' + EMBEDDING_NAME
EMBEDDING_OUTPUT_DIMENSIONS = 300
IS_BINARY_FILE = True
IS_WORD2VEC_FORMAT = True

# PARAMETERS FOR VOCABULARY AND FEATURE VECTOR CREATION
CONVERT_TO_LOWER_CASE = True
MAX_INPUT_VECTOR_DIMENSIONS = None
MAX_VOCAB_SIZE = None
CHARACTER_FILTERS = '"#$%&()*+,-./:;<=>@[\]^_`{|}~'

if not IS_WORD2VEC_FORMAT:
    glove2word2vec(EMBEDDING_PATH, EMBEDDING_PATH+".word2vec")
    EMBEDDING_NAME += ".word2vec"
    EMBEDDING_PATH += ".word2vec"

FILE_PATH = '../Data/consolidated_data.csv'
FEATURE_VECTORS_TARGET_PATH = '../Data/feature_vectors.csv'
FILTERED_EMBEDDING_TARGET_PATH = '../Data/FILTERED_EMBEDDING_MATRIX_'+EMBEDDING_NAME+'.npy'

def main():
    fitted_tokenizer = get_fitted_tokenizer()
    gc.collect() # FREE UNREFRENCED MEMORY EXPLICITLY
    embedding_matrix = get_filtered_word_embeddings(fitted_tokenizer)
    gc.collect() # FREE UNREFRENCED MEMORY EXPLICITLY
    np.save(FILTERED_EMBEDDING_TARGET_PATH, embedding_matrix)
    print("Filtered embedding matrix saved successfully")

def get_fitted_tokenizer():
    # READS CONSOLIDATED CSV
    # FITS TOKENIZER ON TWEETS
    # ENCODE AND PAD THE TWEETS
    # SAVE PADDED, ENCODED TWEETS ALONG WITH OTHER FEATURES AND CLASSIFICATION TO FEATURE VECTOR FILE
    # RETURNS TOKENIZER

    source_file = pd.read_csv(FILE_PATH, skipinitialspace=True)
    source_file['tweet'] = source_file['tweet'].astype(str)
    print("Source file loaded. Total rows = {}".format(len(source_file)))
    # PREPARE TOKENIZER
    t = Tokenizer(num_words=MAX_VOCAB_SIZE, filters=CHARACTER_FILTERS, lower=CONVERT_TO_LOWER_CASE, split=' ')
    t.fit_on_texts(source_file['tweet'].tolist())
    vocab_size = len(t.word_index) + 1
    print("Tokenizer fitted on vocabulary. Vocabulary size = {}".format(vocab_size))
    # INTEGER ENCODE THE TWEETS
    encoded_tweets = t.texts_to_sequences(source_file['tweet'].tolist())
    print("Encoding of tweets successful.")
    print("Top 10 encodings...")
    for i in range(10):
        print(encoded_tweets[i])
    print("Last 10 encodings...")
    for i in range(10):
        print(encoded_tweets[-1*i])
    print("Padding tweets to length {}".format(MAX_INPUT_VECTOR_DIMENSIONS))
    # PAD THE ENCODINGS
    encoded_tweets = pad_sequences(encoded_tweets, maxlen=MAX_INPUT_VECTOR_DIMENSIONS, padding='post', truncating='post')
    print("Top 10 paded encodings...")
    for i in range(10):
        print(encoded_tweets[i])
    print("Last 10 paded encodings...")
    for i in range(10):
        print(encoded_tweets[-1*i])
    feature_vectors = pd.DataFrame(encoded_tweets)
    feature_vectors = pd.concat([feature_vectors, source_file.iloc[:,1:10]], axis=1)
    print("Feature vectors...")
    print(feature_vectors)
    feature_vectors.to_csv(FEATURE_VECTORS_TARGET_PATH)
    print("Feature vectors saved to file")

    return t

def get_filtered_word_embeddings(fitted_tokenizer):
    # RETURNS FILTERD WORD EMBEDDING MATRIX ACCORDING TO FITTED VOCABULARY

    model = KeyedVectors.load_word2vec_format(EMBEDDING_PATH, binary=IS_BINARY_FILE)
    print(EMBEDDING_NAME + " successfully loaded with vocabulary size = {}".format(len(model.wv.vocab)))

    embedding_matrix = np.zeros((len(fitted_tokenizer.word_index) + 1, EMBEDDING_OUTPUT_DIMENSIONS))
    for word, i in fitted_tokenizer.word_index.items():
        if word in model.wv.vocab:
            embedding_matrix[i] = model.wv.get_vector(word)

    print("Embedding matrix filtered. Shape of matrix {}".format(embedding_matrix.shape))
    return embedding_matrix

main()
