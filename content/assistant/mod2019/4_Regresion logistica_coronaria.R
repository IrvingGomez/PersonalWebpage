library(R330)
data(chd.df)
dat = chd.df

dim(dat) # 100x2

# Los datos son edades (en años) e indicadores de presencia
# o ausencia de daño significativo en la coronaria de 100
# individuos seleccionados para participar en el estudio

# Deseamos establecer una relación entre la edad de una persona
# y su propensión a padecer un problema en la coronaria

# Datos de Hosmer, D.W. & Lemeshow, S. (1989)
# Applied logistic regression. Wiley

# Grafica de los datos
edad = dat$age
coro = dat$chd

edaj = jitter(edad)             # solo con fines de graficacion

x11()
plot(edaj, coro, xlab="Edad", ylab="Indicador CHD",
     ylim=c(-0.1,1.1),
     mgp=c(1.5,0.5,0), cex.axis=0.8, cex.lab=0.8, cex.main=1,
     xlim=c(15,75), cex=0.7, main="Regresion Lineal",
     pch=ifelse(coro==1, "1", "0"))
rug(edaj)
out = lm(coro~edad)
abline(out,lwd=2,col="blue")    # esta es la recta de regresion

# Resolviendo ecuaciones de verosimilitud. Metodo de Newton.
y = coro
n = length(y)
X = cbind(rep(1,n),edad)
b = c(-10,0.2)             # valores iniciales

# Las 4 lineas anteriores son especificas para los datos
# de enfermedadesdel corazon. Las siguientes son generales
# y se aplican para cualquier otra y y X's (incluso X con
# mas variables predictoras)

tolm   = 1e-6       # tolerancia (norma minima de delta)
iterm  = 100        # numero maximo de iteraciones
tolera = 1          # inicializar tolera
itera  = 0          # inicializar itera
histo  = b          # inicializar historial de iteraciones

while((tolera>tolm)&(itera<iterm)){
  p      = 1/(1+exp(-as.vector(X%*%b)))
  W      = p*(1-p)
  delta  = as.vector(solve(t(X*W)%*%X, t(X)%*%(y-p)))
  b      = b+delta
  tolera = sqrt(sum(delta^2))
  histo  = rbind(histo, b)
  itera  = itera+1
}

histo

# histo -10.000000 0.20000000
# b      -1.404259 0.03586446
# b      -4.344716 0.09181704
# b      -5.190388 0.10857390
# b      -5.277587 0.11030380
# b      -5.278444 0.11032079
# b      -5.278444 0.11032079

#Graficamos la regresion logistica
x11()
plot(edaj, coro, xlab="Edad", ylab="Indicador CHD",
     ylim=c(-0.1,1.1),
     mgp=c(1.5,0.5,0), cex.axis=0.8, cex.lab=0.8, cex.main=1,
     xlim=c(15,75), cex=0.7, main="Regresion Logística",
     pch=ifelse(coro==1, "1", "0"))
rug(edaj)
xx = seq(15,75,length=200)
X  = cbind(rep(1,n), xx)
p = 1/(1+exp(-as.vector(X%*%b)))
lines(xx,p,lwd=2,col="blue")


