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
import statsmodels.api as sm

from scipy.optimize import least_squares
from scipy.stats import norm, t

alpha = 0.05

dat = pd.read_csv('ChickWeight.csv')
dat = dat.drop(dat.columns[0], axis=1)
dat['Diet'] = dat['Diet'].astype('category')

## Let's select just the diet=3
dat_example = dat.loc[dat['Diet']==3, ['weight','Time', 'Chick']].reset_index(drop=True)

y = dat_example['weight']
X = dat_example['Time']
n = len(y)
p = 3

# Initialize
M0 = y.max()
r0 = 0.1
b0 = 15

## Using scipy least squares
def logistic_gowth(theta, t):
    return theta[0] / (1 + np.exp(- theta[1] * (t - theta[2])))

def fun(theta):
    return logistic_gowth(theta, X) - y

theta0 = [M0,r0,b0]
log_growth = least_squares(fun, theta0)
theta_star = log_growth.x
F_matrix = log_growth.jac
y_hat = logistic_gowth(theta=log_growth.x, t=X)

hat_sigma2 = sum((log_growth.fun)**2/(n-p))
var_params = np.diag(hat_sigma2 * np.linalg.inv(F_matrix.T @ F_matrix))
var_params

# Let's get the significance of the estimators
se_params = np.sqrt(var_params)
z_score = theta_star/se_params
p_value = 1-norm.cdf(np.abs(z_score))

z_score
p_value

plt.figure(figsize=(10,7.5))
sns.lineplot(x=dat_example['Time'], y=dat_example['weight'])
sns.scatterplot(x=dat_example['Time'], y=dat_example['weight'])
plt.plot(X[:12], y_hat[:12], 'o-', label='estimated')
plt.xlabel('time')
plt.ylabel('weight')
plt.title("Weight chickens with diet 3 over time")
plt.legend(loc='upper left')

low_pred = y_hat[:12] - np.sqrt(hat_sigma2) * t.ppf(1-alpha/2, n-p)
upp_pred = y_hat[:12] + np.sqrt(hat_sigma2) * t.ppf(1-alpha/2, n-p)

plt.figure(figsize=(10,7.5))
plt.fill_between(X[:12], low_pred, upp_pred, facecolor='green', alpha=0.5, label='Prediction interval')
sns.scatterplot(x=dat_example['Time'], y=dat_example['weight'])
plt.plot(X[:12], y_hat[:12], 'o-', label='estimated')
plt.xlabel('time')
plt.ylabel('weight')
plt.title("Weight chickens with diet 3 over time")
plt.legend(loc='upper left')

# Let's add weights to the points
dat_weights_regression = dat_example[['weight','Time']].groupby(['Time']).var().reset_index()
dat_weights_regression = dat_weights_regression.rename(columns={'weight':'var'})

# It looks like the logarithm of the variance is quadratic with the time
plt.plot(dat_weights_regression['Time'], np.log(dat_weights_regression['var']))

X_var = pd.concat([
    dat_weights_regression['Time'],
    dat_weights_regression['Time']**2
    ], axis=1)
y_var = np.log(dat_weights_regression['var'])
var_t = sm.OLS(y_var, X_var).fit()

plt.plot(dat_weights_regression['Time'], np.log(dat_weights_regression['var']))
plt.plot(dat_weights_regression['Time'], var_t.predict(X_var))

plt.plot(y_var, y_var)
plt.plot(var_t.predict(X_var), y_var)

betas = var_t.params

plt.plot(np.exp(betas[0]*X[:12]+betas[1]*X[:12]**2),dat_weights_regression['var'])

# We see that we have stabilized the variance
y_transform = y*np.exp(-0.5*(betas[0]*X+betas[1]*X**2))
plt.scatter(X, y_transform)

def logistic_gowth_transform(theta, t):
    aux = np.exp(-0.5*(betas[0]*t+betas[1]*t**2))
    return aux * theta[0] / (1 + np.exp(- theta[1] * (t - theta[2])))

def fun(theta):
    return logistic_gowth_transform(theta, X) - y_transform

theta0 = [M0,r0,b0]
log_growth_transform = least_squares(fun, theta0)
theta_star_transform = log_growth_transform.x
F_matrix = log_growth_transform.jac

theta_star_transform
hat_sigma2_transform = sum((log_growth_transform.fun)**2/(n-p))
hat_sigma2_transform

var_params = np.diag(hat_sigma2_transform * np.linalg.inv(F_matrix.T @ F_matrix))
var_params

# Let's get the significance of the estimators
se_params = np.sqrt(var_params)
z_score = theta_star_transform/se_params
p_value = 1-norm.cdf(np.abs(z_score))

z_score
p_value

# Let's plot the result
X0 = np.linspace(0, 50)
y_hat = logistic_gowth(theta=theta_star_transform, t=X0)

aux = np.sqrt(hat_sigma2_transform*np.exp(betas[0]*X0+betas[1]*X0**2))
low_pred = y_hat - aux * t.ppf(1-alpha/2, n-p)
upp_pred = y_hat + aux * t.ppf(1-alpha/2, n-p)

plt.figure(figsize=(10,7.5))
plt.fill_between(X0, low_pred, upp_pred, facecolor='green', alpha=0.5, label='Prediction interval')
sns.scatterplot(x=dat_example['Time'], y=dat_example['weight'])
plt.plot(X0, y_hat, 'r-', label='estimated')
plt.xlabel('time')
plt.ylabel('weight')
plt.title("Weight chickens with diet 3 over time")
plt.legend(loc='upper left')

###
