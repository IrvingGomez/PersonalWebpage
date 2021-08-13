#########################
##                     ##
## Irving Gomez Mendez ##
##     May 04, 2021    ##
##                     ##
#########################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# Data from Hosmer, D.W. & Lemeshow, S. (1989) Applied logistic regression. Wiley
# Data are ages (in years) and indicator of significant damage in the coronary of 100 people
dat = pd.read_csv('Heart_Disease_vs_Age.csv')
n = dat.shape[0]
X = np.vstack([np.ones(n), dat['age']]).T
y = dat['chd']

# Logistic regression by hand
b = [0,0] # initial values

tolm   = 1e-6       # tolerance (minimum norm of the difference of the betas)
iterm  = 100        # maximum number of iterations
tolera = 1          # initialize tolera
itera  = 0          # initialize ittera
histo  = b          # initialize beta upgrade

while((tolera > tolm) and (itera < iterm)):
  p      = 1/(1+np.exp(-X @ b))
  W      = np.diag(p*(1-p))
  delta  = np.linalg.solve(X.T @ W @ X, X.T @ (y-p))
  b      = b+delta
  tolera = np.sqrt(sum(delta**2))
  histo  = np.vstack([histo, b])
  itera  = itera+1

histo

n0 = 50
x0 = np.linspace(dat['age'].min(), dat['age'].max(), n0)
X0 = np.vstack([np.ones(n0), x0]).T

plt.figure(figsize=(10,7.5))
plt.plot(dat['age'], dat['chd'], 'o')
plt.plot(x0, 1/(1+np.exp(-X0 @ b)), 'r'),
plt.xlabel('Age')
plt.ylabel('Prob. of Coronary Heart Disease')

# Using LogisticRegression
logreg = LogisticRegression(penalty='none')
logreg.fit(np.array(dat['age'])[:,None],y)

b_star = logreg.coef_[0]
b_star
logreg.intercept_

plt.figure(figsize=(10,7.5))
plt.plot(dat['age'], dat['chd'], 'o')
plt.plot(x0, (logreg.predict_proba(x0[:,None]).T)[1,], 'r'),
plt.xlabel('Age')
plt.ylabel('Prob. of Coronary Heart Disease')

###
