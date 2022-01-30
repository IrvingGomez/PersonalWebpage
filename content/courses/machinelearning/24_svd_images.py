##########################
##                      ##
## Irving Gomez Mendez  ##
##   October 30, 2021   ##
##                      ##
##########################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

img = plt.imread("Taguchi.jpg")

n, p = img.shape
u, d, v_T  = np.linalg.svd(img, full_matrices=False)

img = img/255

img_svd = np.zeros(n*p).reshape(n,p)
plt.figure(figsize=(15,18))
plt.subplots_adjust(wspace=0, hspace=0)
for i in range(16):
    if i == 0:
        plt.subplot(4, 4, i+1)
        plt.imshow(img, cmap='gray')
        plt.xticks([])
        plt.yticks([])
    else:
        img_svd += d[i-1] * u[:,i-1].reshape(n, 1) @ v_T[i-1,:].reshape(1, p)
        plt.subplot(4, 4, i+1)
        plt.imshow(img_svd, cmap='gray')
        plt.xticks([])
        plt.yticks([])

img_block = img[:270,:230]
blocks = img_block.reshape(10,27,10,23).swapaxes(1, 2)

plt.figure(figsize=(7.5,9))
plt.subplots_adjust(wspace=0, hspace=0)
for i in range(10):
    for j in range(10):
        plt.subplot(10, 10, 10*i+(j+1))
        plt.imshow(blocks[i][j], cmap='gray', vmin=0, vmax=1)
        plt.xticks([])
        plt.yticks([])

#plt.figure(figsize=(7.5,9))
#plt.imshow(blocks.swapaxes(1,2).reshape(270,230), cmap='gray')

blocks_flat = blocks.reshape(100,27*23)
n, p = img_block.shape
n_block, p_block =  blocks_flat.shape
u, d, v_T  = np.linalg.svd(blocks_flat, full_matrices=False)

img_svd = np.zeros(n*p).reshape(n,p)
plt.figure(figsize=(15,18))
plt.subplots_adjust(wspace=0, hspace=0)
for i in range(16):
    if i == 0:
        plt.subplot(4, 4, i+1)
        plt.imshow(img, cmap='gray')
        plt.xticks([])
        plt.yticks([])
    else:
        blocks_flat_recons = d[i-1] * u[:,i-1].reshape(n_block, 1) @ v_T[i-1,:].reshape(1, p_block)
        img_svd += blocks_flat_recons.reshape(10,10,27,23).swapaxes(1,2).reshape(270,230)
        plt.subplot(4, 4, i+1)
        plt.imshow(img_svd, cmap='gray')
        plt.xticks([])
        plt.yticks([])



###
