#########################
##                     ##
## Irving Gomez Mendez ##
##    March 03, 2021   ##
##                     ##
#########################

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

# Data
P = np.array([21, 19, 20, 15, 18, 18, 7, 16, 14, 9, 11, 13 ,10 ,10 ,10])
Q = np.array([3, 3, 7, 6, 10, 15, 16, 13, 9, 15, 9, 15, 12, 18, 21])
C = 6
U = Q*(P-C)
n = len(Q)
p = 3

# confidence level
alpha = 0.05

# We see graphically our assumptions
plt.figure(figsize=(7.5,7.5))
plt.scatter(P, Q, label='Original data')

plt.figure(figsize=(7.5,7.5))
plt.scatter(P, U, label='Original data')

# Construct the design matrix
XX = np.vstack([np.ones(n), P, P**2]).T

# This would be the design matrix for Q
XX_for_Q = np.vstack([np.ones(n), P]).T

V  = np.diag((P-C)**2)
V_inv = np.linalg.inv(V)

W = XX.T @ V_inv @ XX
W_inv = np.linalg.inv(W)
W_inv_for_Q = np.linalg.inv(XX_for_Q.T @ XX_for_Q)

# Get the beta estimators
hat_beta = W_inv @ XX.T @ V_inv @ U
hat_beta_0, hat_beta_1, hat_beta_2 = hat_beta

# Get the alpha estimators
hat_alpha_0 = -hat_beta_0/C
hat_alpha_1 = hat_beta_2
hat_alpha   = np.array([hat_alpha_0,hat_alpha_1])

# See graphically the estimation
x0 = np.linspace(6, 27, 50)
plt.figure(figsize=(10,5))
plt.scatter(P, U, label='Original data')
plt.plot(x0, hat_beta_0+hat_beta_1*x0+hat_beta_2*x0**2, 'r', label='Expected Gain')
plt.legend(loc='upper left')

plt.figure(figsize=(10,5))
plt.scatter(P, Q,label='Original data')
plt.plot(x0, hat_alpha_0+hat_alpha_1*x0, 'r', label='Expected Sale')
plt.legend(loc='upper right')

# Get sigma^2 estimator
SSE = (U-XX @ hat_beta).T @ V_inv @ (U-XX @ hat_beta)
hat_sigma_2 = 1/(n-p)*SSE

# get P_star, U_star and Q_star estimators
hat_P_star = -hat_beta_1/(2*hat_beta_2)
hat_X_star = np.array([1,hat_P_star,hat_P_star**2]).reshape(3,1)
hat_H_star = np.array([1,hat_P_star]).reshape(2,1)
hat_U_star = hat_X_star.T @ hat_beta
hat_Q_star = hat_H_star.T @ hat_alpha

# get confidence interval for P_star
delta_hat_P_star  = np.array([0, -1/(2*hat_beta_2), hat_beta_1/(2*hat_beta_2**2)]).reshape(3,1)
aux_t_conf_P_star = np.sqrt(hat_sigma_2 * delta_hat_P_star.T @ W_inv @ delta_hat_P_star)
aux_t_conf_P_star = aux_t_conf_P_star[0][0]
hat_P_star_low    = hat_P_star - t.ppf(1-alpha/2,n-p)*aux_t_conf_P_star
hat_P_star_upp    = hat_P_star + t.ppf(1-alpha/2,n-p)*aux_t_conf_P_star

# Create a vector for P_star
P0 = np.linspace(hat_P_star_low, hat_P_star_upp, 20)
X0 = np.vstack([np.ones(len(P0)),P0,P0**2]).T
H0 = np.vstack([np.ones(len(P0)),P0]).T
U0 = X0 @ hat_beta
Q0 = H0 @ hat_alpha

# get confidence interval for U_star
aux_t_conf_U_star   = np.sqrt(hat_sigma_2 * hat_X_star.T @ W_inv @ hat_X_star)
aux_t_conf_U_star   = aux_t_conf_U_star[0][0]
hat_U_star_low_conf = hat_U_star - t.ppf(1-alpha/2,n-p)*aux_t_conf_U_star
hat_U_star_upp_conf = hat_U_star + t.ppf(1-alpha/2,n-p)*aux_t_conf_U_star

aux_t_conf_U_star_0   = np.sqrt(hat_sigma_2 * np.diag(X0 @ W_inv @ X0.T))
hat_U_star_0_low_conf = U0 - t.ppf(1-alpha/2,n-p)*aux_t_conf_U_star_0
hat_U_star_0_upp_conf = U0 + t.ppf(1-alpha/2,n-p)*aux_t_conf_U_star_0

