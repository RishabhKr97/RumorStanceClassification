# CODE TO TEST MODELS AND GENERATE PERFORMANCE METRICS

import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

IS_RNN = True

if IS_RNN:
    MODEL_PATH = '../Model/RNN_ALL_DIM_1544080373_D1-100_D2-100_relu.h5'
    CLASSIFICATION_PATH = 'classification_report_RNN.txt'
    MATRIX_PATH = 'confusion_matrix_RNN.txt'
else:
    MODEL_PATH = '../Model/ANN_ALL_DIM_1543857875_D1-100_D2-100_relu.h5'
    CLASSIFICATION_PATH = 'classification_report_ANN.txt'
    MATRIX_PATH = 'confusion_matrix_ANN.txt'

FEATURE_VECTORS_TEST_PATH = '../Data/feature_vectors_test.csv'
FEATURE_VECTORS_TEST = pd.read_csv(FEATURE_VECTORS_TEST_PATH, index_col=0)
INPUT_DIM = FEATURE_VECTORS_TEST.shape[1]-1
LABELS=[1, 2, 3, 4]
TARGETS=['Support', 'Deny', 'Query', 'Comment']
model = load_model(MODEL_PATH)

X = FEATURE_VECTORS_TEST.iloc[:,:INPUT_DIM].values
if not IS_RNN:
    X = X.reshape(X.shape[0], INPUT_DIM, 1)
Y = FEATURE_VECTORS_TEST.iloc[:,INPUT_DIM].values

pred_Y = model.predict(X)
pred_Y = pred_Y.argmax(axis=1)+1

report = classification_report(Y, pred_Y, labels=LABELS, target_names=TARGETS, digits=2)
matrix = confusion_matrix(Y, pred_Y, labels=LABELS)
accuracy = accuracy_score(Y, pred_Y)

print("\nCLASSIFICATION REPORT")
print(report)
print("ACCURACY SCORE")
print(accuracy)
print("\nCONFUSION MATRIX")
print(matrix)

with open(CLASSIFICATION_PATH, 'w') as text_file:
    text_file.write(report)
    text_file.write("\nACCURACY = {}%".format(accuracy*100))

np.savetxt(MATRIX_PATH, matrix, delimiter='\t', fmt='%d', header="Support Deny Query Comment")

print("\nSAVED REPORTS TO FILE")