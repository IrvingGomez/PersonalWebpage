#########################
##                     ##
## Irving Gomez Mendez ##
##     May 10, 2021    ##
##                     ##
#########################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

from statsmodels.tools.tools import add_constant
from scipy.optimize import least_squares
from scipy.stats import norm, t

alpha = 0.05

dat = pd.read_csv('ChickWeight.csv')
dat = dat.drop(dat.columns[0], axis=1)
dat = dat.drop('Chick', axis=1)
dat['Diet'] = dat['Diet'].astype('category')

dat_dummies = pd.get_dummies(dat['Diet'])
dat_dummies = dat_dummies.rename(columns={1:'Diet1', 2:'Diet2', 3:'Diet3', 4:'Diet4'})

dat = pd.concat([dat, dat_dummies], axis=1)
dat

y = dat['weight']
X = dat[['Time', 'Diet1', 'Diet2', 'Diet3', 'Diet4']]
n = len(y)
p = 12

# Let's stabilize the variance
dat_var = dat[['weight','Diet','Time']].groupby(['Diet','Time']).var().reset_index()
dat_var = dat_var.rename(columns={'weight':'var'})
dat_var['log_var'] = np.log(dat_var['var'])

dat_var

dat_var = pd.merge(dat, dat_var, how='left', on=['Diet','Time'])
dat_var

X_aux = np.vstack(
    [dat_var['Diet1']*dat_var['Time'],
    dat_var['Diet2']*dat_var['Time'],
    dat_var['Diet3']*dat_var['Time'],
    dat_var['Diet4']*dat_var['Time'],
    dat_var['Diet1']*dat_var['Time']**2,
    dat_var['Diet2']*dat_var['Time']**2,
    dat_var['Diet3']*dat_var['Time']**2,
    dat_var['Diet4']*dat_var['Time']**2
    ]
)

X_aux = X_aux.T
y_aux = dat_var['log_var']

log_var_fit = sm.OLS(y_aux,X_aux).fit()
log_var_fit.summary2()

delta = np.array(log_var_fit.params)

plt.figure(figsize=(10,7.5))
sns.scatterplot(x=log_var_fit.predict(X_aux), y=y_aux, hue=dat_var['Diet'])
sns.lineplot(x=y_aux, y=y_aux)

plt.figure(figsize=(10,7.5))
sns.scatterplot(x=dat_var['Time'],
    y=dat_var['var'],
    hue=dat_var['Diet']
)
sns.lineplot(x=dat_var['Time'],
    y=np.exp(log_var_fit.predict(X_aux)),
    hue=dat_var['Diet']
)

def sigma_1(t,D):
    linear_part = (delta[0]*D[0]+delta[1]*D[1]+delta[2]*D[2]+delta[3]*D[3])*t
    quadratic_part = (delta[4]*D[0]+delta[5]*D[1]+delta[6]*D[2]+delta[7]*D[3])*t**2
    return np.exp(-0.5*(linear_part+quadratic_part))

def logistic_gowth(theta,t,D):
    first_part = theta[0]*D[0]+theta[1]*D[1]+theta[2]*D[2]+theta[3]*D[3]
    second_part = theta[4]*D[0]+theta[5]*D[1]+theta[6]*D[2]+theta[7]*D[3]
    third_part = theta[8]*D[0]+theta[9]*D[1]+theta[10]*D[2]+theta[11]*D[3]
    return first_part/(1+np.exp(-second_part*(t-third_part)))

dat_sigma_1 = dat.apply(lambda row: sigma_1(row['Time'], row[['Diet1','Diet2','Diet3','Diet4']]), axis=1)
dat['weight_transform'] = dat['weight']*dat_sigma_1

plt.figure(figsize=(10,7.5))
sns.scatterplot(x=dat['Time'],y=dat['weight_transform'],hue=dat['Diet'])

# The variance is approx. 1 for all diets and time
dat[['weight_transform','Diet','Time']].groupby(['Diet','Time']).var().reset_index()

def dat_logistic_growth(theta):
    return dat.apply(lambda row: logistic_gowth(theta, row['Time'], row[['Diet1','Diet2','Diet3','Diet4']]), axis=1)

def logistic_growth_transform(theta):
    return dat_sigma_1*dat_logistic_growth(theta)

def fun(theta):
    return logistic_growth_transform(theta) - dat['weight_transform']

theta0 = [dat['weight'].max()]*4 + [0.1]*4 + [15]*4
logistic_growth_transform = least_squares(fun, theta0)
theta_star = logistic_growth_transform.x
F_matrix = logistic_growth_transform.jac

hat_sigma2_transform = sum((logistic_growth_transform.fun)**2/(n-p))
hat_sigma2_transform

var_params = np.diag(hat_sigma2_transform * np.linalg.inv(F_matrix.T @ F_matrix))
var_params

# Let's get the significance of the estimators
se_params = np.sqrt(var_params)
z_score = theta_star/se_params
p_value = 1-norm.cdf(np.abs(z_score))

z_score
p_value

# Let's plot the result in the observed time
y_hat = dat_logistic_growth(theta=theta_star)

aux = np.sqrt(hat_sigma2_transform*dat_sigma_1**(-2))
low_pred = y_hat - aux * t.ppf(1-alpha/2, n-p)
upp_pred = y_hat + aux * t.ppf(1-alpha/2, n-p)