# get prediction interval for U_star
aux_t_pred_U_star   = np.sqrt(hat_sigma_2 * ((hat_P_star-C)**2+hat_X_star.T @ W_inv @ hat_X_star))
aux_t_pred_U_star   = aux_t_pred_U_star[0][0]
hat_U_star_low_pred = hat_U_star - t.ppf(1-alpha/2,n-p)*aux_t_pred_U_star
hat_U_star_upp_pred = hat_U_star + t.ppf(1-alpha/2,n-p)*aux_t_pred_U_star

aux_t_pred_U_star_0   = np.sqrt(hat_sigma_2 * ((P0-C)**2+np.diag(X0 @ W_inv @ X0.T)))
hat_U_star_0_low_pred = U0 - t.ppf(1-alpha/2,n-p)*aux_t_pred_U_star_0
hat_U_star_0_upp_pred = U0 + t.ppf(1-alpha/2,n-p)*aux_t_pred_U_star_0

# get confidence interval for Q_star
aux_t_conf_Q_star   = np.sqrt(hat_sigma_2 * hat_H_star.T @ W_inv_for_Q @ hat_H_star)
aux_t_conf_Q_star   = aux_t_conf_Q_star[0][0]
hat_Q_star_low_conf = hat_Q_star - t.ppf(1-alpha/2,n-p)*aux_t_conf_Q_star
hat_Q_star_upp_conf = hat_Q_star + t.ppf(1-alpha/2,n-p)*aux_t_conf_Q_star

aux_t_conf_Q_star_0   = np.sqrt(hat_sigma_2 * np.diag(H0 @ W_inv_for_Q @ H0.T))
hat_Q_star_0_low_conf = Q0 - t.ppf(1-alpha/2,n-p)*aux_t_conf_Q_star_0
hat_Q_star_0_upp_conf = Q0 + t.ppf(1-alpha/2,n-p)*aux_t_conf_Q_star_0

# get prediction interval for Q_star
aux_t_pred_Q_star   = np.sqrt(hat_sigma_2 * (1+hat_H_star.T @ W_inv_for_Q @ hat_H_star))
aux_t_pred_Q_star   = aux_t_pred_Q_star[0][0]
hat_Q_star_low_pred = hat_Q_star - t.ppf(1-alpha/2,n-p)*aux_t_pred_Q_star
hat_Q_star_upp_pred = hat_Q_star + t.ppf(1-alpha/2,n-p)*aux_t_pred_Q_star

aux_t_pred_Q_star_0   = np.sqrt(hat_sigma_2 * (1+np.diag(H0 @ W_inv_for_Q @ H0.T)))
hat_Q_star_0_low_pred = Q0 - t.ppf(1-alpha/2,n-p)*aux_t_pred_Q_star_0
hat_Q_star_0_upp_pred = Q0 + t.ppf(1-alpha/2,n-p)*aux_t_pred_Q_star_0

# See graphically the estimation
plt.figure(figsize=(15,7.5))
plt.plot(x0, hat_beta_0+hat_beta_1*x0+hat_beta_2*x0**2, 'r', label='Expected Gain')
plt.fill_between(P0, hat_U_star_0_low_pred, hat_U_star_0_upp_pred, facecolor='green', alpha=0.5, label='Prediction interval for U_star')
plt.fill_between(P0, hat_U_star_0_low_conf, hat_U_star_0_upp_conf, facecolor='yellow', alpha=0.5, label='Confidence interval for U_star')
plt.plot([hat_P_star,hat_P_star],[hat_U_star_low_pred,hat_U_star_upp_pred], 'brown', label='Prediction interval for the best guess')
plt.plot([hat_P_star,hat_P_star],[hat_U_star_low_conf,hat_U_star_upp_conf], 'black', label='Confidence interval for the best guess')
plt.scatter(P, U, label='Original data')
plt.legend(loc='upper left')

plt.figure(figsize=(15,7.5))
plt.plot(x0, hat_alpha_0+hat_alpha_1*x0, 'r', label='Expected Sale')
plt.fill_between(P0, hat_Q_star_0_low_pred, hat_Q_star_0_upp_pred, facecolor='green', alpha=0.5, label='Prediction interval for Q_star')
plt.fill_between(P0, hat_Q_star_0_low_conf, hat_Q_star_0_upp_conf, facecolor='yellow', alpha=0.5, label='Confidence interval for Q_star')
plt.plot([hat_P_star,hat_P_star],[hat_Q_star_low_pred,hat_Q_star_upp_pred], 'brown', label='Prediction interval for the best guess')
plt.plot([hat_P_star,hat_P_star],[hat_Q_star_low_conf,hat_Q_star_upp_conf], 'black', label='Confidence interval for the best guess')
plt.scatter(P, Q, label='Original data')
plt.legend(loc='upper left')
