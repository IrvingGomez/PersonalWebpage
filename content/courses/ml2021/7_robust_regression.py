#########################
##                     ##
## Irving Gomez Mendez ##
##    March 03, 2021   ##
##                     ##
#########################

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, uniform
import statsmodels.api as sm
from scipy.stats import t

data = sm.datasets.stackloss.load(as_pandas=False)

alpha=0.05

nsample = 50
x1 = np.linspace(0, 20, nsample)
X = np.column_stack((x1, (x1-5)**2))
X = sm.add_constant(X)
sig = 0.3   # smaller error variance makes OLS<->RLM contrast bigger
beta = [5, 0.5, -0.0]
y_true2 = np.dot(X, beta)
y2 = y_true2 + sig*1. * np.random.normal(size=nsample)
y2[[39,41,43,45,48]] -= 5   # add some outliers (10% of nsample)

res = sm.OLS(y2, X).fit()
res.params
res.scale

res_predict = res.get_prediction(X)
summary_res_predict = res_predict.summary_frame(alpha=0.05)

#aux_t_pred = np.sqrt(res.scale*(1+np.diag(X @ np.linalg.inv(X.T @ X) @ X.T)))
#upp_pred = res.fittedvalues+t.ppf(1-alpha/2,nsample-3)*aux_t_pred
#low_pred = res.fittedvalues-t.ppf(1-alpha/2,nsample-3)*aux_t_pred

resrlm = sm.RLM(y2, X).fit()
resrlm.params
resrlm.scale

aux_t_conf = np.sqrt(resrlm.scale*(np.diag(X @ np.linalg.inv(X.T @ X) @ X.T)))
rlm_upp_conf = resrlm.fittedvalues+t.ppf(1-alpha/2,nsample-3)*aux_t_conf
rlm_low_conf = resrlm.fittedvalues-t.ppf(1-alpha/2,nsample-3)*aux_t_conf

aux_t_pred = np.sqrt(resrlm.scale*(1+np.diag(X @ np.linalg.inv(X.T @ X) @ X.T)))
rlm_upp_pred = resrlm.fittedvalues+t.ppf(1-alpha/2,nsample-3)*aux_t_pred
rlm_low_pred = resrlm.fittedvalues-t.ppf(1-alpha/2,nsample-3)*aux_t_pred

fig = plt.figure(figsize=(12,8))
plt.plot(x1, y2, 'o',label="data")
plt.plot(x1, y_true2, 'b', label="True")
plt.plot(x1, res.fittedvalues, 'r', label="OLS")
plt.plot(x1, summary_res_predict['mean_ci_lower'], 'r--')
plt.plot(x1, summary_res_predict['mean_ci_upper'], 'r--')
plt.plot(x1, summary_res_predict['obs_ci_lower'], 'purple')
plt.plot(x1, summary_res_predict['obs_ci_upper'], 'purple')
plt.legend(loc="best")

fig = plt.figure(figsize=(12,8))
plt.plot(x1, y2, 'o',label="data")
plt.plot(x1, y_true2, 'b', label="True")
plt.plot(x1, resrlm.fittedvalues, 'orange', label="RLM")
plt.plot(x1, rlm_low_conf, '--', color='orange')
plt.plot(x1, rlm_upp_conf, '--', color='orange')
plt.plot(x1, rlm_low_pred, 'purple')
plt.plot(x1, rlm_upp_pred, 'purple')
plt.legend(loc="best")
