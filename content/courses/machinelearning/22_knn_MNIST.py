import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.datasets import load_digits
from sklearn.neighbors import KNeighborsClassifier

import tensorflow as tf
mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0

train_images = train_images.reshape(train_images.shape[0],train_images.shape[1],train_images.shape[2],1)
test_images = test_images.reshape(test_images.shape[0],test_images.shape[1],test_images.shape[2],1)

train_images = train_images[:2000]
train_labels = train_labels[:2000]

test_images = train_images[:600]
test_labels = test_labels[:600]

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    # The CIFAR labels happen to be arrays,
    # which is why you need the extra index
    plt.xlabel(train_labels[i])

# flattening the images
flat_train = train_images.reshape((len(train_images), np.prod(train_images.shape[1:]))).astype('float32')
flat_test = test_images.reshape((len(test_images), np.prod(test_images.shape[1:]))).astype('float32')

knn = KNeighborsClassifier(n_neighbors=20)
knn.fit(flat_train, train_labels)
predictions_knn = knn.predict(flat_test)

knn_cm = confusion_matrix(y_true = test_labels,
                         y_pred = predictions_knn,
                         labels = [0,1,2,3,4,5,6,7,8,9])

plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(test_images[i], cmap=plt.cm.binary)
    # The CIFAR labels happen to be arrays,
    # which is why you need the extra index
    if test_labels[i] == predictions_knn[i]:
        plt.xlabel(str(test_labels[i]) +', '+ str(predictions_knn[i]), c='b')
    else:
        plt.xlabel(str(test_labels[i]) +', '+ str(predictions_knn[i]), c='r')

test_accuracy = np.diag(knn_cm).sum()/knn_cm.sum()

plt.figure(figsize=(10,10))
sns.heatmap(knn_cm, annot=True,
            linewidths=.5, square = True, cmap='BuPu', fmt='0.4g')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
plt.title('Accuracy Score: {}'.format(round(test_accuracy,4)))

k_range = range(1, 100)
k_scores = []# use iteration to caclulator different k in models, then return the average accuracy based on the cross validation
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(flat_train, train_labels)
    predictions_knn = knn.predict(flat_test)

    knn_cm = confusion_matrix(y_true = test_labels,
                             y_pred = predictions_knn,
                             labels = [0,1,2,3,4,5,6,7,8,9])

    test_accuracy = np.diag(knn_cm).sum()/knn_cm.sum()
    k_scores.append(test_accuracy)

plt.figure(figsize=(10,7.5))
plt.plot(k_range, k_scores)
plt.xlabel('Value of K for KNN')
plt.ylabel('Test Data Accuracy')

k_star = np.where(k_scores == max(k_scores))[0][0]+1

knn = KNeighborsClassifier(n_neighbors=k_star)
knn.fit(flat_train, train_labels)
predictions_knn = knn.predict(flat_test)

knn_cm = confusion_matrix(y_true = test_labels,
                         y_pred = predictions_knn,
                         labels = [0,1,2,3,4,5,6,7,8,9])

test_accuracy = np.diag(knn_cm).sum()/knn_cm.sum()

plt.figure(figsize=(10,10))
sns.heatmap(knn_cm, annot=True,
            linewidths=.5, square = True, cmap='BuPu', fmt='0.4g')
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
plt.title('Accuracy Score: {}'.format(round(test_accuracy,4)))
