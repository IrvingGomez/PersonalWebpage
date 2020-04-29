# Clasificacion de digitos usando regresion logistica regularizada (a pie)
library(LiblineaR)

#setwd("~/CIMAT/2_Maestria/2° semestre/Modelos Estadisticos 1/Programas/10_Regresion logistica reguralizada_digits")

# Leemos los datos con los que se hara el ajuste
datos = scan("digitrain.txt")
dato  = matrix(datos, ncol=257, byrow=T)         # 7291 x 257
base  = 8;  vs = 3
dat   = dato[(dato[,1]==base)|(dato[,1]==vs),]   # 1200 x 257
y     = ifelse(dat[,1]==base,0,1)
dd    = as.data.frame(dat[,-1])
colnames(dd) = paste("X",1:(dim(dd)[2]), sep="")

# Ajustamos un modelo de regresion logistica regularizada
out   = LiblineaR(data=dd, target=y, type=6)  # la regularizacion es en L1

# Leemos los datos que usaremos para probar el modelo de clasificaion
datp  = scan("digitest.txt")
dap   = matrix(datp, ncol=257, byrow=T)          # 2007 x 257
dp    = dap[(dap[,1]==base)|(dap[,1]==vs),]      #  332 x 257
yp    = ifelse(dp[,1]==base,0,1)
d     = as.data.frame(dp[,-1])
colnames(d)  = paste("X",1:(dim(d)[2]), sep="")

# Evaluamos la bondad de prediccion con los datos de prueba

pre  = predict(out, d, decisionValues=T)
ypre = ifelse(pre$prediction==0, base, vs)
yobs = ifelse(yp==0, base, vs)
pp   = table(ypre, yobs)

pp
#    yobs
#ypre   3   8
#   3 161   6
#   8   5 160

100*sum(diag(pp))/sum(pp)   # 96.7 porcentaje de aciertos con los datos de prueba

# Con regresion logistica estandar se obtuvo:

#    yobs
#ypre   3   8
#   3 152   9
#   8  14 157

100*sum(diag(pp))/sum(pp)   # 93.1 porcentaje de aciertos con los datos de prueba