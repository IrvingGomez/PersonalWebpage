# Clasificacion de digitos usando regresion logistica regularizada (a pie)

#setwd("~/CIMAT/2_Maestria/2° semestre/Modelos Estadisticos 1/Programas/9_Regresion logistica reguralizada_digits")
datos = scan("digitrain.txt")
dato  = matrix(datos, ncol=257, byrow=T)         # 7291 x 257
base  = 8;  vs = 3
dat   = dato[(dato[,1]==base)|(dato[,1]==vs),]   # 1200 x 257
y     = ifelse(dat[,1]==base,0,1)
dd    = as.data.frame(dat[,-1])
colnames(dd) = paste("X",1:(dim(dd)[2]), sep="")

datp  = scan("digitest.txt")
dap   = matrix(datp, ncol=257, byrow=T)          # 2007 x 257
dp    = dap[(dap[,1]==base)|(dap[,1]==vs),]      #  332 x 257
yp    = ifelse(dp[,1]==base,0,1)
d     = as.data.frame(dp[,-1])
colnames(d)  = paste("X",1:(dim(d)[2]), sep="")

X   = as.matrix(dd)
y   = y
lam = 0.01

obj = function(p){
  b0 = p[1]
  b  = p[-1]
  Xb = X%*%b
  pp = 1/(1+exp(-b0)*exp(-Xb))
  return(-mean(log(1-pp)+y*Xb+y*b0)+lam*sum(b*b)/2)
}

ini = c(1,rep(0,256))
out = nlminb(ini, obj)

# Evaluamos la bondad de prediccion con los datos de prueba

b0op = out$par[1]
bop  = out$par[-1]
pred = 1/(1+exp(-b0op)*exp(-(as.matrix(d))%*%bop))
ypre = ifelse(pred<0.5, base, vs)
yobs = ifelse(yp==0, base, vs)
pp   = table(ypre, yobs)
100*sum(diag(pp))/sum(pp)   # 91.27 con lam=10
                            # 92.77 con lam=1
                            # 96.08 con lam=0.01
                            # 95.78 con lam=0.001
pred = 1/(1+exp(-b0op)*exp(-X%*%bop))
ypre = ifelse(pred<0.5, base, vs)
yobs = ifelse(y==0, base, vs)
pp   = table(ypre, yobs)

pp
#    yobs
#ypre   3   8
#   3 653   0
#   8   5 542

100*sum(diag(pp))/sum(pp)   # 99.58 con lam=0.01 para los datos de entrenamiento
