#########################
##                     ##
## Irving Gomez Mendez ##
##    April 02, 2021   ##
##                     ##
#########################

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate

x = np.linspace(-3, 3, 50)
y = np.exp(-x**2) + 0.1 * np.random.randn(50)
xs = np.linspace(-3, 3, 1000)

spl_1 = interpolate.UnivariateSpline(x, y, s = 0)
spl_2 = interpolate.UnivariateSpline(x, y, s = 0.5)
spl_3 = interpolate.UnivariateSpline(x, y, s = 3)

plt.figure(figsize=(7.5,5))
plt.plot(xs, spl_1(xs), 'g', lw=2)
plt.plot(xs, spl_2(xs), 'b', lw=2)
plt.plot(xs, spl_3(xs), 'y', lw=2)
plt.plot(x, y, 'ro', ms=5)
