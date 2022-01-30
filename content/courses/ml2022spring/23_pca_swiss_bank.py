##########################
##                      ##
## Irving Gomez Mendez  ##
##   October 30, 2021   ##
##                      ##
##########################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

dat = pd.read_csv('banknotes.csv')

dat

sns.pairplot(data=dat, hue='conterfeit', corner=True)

class PCA_varios_metodos:
    def __init__(self, dat):
        X = dat.drop('conterfeit', axis=1)
        self.n, self.p = X.shape
        self.X = X

    def centrar_X(self):
        self.X_centered = pd.DataFrame(StandardScaler(with_std=False).fit_transform(self.X))

    def calcula_S(self):
        self.S = self.X.cov()

    def SVD(self):
        self.u, self.d, self.v_T  = np.linalg.svd(self.X_centered, full_matrices=False)

    def verifica_SVD(self):
        return(self.u @ np.diag(self.d) @ self.v_T)

    def PCA_con_SVD(self):
        self.SVD_loads       = self.v_T.T
        self.SVD_variance_CP = self.d**2/(self.n-1)
        self.SVD_CP_UD       = (self.u @ np.diag(self.d))
        self.SVD_CP_V        = self.X_centered @ self.v_T.T

    def PCA_con_matriz_cov(self):
        eigval, eigvect    = np.linalg.eig(self.S)
        self.S_loads       = eigvect
        self.S_variance_CP = eigval
        self.S_CP          = self.X_centered @ eigvect

    def PCA_con_sklearn(self):
        pca                      = PCA(n_components = self.p)
        pca_fit                  = pca.fit_transform(self.X)
        self.sklearn_loads       = pca.components_.T
        self.sklearn_variance_CP = pca.explained_variance_
        self.skelarn_CP          = pca_fit

pca_varios = PCA_varios_metodos(dat)
pca_varios.centrar_X()
pca_varios.calcula_S()
pca_varios.SVD()

pca_varios.X_centered

pd.DataFrame(pca_varios.verifica_SVD())

## PCA through SVD
pca_varios.PCA_con_SVD()
pd.DataFrame(pca_varios.SVD_loads)
pca_varios.SVD_variance_CP
pd.DataFrame(pca_varios.SVD_CP_UD)
pca_varios.SVD_CP_V

## PCA through covariance matrix
pca_varios.PCA_con_matriz_cov()
pd.DataFrame(pca_varios.S_loads)
pca_varios.S_variance_CP
pca_varios.S_CP

pca_varios.PCA_con_sklearn()
pd.DataFrame(pca_varios.sklearn_loads)
pca_varios.sklearn_variance_CP
pd.DataFrame(pca_varios.skelarn_CP)

plt.figure(figsize=(12,10))
plt.plot(pca_varios.sklearn_variance_CP.cumsum()/pca_varios.sklearn_variance_CP.sum())

loads = pd.DataFrame(pca_varios.sklearn_loads)
loads.index = dat.drop('conterfeit', axis=1).columns

loads

plt.figure(figsize=(12,10))
sns.scatterplot(x=loads[0], y=loads[1], hue=loads.index, palette='deep', s=300)
plt.axvline(0, color='red', linestyle='--')
plt.axhline(0, color='red', linestyle='--')
plt.legend(fontsize=15)

Components = pd.DataFrame(pca_varios.skelarn_CP)

plt.figure(figsize=(12,10))
sns.scatterplot(x=Components[0], y=Components[1], hue=dat['conterfeit'], palette='deep', s=300)
plt.legend(fontsize=15)


###
