## Irving Gómez
## 13 September 2019

set.seed(111)
nn <- 50
mm <- 2.5
ss <- 2.5
muestra = rnorm(nn,mm,ss)

emv <- c(mean(muestra),
         sqrt((nn-1)/nn)*sd(muestra)) # 2.013931 2.950755

# Funcion de logverosimilitud global
logver <- function(theta, x = muestra){
  mu     <- theta[1]
  sigma  <- theta[2]
  n      <- length(x)
  t1     <- sum(x)
  t2     <- sum(x^2)
  return(-n*log(sigma)-1/(2*sigma^2)*(t2-2*mu*t1+n*mu^2))
}

# En el caso de EMV por optimizacion numerica usamos 
# funcion auxiliar para maximizar
# notar que se trata de menos la logverosimilitud ya que la funcion
# "optim" minimiza

faux <- function(theta){
  -logver(theta, x = muestra)
}

tilde.mu    <- median(muestra)            
tilde.sigma <- abs(muestra[1]-muestra[2]) 

# Valores Iniciales
c(tilde.mu, tilde.sigma) # 2.155335 1.414891

# Funcion "optim"
emv.optim <- optim(c(tilde.mu, tilde.sigma), faux)$par
emv.mu <- emv.optim[1]
emv.sigma <- emv.optim[2]

# Maximos Verosimiles
emv.optim # 2.013606 2.950522

# Funcion de verosimilitud relativa
Relativa <- function(mu, sigma, x = muestra){
  theta <- c(mu, sigma)
  exp(logver(theta, x)-logver(emv.optim, x))
}

aux <- Vectorize(Relativa, vectorize.args = c('mu', 'sigma'))

# Calculemos la verosimilitud relativa para una rejilla de valores de mu y de sigma
nmu <- 100
nsigma  <- 100

mu_seq <- seq(0.5, 3.5, length=nmu)
sigma_seq  <- seq(2, 4, length=nsigma)

Relativa.grid = outer(mu_seq, sigma_seq, aux)

x11()
persp(mu_seq, sigma_seq, Relativa.grid,
      theta=45,
      phi=20,
      zlim=c(0,1),
      xlab=expression(mu),
      ylab=expression(sigma),
      zlab="Relativa", col="purple")

# Contornos de verosimilitud
x11()
contour(mu_seq, sigma_seq, Relativa.grid, main='Contornos',
        levels=c(0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),
        labels=c(0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),
        labcex=1,xlim=c(0.5,3.5),ylim=c(2,4),
        xlab=expression(mu),
        ylab=expression(sigma),
        cex.lab=1,
        cex.axis=1,
        xaxs="i",
        yaxs="i")

# logversomilitud perfil de mu
lpmu <- function(mu, x = muestra){
  n  <- length(x)
  t1 <- sum(x)
  t2 <- sum(x^2)
  w  <- t2-2*mu*t1+n*mu^2
  return(-n/2*(1+log(w/n)))
}

lp_mu <- sapply(mu_seq, lpmu)

x11()
plot(mu_seq, lp_mu, type="l",col=1,lwd=1,
     main="Logverosimilitud Perfil de mu",
     xlab=expression(mu),
     ylab=expression(l[p](mu)))

abline(v=emv.mu,col=2,lty=2)

# logverosimilitud perfil de sigma
lpsigma <- function(sigma, x = muestra){
  n  <- length(x)
  t1 <- sum(x)
  t2 <- sum(x^2)
  return(-n*log(sigma)-1/(2*sigma^2)*(t2-t1^2/n))
}

lp_sigma <- sapply(sigma_seq, lpsigma)

x11()
plot(sigma_seq, lp_sigma, type="l",col=1,lwd=1,
     main="Logverosimilitud Perfil de sigma",
     xlab=expression(sigma),
     ylab=expression(l[p](sigma)))

abline(v=emv.sigma,col=2,lty=2)

# La trayectoria que se sigue para obtener verosimilitud perfil de sigma
x11()
contour(mu_seq, sigma_seq, Relativa.grid,
        main=expression(paste('Trayectoria para ', l[p](sigma))),
        levels=c(0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),
        labels=c(0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),
        labcex=1,xlim=c(0.5,3.5),ylim=c(2,4),
        xlab=expression(mu),
        ylab=expression(sigma),
        cex.lab=1,
        cex.axis=1,
        xaxs="i",
        yaxs="i")

abline(v=emv.mu,col=2)
points(emv.mu, emv.sigma, col='purple', pch=19)

sigma.rest <- function(mu, x = muestra){
  n  <- length(x)
  t1 <- sum(x)
  t2 <- sum(x^2)
  return(sqrt((t2-2*mu*t1+n*mu^2)/n))
}
  
sigma.rest_seq <- sapply(mu_seq, sigma.rest)

