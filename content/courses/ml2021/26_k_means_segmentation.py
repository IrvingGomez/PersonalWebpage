##########################
##                      ##
## Irving Gomez Mendez  ##
##  November 15, 2021   ##
##                      ##
##########################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

from kneed import KneeLocator
from sklearn.cluster import KMeans

img = plt.imread("GIR.jpg")
img = img/255
n1, n2, p = img.shape
img_flat = img.reshape(n1*n2, p)

plt.imshow(img)
plt.xticks([])
plt.yticks([])

kmeans = KMeans(n_clusters=2, random_state=111, init='random')
kmeans = kmeans.fit(img_flat)
img_recons = np.array([kmeans.cluster_centers_[l].tolist() for l in kmeans.labels_]).reshape(n1, n2, p)

plt.imshow(img_recons)
plt.xticks([])
plt.yticks([])

kmeans = KMeans(n_clusters=2, random_state=489135, init='random')
kmeans = kmeans.fit(img_flat)
img_recons = np.array([kmeans.cluster_centers_[l].tolist() for l in kmeans.labels_]).reshape(n1, n2, p)

plt.imshow(img_recons)
plt.xticks([])
plt.yticks([])

n_cluster = [2,3,4,5,6,7,50]
plt.figure(figsize=(12,5))
plt.subplots_adjust(wspace=0, hspace=0)
for i in range(8):
    if i == 0:
        plt.subplot(2, 4, i+1)
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
    else:
        kmeans = KMeans(n_clusters=n_cluster[i-1], random_state=111)
        kmeans = kmeans.fit(img_flat)
        cluster = pd.Series(kmeans.labels_)
        cluster.name = 'cluster'
        cluster_center = pd.DataFrame(kmeans.cluster_centers_)
        img_recons = pd.merge(cluster, cluster_center, how='left', left_on='cluster', right_index=True).drop('cluster', axis=1)
        plt.subplot(2, 4, i+1)
        plt.imshow(img_recons.to_numpy().reshape(n1,n2,p))
        plt.xticks([])
        plt.yticks([])
