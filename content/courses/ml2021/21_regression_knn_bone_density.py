import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsRegressor

datos_originales = pd.read_csv('bones_mineral_density.csv')
datos = datos_originales[['age', 'gender', 'spnbmd']]

datos_male = datos[datos['gender']=='male']
datos_male = datos_male.sort_values('age')

n_male, p = datos_male.shape
x_male = datos_male['age']
y_male = datos_male['spnbmd']

datos_female = datos[datos['gender']=='female']
datos_female = datos_female.sort_values('age')

n_female, p = datos_female.shape
x_female = datos_female['age']
y_female = datos_female['spnbmd']

knn_1_male = KNeighborsRegressor(n_neighbors=1)
knn_1_male.fit(pd.DataFrame(x_male), y_male)

knn_1_female = KNeighborsRegressor(n_neighbors=1)
knn_1_female.fit(pd.DataFrame(x_female), y_female)

x_vect = pd.DataFrame(pd.Series(np.linspace(9, 26, 100), name='age'))
male_predict = knn_1_male.predict(x_vect)
female_predict = knn_1_female.predict(x_vect)

plt.figure(figsize=(10,7.5))
sns.scatterplot(data=datos, x='age', y='spnbmd', hue='gender')
plt.plot(x_vect, male_predict,  color = 'DodgerBlue', linewidth = 2)
plt.plot(x_vect, female_predict, color = 'DeepPink', linewidth = 2)
plt.legend()

# choose k between 1 to 31
k_range = range(1, 31)
k_scores = []# use iteration to caclulator different k in models, then return the average accuracy based on the cross validation
for k in k_range:
    knn = KNeighborsRegressor(n_neighbors=k)
    scores = cross_val_score(knn, pd.DataFrame(x_male), y_male, cv=5)
    k_scores.append(scores.mean())# plot to see clearly
plt.plot(k_range, k_scores)
plt.xlabel('Value of K for KNN')
plt.ylabel('Cross-Validated Accuracy')

k_male_star = np.where(k_scores == max(k_scores))[0][0]+1

# choose k between 1 to 31
k_range = range(1, 31)
k_scores = []# use iteration to caclulator different k in models, then return the average accuracy based on the cross validation
for k in k_range:
    knn = KNeighborsRegressor(n_neighbors=k)
    scores = cross_val_score(knn, pd.DataFrame(x_female), y_female, cv=5)
    k_scores.append(scores.mean())# plot to see clearly
plt.plot(k_range, k_scores)
plt.xlabel('Value of K for KNN')
plt.ylabel('Cross-Validated Accuracy')

k_female_star = np.where(k_scores == max(k_scores))[0][0]+1

k_male_star
k_female_star

knn_2_male = KNeighborsRegressor(n_neighbors=k_male_star)
knn_2_male.fit(pd.DataFrame(x_male), y_male)

knn_2_female = KNeighborsRegressor(n_neighbors=k_female_star)
knn_2_female.fit(pd.DataFrame(x_female), y_female)

male_predict_2 = knn_2_male.predict(x_vect)
female_predict_2 = knn_2_female.predict(x_vect)

plt.figure(figsize=(10,7.5))
sns.scatterplot(data=datos, x='age', y='spnbmd', hue='gender')
plt.plot(x_vect, male_predict_2,  color = 'DodgerBlue', linewidth = 2)
plt.plot(x_vect, female_predict_2, color = 'DeepPink', linewidth = 2)
plt.legend()

## Suavizando con kernel
def gaussian_kernel(distances):
    h = 10
    weights = np.exp(-(distances**2)/h)
    return(weights)

knn_kernel_male = KNeighborsRegressor(n_neighbors=k_male_star, weights=gaussian_kernel)
knn_kernel_male.fit(pd.DataFrame(x_male), y_male)

knn_kernel_female = KNeighborsRegressor(n_neighbors=k_female_star, weights=gaussian_kernel)
knn_kernel_female.fit(pd.DataFrame(x_female), y_female)

male_predict_kernel = knn_kernel_male.predict(x_vect)
female_predict_kernel = knn_kernel_female.predict(x_vect)

plt.figure(figsize=(10,7.5))
sns.scatterplot(data=datos, x='age', y='spnbmd', hue='gender')
plt.plot(x_vect, male_predict_kernel,  color = 'DodgerBlue', linewidth = 2)
plt.plot(x_vect, female_predict_kernel, color = 'DeepPink', linewidth = 2)
plt.legend()


###
