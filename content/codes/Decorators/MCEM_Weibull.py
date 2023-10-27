# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 20:35:52 2016

@author: Dmitri
"""

from numpy import exp, log, arange, ceil, log2, array, mean, percentile, append
from pylab import hist, plot, figure
from scipy.stats import uniform, gamma, weibull_min
from time import clock
from numpy.random import choice

#######################################################
#######################################################
#######################################################

class MCEM_Weibull:
    muestra = []
    eta = 0
    beta = 0
    t = []
    n = 0
    p = []
    medio = []
    x = []
    cadena = []

    def __init__(self,n,eta,beta,t):
        self.eta = eta
        self.beta = beta

        self.t = append([0], t)
        self.t = append(self.t, [float("inf")])

        self.n = n
        self.x = (self.t/eta)**beta

        self.p = []
        for j in range(0,len(self.t)-2):
            aux = exp(-self.x[j])-exp(-self.x[j+1])
            self.p += [aux]
        self.p += [1-sum(self.p)]
        self.muestra = choice(len(self.t)-1, size=self.n, p=self.p)

        self.medio = array([0.0]*len(self.muestra))
        for j in range(0,len(self.t)-2):
            self.medio[self.muestra == j] = (self.t[j+1]+self.t[j])*0.5
        self.medio[self.muestra == len(self.t)-2] = self.t[len(self.t)-2]

    def inic_cadena(self):
        '''
        Esta función inicializa la cadena
        '''

        # The gringorten formula
        y = arange((1-0.44)/(self.n+0.12),(self.n+1-0.44)/(self.n+0.12),1/(self.n+0.12))
        tau = map(lambda x: log(log(1/(1-x))), y)
        x = sorted(log(self.medio))

        x_bar = mean(x)
        y_bar = mean(y)

        Sxy = sum((array(x)-x_bar)*(y-y_bar))
        Sxx = sum((array(x)-x_bar)**2)

        b = Sxy/Sxx
        a = mean(tau)-x_bar*b

        eta = exp(-a/b)
        beta = b
        self.cadena += [[eta, beta]]

ejemplo = MCEM_Weibull(n=20,eta=10,beta=2,t=array([3.0,8.0,13.0,21.0,23.0]))
ejemplo.eta
ejemplo.beta
ejemplo.cadena
ejemplo.muestra
ejemplo.medio
ejemplo.p
ejemplo.x
ejemplo.t
ejemplo.n

ejemplo.inic_cadena()

ejemplo.cadena

len(ejemplo.muestra)


ejemplo.inic_cadena()
ejemplo.cadena

yy = arange((1-0.44)/(20+0.12),(20+1-0.44)/(20+0.12),1/(20+0.12))
ttau = map(lambda x: log(log(1/(1-x))), yy)

yy

aaa = float("inf")
exp(-aaa)

yy-mean(yy)


(ejemplo.medio*ejemplo.muestra)**2





mean(sorted(log(ejemplo.medio)))
