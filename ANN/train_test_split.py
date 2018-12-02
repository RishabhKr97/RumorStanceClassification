# SPLIT DATA INTO TRAIN AND TEST AFTER SHUFFLING
# 90% TRAIN+VALIDATION, 10% TEST

import pandas as pd
import numpy as np

FEATURE_VECTORS_PATH = '../Data/feature_vectors.csv'

feature_vectors = pd.read_csv(FEATURE_VECTORS_PATH, index_col=0)

# SAVE SHUFFLED TRAINING, TEST AND VALIDATION DATA
# pylint: disable=unbalanced-tuple-unpacking
feature_vectors_training, feature_vectors_test = np.split(feature_vectors.sample(frac=1), [int(.9 * len(feature_vectors))])
feature_vectors_training = feature_vectors_training.reset_index(drop=True)
feature_vectors_test = feature_vectors_test.reset_index(drop=True)
print("TRAINING DATA : LENGTH = {}".format(len(feature_vectors_training)))
print(feature_vectors_training)
feature_vectors_training.to_csv(FEATURE_VECTORS_PATH[:-4]+"_training.csv")
print("TEST DATA : LENGTH = {}".format(len(feature_vectors_test)))
print(feature_vectors_test)
feature_vectors_test.to_csv(FEATURE_VECTORS_PATH[:-4]+"_test.csv")
