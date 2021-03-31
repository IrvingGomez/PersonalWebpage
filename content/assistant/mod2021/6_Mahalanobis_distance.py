#########################
##                     ##
## Irving Gomez Mendez ##
##  February 27, 2021  ##
##                     ##
#########################

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t, multivariate_normal
import random

random.seed(111)
mu = [0,0]
Sigma = [[2,0.7],[0.7,2]]
points = multivariate_normal.rvs(mu,Sigma,200)

# Mahalanobis distance
D_M = np.sqrt(np.diag((points-mu) @ np.linalg.inv(Sigma) @ (points-mu).T))

plt.figure(figsize=(7.5,7.5))
plt.scatter(points[:,0], points[:,1], label='Original data', c=D_M)
plt.colorbar()
