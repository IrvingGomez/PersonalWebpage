#########################
##                     ##
## Irving Gomez Mendez ##
##     May 09, 2021    ##
##                     ##
#########################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import sympy as sym
from sympy.functions import exp
from scipy.optimize import least_squares
from scipy.stats import norm, t

alpha = 0.05

dat = pd.read_csv('ChickWeight.csv')
dat = dat.drop(dat.columns[0], axis=1)
dat['Diet'] = dat['Diet'].astype('category')

plt.figure(figsize=(10,7.5))
sns.scatterplot(x=dat['Time'], y=dat['weight'], hue=dat['Diet'], s=50)

plt.figure(figsize=(10,7.5))
sns.lineplot(
    x=dat['Time'], y=dat['weight'],
    hue=dat['Diet'], style=dat['Diet']
)
## Let's select just the diet=3
dat_example = dat.loc[dat['Chick']==3, ['weight','Time']].reset_index(drop=True)

plt.figure(figsize=(10,7.5))
sns.lineplot(x=dat_example['Time'], y=dat_example['weight'])
sns.scatterplot(x=dat_example['Time'], y=dat_example['weight'])
# We are going to model using a logistic growth
M, r, b, t = sym.symbols('M r b t')
f = M/(1+exp(-r*(t-b)))

sym.diff(f, M)
sym.diff(f, r)
sym.diff(f, b)

def f(t, M, r, b):
    return(M/(1+np.exp(-r*(t-b))))

def F_1(t,M,r,b):
    return(1/(1+np.exp(-r*(t-b))))

def F_2(t,M,r,b):
    return((M*(t-b)*np.exp(-r*(t-b)))/(1+np.exp(-r*(t-b)))**2)

def F_3(t,M,r,b):
    return((-M*r*np.exp(-r*(t-b)))/(1+np.exp(-r*(t-b)))**2)

y = dat_example['weight']
X = dat_example['Time']
n = len(y)
p = 3

# Initialize
M0 = y.max()
r0 = 0.1
b0 = 15

tt = [M0,r0,b0]

tolm   = 1e-6       # tolerance (minimum norm of the difference of the betas)
iterm  = 100        # maximum number of iterations
tolera = 1          # initialize tolera
itera  = 0          # initialize ittera
histo  = tt          # initialize beta upgrade

while((tolera > tolm) and (itera < iterm)):
    F_matrix = np.vstack([
        F_1(dat_example['Time'], tt[0], tt[1], tt[2]),
        F_2(dat_example['Time'], tt[0], tt[1], tt[2]),
        F_3(dat_example['Time'], tt[0], tt[1], tt[2])
    ])
    F_matrix = F_matrix.T
    y_hat = f(dat_example['Time'], tt[0], tt[1], tt[2])
    delta = np.linalg.solve(F_matrix.T @ F_matrix, F_matrix.T @ (y-y_hat))
    tt = tt + delta
    tolera = np.sqrt(sum(delta**2))
    histo  = np.vstack([histo, tt])
    itera  = itera+1

histo

## Using scipy least squares
def logistic_gowth(theta, t):
    return theta[0] / (1 + np.exp(- theta[1] * (t - theta[2])))

def fun(theta):
    return logistic_gowth(theta, X) - y

theta0 = [M0,r0,b0]
log_growth = least_squares(fun, theta0)
log_growth.x

F_matrix

log_growth.jac

# Getting confidence intervals
hat_sigma2 = sum((y-y_hat)**2/(n-p))
var_params = np.diag(hat_sigma2 * np.linalg.inv(F_matrix.T @ F_matrix))
var_params

# Let's get the significance of the estimators
se_params = np.sqrt(var_params)
z_score = tt/se_params
p_value = 1-norm.cdf(np.abs(z_score))

z_score
p_value

# predictions
y_hat = logistic_gowth(theta=log_growth.x, t=X)

plt.figure(figsize=(10,7.5))
plt.plot(X, y, 'o-', label='data')
plt.plot(X, y_hat, 'o-', label='estimated')
plt.xlabel('time')
plt.ylabel('weight')
plt.title("Weight of a chicken over time")
plt.legend(loc='upper left')

low_pred = y_hat - np.sqrt(hat_sigma2) * t.ppf(1-alpha/2, n-p)
upp_pred = y_hat + np.sqrt(hat_sigma2) * t.ppf(1-alpha/2, n-p)

plt.figure(figsize=(10,7.5))
plt.fill_between(X, low_pred, upp_pred, facecolor='green', alpha=0.5, label='Prediction interval')
plt.plot(X, y, 'o-', label='data')
plt.plot(X, y_hat, 'o-', label='estimated')
plt.xlabel('time')
plt.ylabel('weight')
plt.title("Weight of a chicken over time")
plt.legend(loc='upper left')



###