# La trayectoria que se sigue para obtener verosimilitud perfil de mu
x11()
contour(mu_seq, sigma_seq, Relativa.grid,
        main=expression(paste('Trayectoria para ', l[p](mu))),
        levels=c(0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),
        labels=c(0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9),
        labcex=1,xlim=c(0.5,3.5),ylim=c(2,4),
        xlab=expression(mu),
        ylab=expression(sigma),
        cex.lab=1,
        cex.axis=1,
        xaxs="i",
        yaxs="i")

points(mu_seq, sigma.rest_seq, type='l', col='tomato', lwd=2)
points(emv.mu, emv.sigma, col='purple', pch=19)

#PP plot
alphas <- seq(1/(nn+1), nn/(nn+1), length = nn)
pp     <- pnorm(sort(muestra), mean = emv.mu, sd = emv.sigma)
us_l   <- qbeta(0.025, 1:nn, (nn+1)-(1:nn))
us_u   <- qbeta(0.975, 1:nn, (nn+1)-(1:nn))

x11()
plot(alphas, pp,
     pch=19,
     col='purple',
     main="PP plot",
     xlab=expression(i/n+1),
     ylab=expression(u[i]),
     cex.lab=1.5,
     xlim=c(-0.05,1.05),
     ylim=c(-0.05,1.05),
     xaxs="i",
     yaxs="i")
curve(1*x, add = T)

points(alphas, us_l, type='l', col='tomato', lwd=2)
points(alphas, us_u, type='l', col='tomato', lwd=2)

#QQ plot
qq     <- qnorm(alphas, mean = emv.mu, sd = emv.sigma)
band_u_qq <- qnorm(us_u, mean = emv.mu, sd = emv.sigma)
band_l_qq <- qnorm(us_l, mean = emv.mu, sd = emv.sigma)

x11()
plot(qq, sort(muestra),
     pch=19,
     col='purple',
     main="QQ plot",
     xlab=expression(Q[i/n+1]),
     ylab=expression(x[i]),
     cex.lab=1.5,
     xlim=c(-6,10),
     ylim=c(-6,10),
     xaxs="i",
     yaxs="i")
curve(1*x, add = T)

points(qq, band_u_qq, type='l', col='tomato', lwd=2)
points(qq, band_l_qq, type='l', col='tomato', lwd=2)

# Funcion de distribucion empirica de nuestra muestra
F.emp<-ecdf(muestra)

# Bandas no parametricas
U <- function(x = muestra, alpha){
  n <- length(x)
  epsilon <- sqrt(log(2/alpha)/(2*n))
  ecdf    <- seq(1/n, n/n, length = n)
  out     <- c()
  for (i in 1:n){
    out <- c(out, min(ecdf[i]+epsilon,1))
  }
  return(out)
}

L <- function(x = muestra, alpha){
  n <- length(x)
  epsilon <- sqrt(log(2/alpha)/(2*n))
  ecdf    <- seq(1/n, n/n, length = n)
  out     <- c()
  for (i in 1:n){
    out <- c(out, max(ecdf[i]-epsilon,0))
  }
  return(out)
} 

# stepfun hace una funcion escalonadas, dando el lugar
# de los brincos y el tamanho de cada uno
# sapply aplica un vector a una funcion
xx <- seq(-6,10, length = 1000)

# bandas no parametricas
band_u <- sapply(xx,stepfun(sort(muestra),
                      c(U(x = muestra, 0.05),1)))

band_l <- sapply(xx,stepfun(sort(muestra),
                      c(0,L(x = muestra, 0.05))))
x11()
plot(F.emp,
     xlab="x", ylab=expression(paste(F[n](x), " & F(x)")),
     main="ECDF, verdadera CDF y bandas no parametricas",
     col="purple", lwd=2)
curve(pnorm(x, mean = mm, sd = ss), col='tomato', lwd=2, add=TRUE)
points(xx, band_u, type = 'l', col="forestgreen", lwd=2)
points(xx, band_l, type = 'l', col="forestgreen", lwd=2)

# bandas parametricas
band_u_param <- F.emp(xx)+
  qnorm(1-0.05/2)/sqrt(nn)*sqrt(F.emp(xx)*(1-F.emp(xx)))

band_u_param[which(band_u_param > 1)] <- 1

band_l_param <- F.emp(xx)-
  qnorm(1-0.05/2)/sqrt(nn)*sqrt(F.emp(xx)*(1-F.emp(xx)))

band_l_param[which(band_l_param < 0)] <- 0

x11()
plot(F.emp,
     xlab="x", ylab=expression(paste(F[n](x), " & F(x)")),
     main="ECDF, verdadera CDF y bandas parametricas",
     col="purple", lwd=2)
curve(pnorm(x, mean = mm, sd = ss), col='tomato', lwd=2, add=TRUE)
points(xx, band_u_param, type = 'l', col="forestgreen", lwd=2)
points(xx, band_l_param, type = 'l', col="forestgreen", lwd=2)


