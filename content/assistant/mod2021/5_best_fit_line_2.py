#########################
##                     ##
## Irving Gomez Mendez ##
##  February 27, 2021  ##
##                     ##
#########################

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t, f
from matplotlib.lines import Line2D

dat = np.array([[100, 89, 89, 92, 78, 101, 90, 82, 95, 108, 111, 112,
    125, 123, 100, 102, 112, 112, 100, 107, 103, 129, 118, 149],
    [709, 740, 586, 806, 694, 760, 664, 509, 619, 652, 772, 896,
    742, 831, 667, 772, 838, 679, 889, 690, 698, 860, 799, 882]]).T
dat = dat/10

n = dat.shape[0]
yy = dat[:,1]
XX = np.vstack([np.ones(n),dat[:,0]]).T
p = XX.shape[1]

# We compute the coeff.
beta_0, beta_1 = np.linalg.lstsq(XX, yy, rcond=None)[0]
beta = [beta_0, beta_1]

# Calculate the SSE
SSE = np.linalg.lstsq(XX, yy, rcond=None)[1]

# We get confidence interval
alpha = 0.05
x0 = np.linspace(7, 15, 50)
X0 = np.array([np.ones(len(x0)),x0]).T

aux_t_conf = np.sqrt(SSE/(n-p)*(np.diag(X0 @ np.linalg.inv(XX.T @ XX) @ X0.T)))
yy0_hat = X0 @ np.array([beta_0, beta_1])
upp_conf = yy0_hat+t.ppf(1-alpha/2,n-p)*aux_t_conf
low_conf = yy0_hat-t.ppf(1-alpha/2,n-p)*aux_t_conf

# We get prediction interval
aux_t_pred = np.sqrt(SSE/(n-p)*(1+np.diag(X0 @ np.linalg.inv(XX.T @ XX) @ X0.T)))
yy0_hat = X0 @ np.array([beta_0, beta_1])
upp_pred = yy0_hat+t.ppf(1-alpha/2,n-p)*aux_t_pred
low_pred = yy0_hat-t.ppf(1-alpha/2,n-p)*aux_t_pred

plt.figure(figsize=(10,5))
plt.plot(dat[:,0], yy, 'o', label='Original data', markersize=5)
plt.plot(x0, beta_0+beta_1*x0, 'r', label='Fitted line')
plt.fill_between(x0, low_pred, upp_pred, facecolor='green', alpha=0.5, label='Prediction interval')
plt.fill_between(x0, low_conf, upp_conf, facecolor='yellow', alpha=0.5, label='Confidence interval')
plt.legend(loc='upper left')

# We get confidence intervals and region of cofidence for beta
aux_t_conf = np.sqrt(SSE/(n-p)*(np.diag(np.linalg.inv(XX.T @ XX))))

beta_0_upp = beta_0+t.ppf(1-alpha/2,n-p)*aux_t_conf[0]
beta_0_low = beta_0-t.ppf(1-alpha/2,n-p)*aux_t_conf[0]

beta_1_upp = beta_1+t.ppf(1-alpha/2,n-p)*aux_t_conf[1]
beta_1_low = beta_1-t.ppf(1-alpha/2,n-p)*aux_t_conf[1]

def conf_region(b0, b1):
    bb = np.array([b0, b1])
    return (n-p)/(p*SSE)*((bb-beta).T @ XX.T @ XX @ (bb-beta))

beta_0_vect = np.linspace(0, 70, 50)
beta_1_vect = np.linspace(1, 7, 50)
z = conf_region(beta_0_vect[:,None], beta_1_vect[None,:])

plt.figure(figsize=(10,5))
plt.plot(beta_0, beta_1, 'o', markersize=5)
plt.contour(beta_0_vect, beta_1_vect, z, levels=[f.ppf(1-alpha, p, n-p)])
plt.plot([beta_0_low,beta_0_upp,beta_0_upp,beta_0_low,beta_0_low],
    [beta_1_low,beta_1_low,beta_1_upp,beta_1_upp,beta_1_low])
