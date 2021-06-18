from pygam import LinearGAM, s, f #l, te, intercept

#y∼ExponentialFamily(μ|X)
#g(μ|X)=β0+f1(X1)+f2(X2,X3)+…+fM(XN)

#GAM (base class for constructing custom models)
#LinearGAM
#LogisticGAM
#GammaGAM
#PoissonGAM
#InvGaussGAM
#ExpectileGAM

#GAM(distribution='...')
#'normal'
#'binomial'
#'poisson'
#'gamma'
#'inv_gauss'

#GAM(link='...')
#'identity'
#'logit'
#'inverse'
#'log'
#'inverse-squared'

from pygam.datasets import wage
import matplotlib.pyplot as plt

X, y = wage(return_X_y=True)

#X[0] es el año X[0] = 0 es 2000?...
#X[1] es la edad de la persona
#X[2] es su nivel de estudios, 0 = basica, 1=media superior, 2 = universidad, 3= posgrado
#y ingresos $$

## model
gam1 = LinearGAM(s(0) + s(1) + f(2), fit_intercept = False)
gam1.gridsearch(X, y)

## plotting
plt.figure(figsize=(10,7.5))
fig, axs = plt.subplots(1,3)
titles = ['year', 'age', 'education']
for i, ax in enumerate(axs):
    XX = gam1.generate_X_grid(term=i)
    ax.plot(XX[:, i], gam1.partial_dependence(term=i, X=XX))
    ax.plot(XX[:, i], gam1.partial_dependence(term=i, X=XX, width=.95)[1], c='r', ls='--')
    ax.set_title(titles[i])
plt.rcParams['figure.figsize'] = [10, 7.5]

XX = [[2021, 29, 4]]
print(gam1.predict(XX))
for i in range(3):
    print(gam1.partial_dependence(term = i, X=XX))

## model
gam2 = LinearGAM(s(0, constraints='monotonic_inc') + s(1, constraints='concave') + f(2), fit_intercept = False)
gam2.gridsearch(X, y)

## plotting
fig, axs = plt.subplots(1,3)
titles = ['year', 'age', 'education']
for i, ax in enumerate(axs):
    XX = gam2.generate_X_grid(term=i)
    ax.plot(XX[:, i], gam2.partial_dependence(term=i, X=XX))
    ax.plot(XX[:, i], gam2.partial_dependence(term=i, X=XX, width=.95)[1], c='r', ls='--')
    ax.set_title(titles[i])

XX = [[2021, 29, 4]]
print(gam2.predict(XX))
for i in range(3):
    print(gam2.partial_dependence(term = i, X=XX))

gam3 = LinearGAM(s(0) + s(1, constraints = 'concave') + f(2), fit_intercept = False)
gam3.gridsearch(X, y)

## plotting
fig, axs = plt.subplots(1,3)
titles = ['year', 'age', 'education']
for i, ax in enumerate(axs):
    XX = gam3.generate_X_grid(term=i)
    ax.plot(XX[:, i], gam3.partial_dependence(term=i, X=XX))
    ax.plot(XX[:, i], gam3.partial_dependence(term=i, X=XX, width=.95)[1], c='r', ls='--')
    ax.set_title(titles[i])
