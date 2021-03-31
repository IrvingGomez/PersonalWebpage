#########################
##                     ##
## Irving Gomez Mendez ##
##    March 03, 2021   ##
##                     ##
#########################

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, uniform

# m(x) = e_1.T(X_x.T W_x X_x)**(-1) @ (X_x.T W_x Y)

def m(x):
    return (np.sin(2*np.pi*x**3))**3

n = 100
h = 0.024
epsilon = norm.rvs(scale=0.1, size=n)
x_dat = uniform.rvs(size=n)
y = np.array([m(xx) for xx in x_dat])

x_vect = np.linspace(0,1,100)
m_vect =  [m(xx) for xx in x_vect]

y_dat = y+epsilon

plt.figure(figsize=(15,7.5))
plt.scatter(x_dat, y+epsilon)
plt.plot(x_vect, m_vect, 'r--')

def hat_m(x):
    XX = np.vstack([np.ones(n),(x_dat-x)]).T
    W = np.diag(norm.pdf((x_dat-x)/h))
    beta_0 = np.linalg.solve(XX.T @ W @ XX, XX.T @ W @ y_dat)[0]
    return(beta_0)

hat_m_vect = [hat_m(xx) for xx in x_vect]

plt.figure(figsize=(15,7.5))
plt.scatter(x_dat, y+epsilon)
plt.plot(x_vect, m_vect, 'r--')
plt.plot(x_vect, hat_m_vect, 'purple')
