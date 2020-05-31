# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 22:59:23 2016

@author: Dmitri
"""

from numpy import log2, mean, std, ceil, arange, sqrt, zeros, log
from pylab import hist, title, plot, figure, ylabel, xlabel, axis, step
from scipy.stats import norm
from statsmodels.distributions import ECDF

# Aquí simula n normales padrón, saca su media, su varianza
# y hace un histogrma
nn=1000
x=norm.rvs(size=nn)
print(mean(x))
print(std(x))

hist(x,bins=int(ceil(log2(nn)))+1,color='purple',density=True, range=(-4,4))
title(u'Histograma de una Normal Padrón 'r'$\mathcal{N}(0,\ 1)$')

# Aquí hace la densidad de una Beta Incompleta
x=arange(start=0,stop=1,step=0.05)
y=x*0.3**(x-1)

plot(x,y,'purple',linewidth=3)
title('Verosimilitud de una Beta Incompleta')
ylabel(r'f(x; $\theta$)')
xlabel(r'$\theta$')

# Cómo hacer una ECDF (Empirical Cumulative Distribution Function)
# y sus bandas de confianza (tal como me dijo Caro)

########################
### GRACIAS Caro !!! ###
########################

def U(muestra,alpha):
    n=len(muestra)
    epsilon=sqrt(log(2./alpha)/(2*n))
    ecdf=ECDF(muestra)
    nn=len(ecdf.y)
    out=zeros(nn)
    for i in range(0,nn):
        out[i]=min(ecdf.y[i]+epsilon,1)
    return out

def L(muestra,alpha):
    n=len(muestra)
    epsilon=sqrt(log(2./alpha)/(2*n))
    ecdf=ECDF(muestra)
    nn=len(ecdf.y)
    out=zeros(nn)
    for i in range(0,nn):
        out[i]=max(ecdf.y[i]-epsilon,0)
    return out

########################
###  Un ejemplo !!!  ###
########################

N=21 #tamaño de la muestra
mm=norm.rvs(size=N)
aa=0.05 #alpha

col='purple'
col2='tomato'
x1=-4   #xlim=x1,x2
x2=4

ecdf=ECDF(mm)

axis([x1,x2,-0.01,1.01])
step(ecdf.x,ecdf.y,where='post',linewidth=2,color=col)
step(ecdf.x,U(mm,aa),where='post',linewidth=2,color=col2)
step(ecdf.x,L(mm,aa),where='post',linewidth=2,color=col2)

# Esto es para darle la colita a las bandas y a la función empírica
plot([x1,min(mm)],[U(mm,aa)[0],U(mm,aa)[0]],linewidth=2,color=col2)
plot([max(mm),x2],[L(mm,aa)[N],L(mm,aa)[N]],linewidth=2,color=col2)

plot([x1,min(mm)],[0,0],linewidth=2,color=col)
plot([max(mm),x2],[1,1],linewidth=2,color=col)

# Esto es para graficar la función de distribución de normal
plot(arange(x1,x2,0.01),norm.cdf(arange(x1,x2,0.01)),
         color='g',linewidth=2)

#############################################
#############################################
