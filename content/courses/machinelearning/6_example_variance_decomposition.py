import numpy as np
np.set_printoptions(suppress=True)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
#from tabulate import tabulate

sss = pd.DataFrame(np.array([[-74, 80, 18, -56, -112],
    [14, -69, 21, 52, 104],
    [66, -72, -5, 764, 1528],
    [-12, 66, -30, 4096, 8192],
    [3, 8, -7, -13276, -26552],
    [4, -12, 4, 8421, 16842]]))

np.array([[-74, 80, 18, -56, -112],
    [14, -69, 21, 52, 104],
    [66, -72, -5, 764, 1528],
    [-12, 66, -30, 4096, 8192],
    [3, 8, -7, -13276, -26552],
    [4, -12, 4, 8421, 16842]])

np.linalg.cond(sss)

# matriz de correlacion
corr_matrix = pd.DataFrame(sss).corr()

corr_matrix.style.set_precision(4).background_gradient(cmap='Spectral', axis=None).to_excel('prueba.xlsx', engine='openpyxl')

plt.figure(figsize=(10,7.5))
sns.heatmap(corr_matrix, cmap='Spectral')

# factores de inflacion de la varianza
# vifs mayores a 5 pueden indicar colinealidad
vif = pd.DataFrame()
vif["VIF_Factor"] = np.round([variance_inflation_factor(sss.values, i) for i in range(sss.shape[1])],2)
vif["features"] = sss.columns
vif

# Para exportar la tabla de VIFs a latex
#print(tabulate(vif, vif.columns, tablefmt="latex"))

# Descomposicion SVD
u, d, vt = np.linalg.svd(sss)
v = vt.T

# valores singulares
d

d[4]

# indices de condicionamiento
d[0]/d

# analisis de descomposicion de la varianza
phis = v**2/d**2
var_decomp_portions = phis.T/sum(phis.T)

pd.DataFrame(var_decomp_portions).style.background_gradient(cmap='Purples', axis=None)

plt.figure(figsize=(10,7.5))
sns.heatmap(var_decomp_portions, cmap='Purples')
