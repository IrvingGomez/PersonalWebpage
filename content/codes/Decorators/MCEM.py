# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 13:07:52 2016

@author: Dmitri
"""

from scipy.stats import norm, truncnorm, binom
from numpy import mean, log, sqrt
from random import seed

from tabulate import tabulate

def EM_Normal(m, theta=3, sigma=1, a=3, eps_par=1e-07, eps_log=1e-10):
    '''
    Input:
    m:          tamaño de la muestra a simular
    theta:      media de la distribución normal
    sigma:      desviación de la distribución normal
    a:          umbral de censura (censura por la derecha tipo I)
    eps_par:    condición de paro en el parametro
    eps_log:    condición de paro en la logverosimilitud
    '''
    
    seed(157)    
    muestra = norm.rvs(loc=theta, scale=sigma, size=m)
    
    muestra[muestra>a] = a          # censuramos la muestra
    
    nocens = muestra[muestra!=a]    # muestra no censurada
    n      = len(nocens)            # cuenta el numero de valores no censurados
    barx   = mean(nocens)           # promedio de los datos no censurados
    
    parte1 = float(n)/m*barx        # una parte del nuevo estimador
    
    delta_par = eps_par+1           # criterio de paro en el parametro
    old_par   = mean(muestra)       # valor inicial del parámetro
    hist_par  = [round(old_par,3)]  # se guarda el historial del parámetro
    
    delta_log = eps_log+1           # criterio de paro en la logverosimilitud
                                    # valor inicial de la logverosimilitud
    old_log   = -0.5*sum((nocens-old_par)**2)+(m-n)*log(1-norm.cdf(a-old_par))
    hist_log  = [round(old_log,3)]  # se guarda el historial de la logverosimilitud    

    aux      = norm.pdf(a-old_par)/(1-norm.cdf(a-old_par))
    MLE      = barx + (m-n)/n*aux     # estima el MLE
    hist_MLE = [round(MLE,3)]       # se guarda el historial del estimador MLE

    MLE2      = MLE
    hist_MLE2 = [round(MLE,3)]
    
    while delta_par > eps_par and delta_log > eps_log:

        parte2    = old_par + aux                   # otra parte del estimador
        new_par   = parte1 + float(m-n)/m*parte2    # nuevo estimador EM
        delta_par = abs(new_par-old_par)
        old_par   = new_par
        hist_par  += [round(old_par,3)]

        # resultado auxiliar, necesario para el MLE y el EM
        aux = norm.pdf(a-old_par)/(1-norm.cdf(a-old_par))         
        
        MLE       = barx + float(m-n)/n*aux                # estima el MLE
        hist_MLE  += [round(MLE,3)]

        MLE2      = barx + float(m-n)/n*norm.pdf(a-MLE2)/(1-norm.cdf(a-MLE2))
        hist_MLE2 += [round(MLE2,3)]
        
        # Se evalua la logverosimilitud en la nueva estimación
        new_log = -0.5*sum((nocens-new_par)**2)+(m-n)*log(1-norm.cdf(a-new_par))
        delta_par = abs(new_log-old_log)
        old_log = new_log
        hist_log += [round(old_log,3)]

    return n, round(barx,3), round(new_par,3), hist_par, hist_log, hist_MLE, hist_MLE2
            
#################################
##                             ##
##   El resultado con m = 10   ##
##                             ##
#################################

res = EM_Normal(m=10.0)
itera = range(0,len(res[3]))

# lo siguiente es para escribir como tabla el resultado
headers = ["iteracion","hat(theta)", "logf(theta)", "ec(hat(theta))", "ecuacion"]
table = [itera,res[3],res[4],res[5],res[6]]
table = map(list, zip(*table))
# exporto la tabla a LaTeX
print tabulate(table,headers,tablefmt="latex")
            
            
def MCEM_Normal(M, m=10.0, n=2, barx=2.638, sigma=1, a=3, eps_par=1e-02, itmax=100):
    '''
    Input:
    m:          tamaño de la muestra
    n:          número de datos no censurados
    M:          número de muestras a simular
    barx:       media de los datos no censurados
    sigma:      desviación de la distribución normal
    a:          umbral de censura (censura por la derecha tipo I)
    eps_par:    condición de paro en el parametro
    '''
    
    delta_par = eps_par+1           # criterio de paro en el parametro
    # valor inicial del parámetro
    parte1    = float(n)/m*barx
    old_par   = parte1 + float(m-n)/m*a       
    hist_par  = [round(old_par,3)]  # se guarda el historial del parámetro
    
    it = 0    
    
    while delta_par > eps_par and it<itmax:

        muestra = truncnorm.rvs((a-old_par)/sigma, b=(float("inf")-old_par)/sigma,
                                loc=old_par, scale=sigma, size=M)
        aux = mean(muestra)
        
        new_par   = parte1 + float(m-n)/m*aux    # nuevo estimador EM
        delta_par = abs(new_par-old_par)
        old_par   = new_par
        hist_par  += [round(old_par,3)]

        it += 1        
        
    return hist_par    
    
res2 = MCEM_Normal(M=10)
itera = range(0,len(res2))

# lo siguiente es para escribir como tabla el resultado
headers = ["iteracion","MCEM"]
table = [itera,res2]
table = map(list, zip(*table))
# exporto la tabla a LaTeX
print tabulate(table,headers,tablefmt="latex")


####################
###              ###
###   inciso 3   ###
###              ###
####################

ppistar=(15+sqrt(53809))/394

def EM_Multi(x1=125, x2=18, x3=20, x4=34, pi=0.5, itmax=8, pistar=ppistar):
    
    pi_old = pi        
    err = abs(pi_old-pistar)
    hist_pi = [round(pi_old,9)]
    hist_err = [round(err,9)]
    hist_rel = []    
    
    it = 0
    
    while it < itmax:
        # Se reestima el parametro
        num = pi_old*x1/(2+pi_old)+x4
        dem = num+x2+x3
        pi_new = num/dem
        
        hist_pi += [round(pi_new,9)]
        
        err = abs(pi_new-pistar)
        hist_err += [round(err,9)]        
        
        err_rel = err/hist_err[-2]
        hist_rel += [round(err_rel,4)]
        
        pi_old = pi_new
        
        it += 1

    return hist_pi, hist_err, hist_rel
    
ppi, eerr, rrel = EM_Multi()

#lo siguiente es para escribir como tabla el resultado
itera = range(0,9)
headers = ["iteracion", "pi^(p)", "pi^(p)-pi^*", "(pi^(p+1)-pi^*)/(pi^(p)-pi^*)"]
table = [itera, ppi, eerr, rrel]
table = map(list, zip(*table))
#exporto la tabla a LaTeX
print tabulate(table,headers,tablefmt="latex")


ppistar=(15+sqrt(53809))/394

def MCEM_Multi(M, x1=125, x2=18, x3=20, x4=34, pi=0.5, itmax=8, pistar=ppistar):
    
    pi_old = pi        
    err = abs(pi_old-pistar)
    hist_pi = [round(pi_old,9)]
    hist_err = [round(err,9)]
    hist_rel = []    
    
    it = 0
    
    while it < itmax:

        muestra = binom.rvs(x1, pi_old/(2+pi_old), size=M)        
        aux = mean(muestra)        
        
        # Se reestima el parametro
        num = aux+x4
        dem = num+x2+x3
        pi_new = num/dem
        
        hist_pi += [round(pi_new,9)]
        
        err = abs(pi_new-pistar)
        hist_err += [round(err,9)]        
        
        err_rel = err/hist_err[-2]
        hist_rel += [round(err_rel,4)]
        
        pi_old = pi_new
        
        it += 1

    return hist_pi, hist_err, hist_rel
    
ppi, eerr, rrel = MCEM_Multi(M=1)

#lo siguiente es para escribir como tabla el resultado
itera = range(0,9)
headers = ["iteracion", "pi^(p)", "pi^(p)-pi^*", "(pi^(p+1)-pi^*)/(pi^(p)-pi^*)"]
table = [itera, ppi, eerr, rrel]
table = map(list, zip(*table))
#exporto la tabla a LaTeX
print tabulate(table,headers,tablefmt="latex")
