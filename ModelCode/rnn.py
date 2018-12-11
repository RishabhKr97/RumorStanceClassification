# CODE FOR RNN

import os.path
import pandas as pd
import pickle
import time
from keras import backend
from keras.callbacks import ModelCheckpoint
from keras.callbacks import TensorBoard
from keras.layers import Dense, Dropout, CuDNNLSTM
from keras.models import load_model
from keras.models import Sequential
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical

LOAD_PREV = False
IS_PCA = False
NAME = ''
VALIDATION_SPLIT = 0.2
EPOCHS = 300

if IS_PCA:
    FEATURE_VECTORS_TRAINING_PATH = '../Data/feature_vectors_PCA_0.99_2601d_training.csv'
    FEATURE_VECTORS_TEST_PATH = '../Data/feature_vectors_PCA_0.99_2601d_test.csv'
else:
    FEATURE_VECTORS_TRAINING_PATH = '../Data/feature_vectors_training.csv'
    FEATURE_VECTORS_TEST_PATH = '../Data/feature_vectors_test.csv'
MODEL_PATH = '../Model/'+NAME+'.h5'
LOG_PATH = '../Logs/'+NAME
FEATURE_VECTORS_TRAINING = pd.read_csv(FEATURE_VECTORS_TRAINING_PATH, index_col=0)
FEATURE_VECTORS_TEST = pd.read_csv(FEATURE_VECTORS_TEST_PATH, index_col=0)
INPUT_DIM = FEATURE_VECTORS_TRAINING.shape[1]-1

def create_model():
    # CREATE A MODEL
    global NAME, MODEL_PATH, LOG_PATH
    if IS_PCA:
        NAME = 'RNN_PCA_{}'.format(int(time.time()))
    else:
        NAME = 'RNN_ALL_DIM_{}'.format(int(time.time()))
    NAME += '_D1-100_D2-100_relu'
    MODEL_PATH = '../Model/'+NAME+'.h5'
    LOG_PATH = '../Logs/'+NAME

    model = Sequential()
    model.add(CuDNNLSTM(128, input_shape=(INPUT_DIM,1), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(CuDNNLSTM(128))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(4, activation='softmax'))
    adam = Adam()
    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    return model

def get_model():
    # LOAD A SAVED MODEL OR GET A NEW ONE IF DOES NOT EXIST

    if LOAD_PREV and os.path.isfile(MODEL_PATH):
        model = load_model(MODEL_PATH)
    else:
        model = create_model()

    return model

def fit_model():
    model = get_model()
    checkpoint = ModelCheckpoint(MODEL_PATH, monitor='val_acc', verbose=1, save_best_only=True)
    tensorboard = TensorBoard(log_dir=LOG_PATH)
    callbacks_list = [checkpoint, tensorboard]
    X = FEATURE_VECTORS_TRAINING.iloc[:,:INPUT_DIM].values
    Y = FEATURE_VECTORS_TRAINING.iloc[:,INPUT_DIM].values
    cat_Y = to_categorical(Y-1)
    X = X.reshape(X.shape[0], INPUT_DIM, 1)
    print("FEATURE VECTORS TRAINING. SHAPE = {}".format(X.shape))
    print(X)
    print("CLASSIFICATIONS. SHAPE = {}".format(Y.shape))
    print(Y)
    print("CATEGORICAL CLASSIFICATION. SHAPE = {}".format(cat_Y.shape))
    print(cat_Y)

    print("MODEL CREATED. STARTING TRAINING.")
    history = model.fit(X, cat_Y, validation_split=VALIDATION_SPLIT, epochs=EPOCHS, callbacks=callbacks_list, verbose=1)
    print("MODEL FITTED. TRAINING COMPLETE")
    model.save(MODEL_PATH[:-3]+'_FULL.h5')
    print("MODEL SAVED")
    with open(MODEL_PATH[:-3]+'_FULL_HISTORY', 'wb') as handle:
        pickle.dump(history, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("HISTORY OBJECT SAVED")

def main():
    fit_model()

main()
