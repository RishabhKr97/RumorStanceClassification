# PCA ON FEATURE VECTORS

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

DESIRED_VARIANCE = 0.99

FEATURE_VECTORS_PATH = '../Data/feature_vectors.csv'

feature_vectors = pd.read_csv(FEATURE_VECTORS_PATH, index_col=0)

# SEPARATING FEATURES AND CLASS
x = feature_vectors.iloc[:,:10807].values
print(x)
print(x.shape)
y = feature_vectors.iloc[:,10807]

# STANDARDIZE THE FEATURES
x = StandardScaler().fit_transform(x)
print(x)

# PCA
pca = PCA(n_components=DESIRED_VARIANCE)
principal_components = pca.fit_transform(x)
print("PCA complete. Dimensions for {}% variance = {}".format(pca.n_components*100, pca.n_components_))
principal_components = pd.DataFrame(principal_components)
principal_components = pd.concat([principal_components, y], axis=1)

PRINCIPAL_COMPONENTS_PATH = '../Data/feature_vectors_PCA_'+str(DESIRED_VARIANCE)+'_'+str(pca.n_components_)+'d.csv'
principal_components.to_csv(PRINCIPAL_COMPONENTS_PATH)
# PRINCIPAL COMPONENTS SAVED
