# GATHER DETAILS OF WORD EMBEDDINGS TO DETERMINE WHICH ONE IS MOST SUITABLE

import gc
import numpy as np
import pandas as pd
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from keras.preprocessing.text import Tokenizer

EMBEDDING_NAME = 'GoogleNews-vectors-negative300.bin'
EMBEDDING_PATH = '../WordEmbedding/' + EMBEDDING_NAME
EMBEDDING_OUTPUT_DIMENSIONS = 300
IS_BINARY_FILE = True
IS_WORD2VEC_FORMAT = True

# PARAMETERS FOR VOCABULARY AND FEATURE VECTOR CREATION
CONVERT_TO_LOWER_CASE = True
MAX_VOCAB_SIZE = None
CHARACTER_FILTERS = '"#$%&()*+,-./:;<=>@[\\]^_`{|}~'

if not IS_WORD2VEC_FORMAT:
    glove2word2vec(EMBEDDING_PATH, EMBEDDING_PATH+".word2vec")
    EMBEDDING_NAME += ".word2vec"
    EMBEDDING_PATH += ".word2vec"

FILE_PATH = '../Data/consolidated_data.csv'
TARGET_PATH = '../Data/word_embedding_stats.'+EMBEDDING_NAME+'.txt'

def main():
    fitted_tokenizer = get_fitted_tokenizer()
    gc.collect() # FREE UNREFRENCED MEMORY EXPLICITLY
    found, not_found, vocab_length, unusual_size_vectors = get_embedding_details(fitted_tokenizer)
    gc.collect() # FREE UNREFRENCED MEMORY EXPLICITLY

    output_file = open(TARGET_PATH, 'wt')
    output_file.write("WORD EMBEDDING STATS FOR {}\n***************\n".format(EMBEDDING_NAME))
    output_file.write("LENGTH OF EMBEDDING VOCABULARY = {}\n".format(vocab_length))
    output_file.write("OUTPUT VECTOR DIMENSION = {}\n".format(EMBEDDING_OUTPUT_DIMENSIONS))
    output_file.write("UNUSUAL SIZED VECTORS = {}\n".format(unusual_size_vectors))
    output_file.write("LENGTH OF TWEETS VOCABULARY = {}\n".format(len(fitted_tokenizer.word_index) + 1))
    output_file.write("TWEETS CONVERTED TO LOWER CASE = {}\n".format(CONVERT_TO_LOWER_CASE))
    output_file.write("CHARACTER FILTERS USED = {}\n".format(CHARACTER_FILTERS))
    output_file.write("FOUND WORDS = {}. PERCENTAGE = {}%\n".format(len(found), round((len(found)/(len(fitted_tokenizer.word_index) + 1))*100,2)))
    output_file.write("NOT FOUND WORDS = {}. PERCENTAGE = {}%\n***************\n".format(len(not_found), round((len(not_found)/(len(fitted_tokenizer.word_index) + 1))*100,2)))
    output_file.write("NOT FOUND WORDS ARE\n***************\n")
    for word in not_found:
        output_file.write("{} : {}\n".format(word[0], word[1]))
    output_file.write("FOUND WORDS ARE\n***************\n")
    for word in found:
        output_file.write("{} : {}\n".format(word[0], word[1]))
    output_file.close()

    print("Stats saved to {}".format(TARGET_PATH))

def get_fitted_tokenizer():
    # READS CONSOLIDATED CSV
    # FITS TOKENIZER ON TWEETS
    # RETURNS TOKENIZER

    source_file = pd.read_csv(FILE_PATH, skipinitialspace=True)
    source_file['tweet'] = source_file['tweet'].astype(str)
    print("Source file loaded. Total rows = {}".format(len(source_file)))
    # PREPARE TOKENIZER
    t = Tokenizer(num_words=MAX_VOCAB_SIZE, filters=CHARACTER_FILTERS, lower=CONVERT_TO_LOWER_CASE, split=' ')
    t.fit_on_texts(source_file['tweet'].tolist())
    vocab_size = len(t.word_index) + 1
    print("Tokenizer fitted on vocabulary. Vocabulary size = {}".format(vocab_size))

    return t

def get_embedding_details(fitted_tokenizer):
    # RETURNS FILTERD WORD EMBEDDING MATRIX ACCORDING TO FITTED VOCABULARY

    model = KeyedVectors.load_word2vec_format(EMBEDDING_PATH, binary=IS_BINARY_FILE, unicode_errors='ignore')
    print(EMBEDDING_NAME + " successfully loaded with vocabulary size = {}".format(len(model.wv.vocab)))

    found = []
    not_found = []
    unusual_size_vectors = 0
    for word, i in fitted_tokenizer.word_index.items():
        if word in model.wv.vocab:
            found.append((word,i))
            if(len(model.wv.get_vector(word)) != EMBEDDING_OUTPUT_DIMENSIONS):
                unusual_size_vectors += 1
        else:
            not_found.append((word,i))
    found = sorted(found, key=lambda x: x[1])
    not_found = sorted(not_found, key=lambda x: x[1])
    return found, not_found, len(model.wv.vocab), unusual_size_vectors


main()