low_pred = low_pred.unique()
upp_pred = upp_pred.unique()

def plot_diet(Diet):
    plt.figure(figsize=(10,7.5))
    if Diet == 1:
        plt.fill_between(dat['Time'][:12], low_pred[:12], upp_pred[:12], facecolor='b', alpha=0.5, label='Prediction interval, Diet 1')
        sns.scatterplot(x=dat.loc[dat['Diet'] == 1, 'Time'], y=dat.loc[dat['Diet'] == 1, 'weight'], color='b', label='Diet 1')
    if Diet == 2:
        plt.fill_between(dat['Time'][:12], low_pred[12:24], upp_pred[12:24], facecolor='orange', alpha=0.5, label='Prediction interval, Diet 2')
        sns.scatterplot(x=dat.loc[dat['Diet'] == 2, 'Time'], y=dat.loc[dat['Diet'] == 2, 'weight'], color='orange', label='Diet 2')
    if Diet == 3:
        plt.fill_between(dat['Time'][:12], low_pred[24:36], upp_pred[24:36], facecolor='g', alpha=0.5, label='Prediction interval, Diet 3')
        sns.scatterplot(x=dat.loc[dat['Diet'] == 3, 'Time'], y=dat.loc[dat['Diet'] == 3, 'weight'], color='g', label='Diet 3')
    if Diet == 4:
        plt.fill_between(dat['Time'][:12], low_pred[36:48], upp_pred[36:48], facecolor='r', alpha=0.5, label='Prediction interval, Diet 4')
        sns.scatterplot(x=dat.loc[dat['Diet'] == 4, 'Time'], y=dat.loc[dat['Diet'] == 4, 'weight'], color='r', label='Diet 4')
    sns.lineplot(x=dat['Time'], y=y_hat, hue=dat['Diet'])
    plt.xlabel('time')
    plt.ylabel('weight')
    plt.title("Weight chickens over time")
    plt.legend(loc='upper left')

plot_diet(1)

plot_diet(2)

plot_diet(3)

plot_diet(4)

d = {'Time': list(range(51))*4,
    'Diet': [1]*51 + [2]*51 + [3]*51 + [4]*51,
    'Diet1': [1]*51 + [0]*153,
    'Diet2': [0]*51 + [1]*51 +[0]*102,
    'Diet3': [0]*102 + [1]*51 +[0]*51,
    'Diet4': [0]*153 + [1]*51
}
dat_predict = pd.DataFrame(d)
dat_predict['Diet'] = dat_predict['Diet'].astype('category')

dat_predict_sigma_1 = dat_predict.apply(lambda row: sigma_1(row['Time'], row[['Diet1','Diet2','Diet3','Diet4']]), axis=1)
dat_predict_y_hat   = dat_predict.apply(lambda row: logistic_gowth(theta_star, row['Time'], row[['Diet1','Diet2','Diet3','Diet4']]), axis=1)

aux = np.sqrt(hat_sigma2_transform*dat_predict_sigma_1**(-2))
low_pred = dat_predict_y_hat - aux * t.ppf(1-alpha/2, n-p)
upp_pred = dat_predict_y_hat + aux * t.ppf(1-alpha/2, n-p)

def plot_diet_predict(Diet):
    plt.figure(figsize=(10,7.5))
    if Diet == 1:
        plt.fill_between(dat_predict['Time'][:51], low_pred[:51], upp_pred[:51], facecolor='b', alpha=0.5, label='Prediction interval, Diet 1')
        sns.scatterplot(x=dat.loc[dat['Diet'] == 1, 'Time'], y=dat.loc[dat['Diet'] == 1, 'weight'], color='b', label='Diet 1')
    if Diet == 2:
        plt.fill_between(dat_predict['Time'][:51], low_pred[51:102], upp_pred[51:102], facecolor='orange', alpha=0.5, label='Prediction interval, Diet 2')
        sns.scatterplot(x=dat.loc[dat['Diet'] == 2, 'Time'], y=dat.loc[dat['Diet'] == 2, 'weight'], color='orange', label='Diet 2')
    if Diet == 3:
        plt.fill_between(dat_predict['Time'][:51], low_pred[102:153], upp_pred[102:153], facecolor='g', alpha=0.5, label='Prediction interval, Diet 3')
        sns.scatterplot(x=dat.loc[dat['Diet'] == 3, 'Time'], y=dat.loc[dat['Diet'] == 3, 'weight'], color='g', label='Diet 3')
    if Diet == 4:
        plt.fill_between(dat_predict['Time'][:51], low_pred[153:204], upp_pred[153:204], facecolor='r', alpha=0.5, label='Prediction interval, Diet 4')
        sns.scatterplot(x=dat.loc[dat['Diet'] == 4, 'Time'], y=dat.loc[dat['Diet'] == 4, 'weight'], color='r', label='Diet 4')
    sns.lineplot(x=dat_predict['Time'], y=dat_predict_y_hat, hue=dat_predict['Diet'])
    plt.xlabel('time')
    plt.ylabel('weight')
    plt.title("Weight chickens over time")
    plt.legend(loc='upper left')

plot_diet_predict(1)

plot_diet_predict(2)

plot_diet_predict(3)

plot_diet_predict(4)



###
