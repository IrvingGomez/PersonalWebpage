#########################
##                     ##
## Irving Gomez Mendez ##
##    May 11, 2021     ##
##                     ##
#########################
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.stats import boxcox, chi2_contingency
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.model_selection import RepeatedKFold
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import variance_inflation_factor

def hist_variable(data, variable, binwidth=None):
    plt.figure(figsize=(10,7.5))
    sns.histplot(data=data, x=variable, stat='density', color='rebeccapurple')
    sns.kdeplot(data=data, x=variable, fill=True, color='rebeccapurple', linewidth=2)

dat = pd.read_csv("bank_additional/bank-additional.csv", sep=';')
dat = dat.rename(columns={'y':'deposit'})
dat = dat.astype({
    'job': 'category',
    'marital': 'category',
    'education': 'category',
    'default': 'category',
    'housing': 'category',
    'loan': 'category',
    'contact': 'category',
    'month': 'category',
    'day_of_week': 'category',
    'poutcome': 'category',
    'deposit': 'category'})

dat = dat[['duration', 'emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']]

# Brief description of the data
dat.describe()

hist_variable(dat, 'duration')

dat = dat[dat['duration'] > 0]

# We can perform a Box-Cox transformation to normalize the duration?
duration_transform, lamb = boxcox(dat['duration'])

lamb

plt.figure(figsize=(10,7.5))
sns.histplot(duration_transform, stat='density', color='rebeccapurple')
sns.kdeplot(duration_transform, fill=True, color='rebeccapurple', linewidth=2)

np.mean(duration_transform)
np.std(duration_transform)

(duration_transform*lamb+1)**(1/lamb)

dat['duration_transform'] = duration_transform

##############################
##                          ##
## Social and economic data ##
##                          ##
##############################
dat_social_economic = dat[['emp.var.rate', 'cons.price.idx', 'cons.conf.idx', 'euribor3m', 'nr.employed']]
np.round(dat_social_economic.describe(),3)

# We check the condition number
np.linalg.cond(dat_social_economic)
# The condition number is too big, we can see that nr.employed has a different scale that the other features.
# It could be better to standardize this data

dat_social_economic_scale = StandardScaler().fit_transform(dat_social_economic)
dat_social_economic_scale = pd.DataFrame(dat_social_economic_scale, columns=dat_social_economic.columns)

np.linalg.cond(dat_social_economic_scale)
# The condition number is low now, but it could mean a moderate to high correlation between variables

# Kendall-Silvey suggestion as follows: there are as many near dependencies among the columns of a data matrix X as
# there are high condition indexes (singular values small relative to p,,). Two points regarding this extension must be emphasized.

# weak dependencies are associated with condition indexes around 5 or 10, whereas moderate to strong
# relations are associated with condition indexes of 30 to 100.

corr_matrix = dat_social_economic_scale.corr()

plt.figure(figsize=(10,7.5))
sns.heatmap(corr_matrix, cmap='Purples')
# It looks like 4 variables, except cons.conf.idx are highly correlated
# Especially euribor3m and nr.employed, we could just select one of these variables

# We calculate the Variance Inflation Factors

#One recommendation is that if VIF is greater than 5, then the explanatory
#variable given by exog_idx is highly collinear with the other explanatory
#variables, and the parameter estimates will have large standard errors
#because of this.

vif = pd.DataFrame()
vif["VIF Factor"] = np.round([variance_inflation_factor(dat_social_economic_scale.values, i) for i in range(dat_social_economic_scale.shape[1])],2)
vif["features"] = dat_social_economic_scale.columns
vif

np.diag(np.linalg.inv(dat_social_economic_scale.T @ dat_social_economic_scale))*4119
np.diag(np.linalg.inv(corr_matrix))

# Let's do the pairplot.

plt.figure(figsize=(5,5))
sns.pairplot(dat_social_economic_scale, kind="reg", corner = True,
    plot_kws={'line_kws':{'color':'orange'}, 'scatter_kws':{'color': 'rebeccapurple'}},
    diag_kws={'color': 'rebeccapurple'})

# We can check all the condition indexes
u, d, vt = np.linalg.svd(dat_social_economic_scale)
v = vt.T

np.round(d[0]/d,2)
# There are two conditions indexes above 10, the rest are below 5. This would mean that there
# are 2 collinearities in the data
phis = v**2/d**2
var_decomp_portions = phis.T/sum(phis.T)

plt.figure(figsize=(10,7.5))
ax = sns.heatmap(var_decomp_portions, cmap='Purples')
ax.xaxis.set_ticklabels(dat_social_economic_scale.columns)
# This suggests a collinearity between the last 3 variables (especially the last 2)
# and another collinearity between the first two variables
