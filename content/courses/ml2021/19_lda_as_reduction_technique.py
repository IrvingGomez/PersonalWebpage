##########################
##                      ##
## Irving Gomez Mendez  ##
##   October 17, 2021   ##
##                      ##
##########################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

import warnings
warnings.filterwarnings("ignore")

dat_train = pd.read_csv('vowel_train.csv')
dat_train.drop('row.names', axis=1, inplace=True)
n_train = dat_train.shape[0]

dat_test = pd.read_csv('vowel_test.csv')
dat_test.drop('row.names', axis=1, inplace=True)
n_test = dat_test.shape[0]

lda = LinearDiscriminantAnalysis(store_covariance=True)
lda.fit(dat_train.drop('y', axis=1), dat_train['y'])

lda.means_.shape

B = np.cov(lda.means_.T)
W = lda.covariance_
A = np.linalg.solve(W, B)
eigenvectors = np.linalg.eig(A)[1]

direcciones_discriminantes = dat_train.drop('y', axis=1) @ eigenvectors
direcciones_discriminantes = pd.concat([dat_train['y'], direcciones_discriminantes], axis=1)

direcciones_discriminantes

proyected_means = lda.means_ @ eigenvectors
proyected_means = pd.concat([pd.Series(range(11), name='y'), pd.DataFrame(proyected_means)], axis=1)

proyected_means

#direcciones_discriminantes.groupby('y').mean().reset_index()

plt.figure(figsize=(12,12))
sns.scatterplot(data=direcciones_discriminantes, x=0, y=1, style='y', hue='y', palette='deep', s= 100)
sns.scatterplot(data=proyected_means, x=0, y=1, s=500, hue='y', palette='deep', legend=False)

plt.figure(figsize=(12,12))
sns.scatterplot(data=direcciones_discriminantes, x=0, y=2, style='y', hue='y', palette='deep', s= 100)
sns.scatterplot(data=proyected_means, x=0, y=2, s=500, hue='y', palette='deep', legend=False)

plt.figure(figsize=(12,12))
sns.scatterplot(data=direcciones_discriminantes, x=1, y=2, style='y', hue='y', palette='deep', s=100)
sns.scatterplot(data=proyected_means, x=1, y=2, s=500, hue='y', palette='deep', legend=False)

plt.figure(figsize=(12,12))
sns.scatterplot(data=direcciones_discriminantes, x=0, y=6, style='y', hue='y', palette='deep', s=100)
sns.scatterplot(data=proyected_means, x=0, y=6, s=500, hue='y', palette='deep', legend=False)

plt.figure(figsize=(12,12))
sns.scatterplot(data=direcciones_discriminantes, x=8, y=9, style='y', hue='y', palette='deep', s=100)
sns.scatterplot(data=proyected_means, x=8, y=9, s=500, hue='y', palette='deep', legend=False)
