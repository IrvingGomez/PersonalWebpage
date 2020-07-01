## Irving Gomez
## 27 September 2019

set.seed(111)
nn      <- 50  # sample size
mm      <- 2.5 # real mean
ss      <- 2.5 # real standard deviation
muestra <- rnorm(nn,mm,ss)

# Sufficient and minimal statistics
t1 <- sum(muestra)
t2 <- sum(muestra^2)
H  <- t2-(t1^2/nn)

# Maximum likelihood estimators
mm.emv <- t1/nn          #2.013931
ss.emv <- sqrt(H/nn)  #2.950755

# Global loglikelihood
logver <- function(theta, mu_hat = mm.emv, s_hat = ss.emv, n = nn){
  mu     <- theta[1]
  sigma  <- theta[2]
  out    <- -n*(log(sigma)+1/2*(s_hat/sigma)^2)-n/(2*sigma^2)*(mu_hat-mu)^2
  return(out)
}

# Maximizing numericaly the global likelihood
faux <- function(theta){
  -logver(theta, mu_hat = mm.emv, s_hat = ss.emv, n = nn)
}

# Where to initialize the algorithm
tilde.mu    <- median(muestra)            #2.155335
tilde.sigma <- abs(muestra[1]-muestra[2]) #1.414891

# "optim" function
emv.optim <- optim(c(tilde.mu, tilde.sigma), faux)$par #2.013606 2.950522

# Relative loglikelihood
logrelver <- function(theta, mu_hat = mm.emv, s_hat = ss.emv, n = nn){
  mu     <- theta[1]
  sigma  <- theta[2]
  out    <- n*(log(s_hat/sigma)-1/2*(s_hat/sigma)^2+1/2)-n/2*((mu_hat-mu)/sigma)^2
  return(out)
}

# Relative likelihood
relver <- function(mu, sigma, mu_hat = mm.emv, s_hat = ss.emv, n = nn){
  theta <- c(mu, sigma)
  out   <- exp(logrelver(theta, mu_hat, s_hat, n))
  return(out)
}

# Using "persp" to plot in 3d the relative likelihood
relver_aux <- Vectorize(relver, vectorize.args = c('mu', 'sigma'))

# We create a sequence for mu and sigma
nmu     <- 100
nsigma  <- 100
mu1     <- 0.5
mu2     <- 3.5
s1      <- 2
s2      <- 4

mu_seq     <- seq(mu1, mu2, length=nmu)
sigma_seq  <- seq(s1, s2, length=nsigma)

# Evaluate the relative likelihood in the sequences created
relativa.grid <- outer(mu_seq, sigma_seq, relver_aux)

x11()
persp(mu_seq, sigma_seq, relativa.grid,
      theta = 45,
      phi   = 20,
      zlim  = c(0,1),
      xlab  = expression(mu),
      ylab  = expression(sigma),
      zlab  = 'Relativa',
      col   = 'purple')

# Likelihood contours

# It is not possible to find closed expressions for the contours,
# thus we need to make them numerically woth "contour"

niveles <- c(0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9)

x11()
contour(mu_seq, sigma_seq, relativa.grid,
        main     = "Likelihood Contours",
        levels   = niveles,
        labels   = niveles,
        xlim     = c(mu1,mu2), ylim = c(s1,s2),
        xlab     = expression(mu),
        ylab     = expression(sigma),
        xaxs     = 'i',
        yaxs     = 'i')

points(mm.emv, ss.emv, col = 'purple', pch = 19)
points(mm, ss, col = 'tomato', pch=19)

legend('topright',
       legend = c(expression(paste('(', hat(mu), ',' , hat(sigma), ')')),
                  expression(paste('(', mu[0], ',' , sigma[0], ')'))),
       pch    = 19,
       col    = c('purple', 'tomato'),
       bty    = 'n')

# Relative profile loglikelihood of mu
logprelver_mu <- function(mu, mu_hat = mm.emv, s_hat = ss.emv, n = nn){
  out <- -n/2*log(((mu_hat-mu)/s_hat)^2+1)
  return(out)
}

# Profile likelihood interval for mu
LI_mu <- function(c, mu_hat = mm.emv, s_hat = ss.emv, n = nn){
  mm1 <- mu_hat-s_hat*sqrt(c^(-2/n)-1)
  mm2 <- mu_hat+s_hat*sqrt(c^(-2/n)-1)
  out <- c(mm1, mm2)
  return(out)
}

x11()
par(mar = c(5, 5, 4, 2) + 0.1)
plot(mu_seq, exp(logprelver_mu(mu_seq)),
     type = 'l',
     main = expression(paste("Relative profile likelihood of ", mu)),
     xlab = expression(mu),
     ylab = expression(R[p](mu)),
     xaxs     = 'i',
     yaxs     = 'i')

abline(v = mm.emv, col = 'purple', lwd = 2)
abline(v = mm, col = 'tomato', lwd = 2)

for(cc in niveles){
  mm_int  <- LI_mu(cc)
  mm_int_1 <- mm_int[1]
  mm_int_2 <- mm_int[2]
  segments(mm_int_1, cc, mm_int_2, cc, col = 'forestgreen', lty = 2, lwd = 2)
}

legend('topright',
       legend = c(expression(hat(mu)), expression(mu[0]),
                  expression(LI[mu])),
       lwd    = 2,
       lty    = c(1,1,2),
       col    = c('purple', 'tomato', 'forestgreen'),
       bty    = 'n')


# Relative profile loglikelihood of sigma
logprelver_sigma <- function(sigma, s_hat = ss.emv, n = nn){
  out <- n*(log(s_hat/sigma)-1/2*(s_hat/sigma)^2+1/2)
  return(out)
}

x11()
par(mar = c(5, 5, 4, 2) + 0.1)
plot(sigma_seq, exp(logprelver_sigma(sigma_seq)),
     type = 'l',
     main = expression(paste("Relative profile likelihood of ", sigma)),
     xlab = expression(sigma),
     ylab = expression(R[p](sigma)),
     xaxs     = 'i',
     yaxs     = 'i')

abline(v = ss.emv, col = 'purple', lwd = 2)
abline(v = ss, col = 'tomato', lwd = 2)

# The likelihood intervals for sigma does not have closed form,
# we use "uniroot"
for(cc in niveles){
  interv_sigma_aux <- function(x){
    logprelver_sigma(x)-log(cc)
  }
  
  s_int_1 <- uniroot(interv_sigma_aux, c(s1, ss.emv))$root
  s_int_2 <- uniroot(interv_sigma_aux, c(ss.emv, s2))$root
  
  segments(s_int_1, cc, s_int_2, cc, col = 'forestgreen', lty = 2, lwd = 2)
}

legend('topright',
       legend = c(expression(hat(sigma)), expression(sigma[0]),
                  expression(LI[sigma])),
       lwd    = 2,
       lty    = c(1,1,2),
       col    = c('purple', 'tomato', 'forestgreen'),
       bty    = 'n')

# Maximum likelihood restricted estimator of  sigma
sigma.rest <- function(mu, s_hat = ss.emv, mu_hat = mm.emv){
  out <- sqrt(s_hat^2+(mu_hat-mu)^2)
  return(out)
}

sigma.rest_seq <- sigma.rest(mu_seq)

# Trajectory to get the profile of mu
x11()
contour(mu_seq, sigma_seq, relativa.grid,
        main     = expression(paste("Trajectory to get ", R[p](mu))),
        levels   = niveles,
        labels   = niveles,
        xlim     = c(mu1,mu2), ylim = c(s1,s2),
        xlab     = expression(mu),
        ylab     = expression(sigma),
        xaxs     = 'i',
        yaxs     = 'i')

points(mm.emv, ss.emv, col = 'purple', pch = 19)
points(mm, ss, col = 'tomato', pch = 19)
points(mu_seq, sigma.rest_seq, type = 'l', col = 'forestgreen', lwd = 2)

legend('topright',
       legend = c(expression(paste('(', hat(mu), ',' , hat(sigma), ')')),
                  expression(paste('(', mu[0], ',' , sigma[0], ')'))),
       pch    = 19,
       col    = c('purple', 'tomato'),
       bty    = 'n')

# Trajectory to get the profile of sigma
x11()
contour(mu_seq, sigma_seq, relativa.grid,
        main     = expression(paste("Trajectory to get ", R[p](sigma))),
        levels   = niveles,
        labels   = niveles,
        xlim     = c(mu1,mu2), ylim = c(s1,s2),
        xlab     = expression(mu),
        ylab     = expression(sigma),
        xaxs     = 'i',
        yaxs     = 'i')

points(mm.emv, ss.emv, col = 'purple', pch = 19)
points(mm, ss, col = 'tomato', pch = 19)
abline(v = mm.emv, col = 'forestgreen', lwd = 2)

legend('topright',
       legend = c(expression(paste('(', hat(mu), ',' , hat(sigma), ')')),
                  expression(paste('(', mu[0], ',' , sigma[0], ')'))),
       pch    = 19,
       col    = c('purple', 'tomato'),
       bty    = 'n')

# The next approximations are find with the symmetric
# reparametrization ideas of Eloisa Diaz-Frances

# Approximated relative profile loglikelihood of sigma
logprelver_aprox_sigma <- function(sigma, s_hat = ss.emv, n = nn){
  out <- -9*n/4*(1-(s_hat/sigma)^(2/3))^2
  return(out)
}

# Approximated profile likelihood interval for sigma
s1_star <- function(c, s_hat = ss.emv, n = nn){
  s_hat*(1+1/3*sqrt(-4*log(c)/n))^(-3/2)
}

s2_star <- function(c, s_hat = ss.emv, n = nn){
  s_hat*(1-1/3*sqrt(-4*log(c)/n))^(-3/2)
}

x11()
par(mar = c(5, 5, 4, 2) + 0.1)
plot(sigma_seq, exp(logprelver_aprox_sigma(sigma_seq)),
     type = 'l',
     main = expression(paste("Approximated relative profile likelihood of ", sigma)),
     xlab = expression(sigma),
     ylab = expression({R^'*'}[p](sigma)),
     xaxs = 'i',
     yaxs = 'i')

abline(v = ss.emv, col = 'purple', lwd = 2)
abline(v = ss, col = 'tomato', lwd = 2)

for(cc in niveles){
  ss_int_1 <- s1_star(cc)
  ss_int_2 <- s2_star(cc)
  segments(ss_int_1, cc, ss_int_2, cc, col = 'forestgreen', lty = 2, lwd = 2)
}

legend('topright',
       legend = c(expression(hat(sigma)), expression(sigma[0]),
                  expression(hat(LI)[sigma])),
       lwd    = 2,
       lty    = c(1,1,2),
       col    = c('purple', 'tomato', 'forestgreen'),
       bty    = 'n')

# Approximated likelihood contours
aprox_cont_rel_left <- function(c2, nsigma = 100,
                                s_hat = ss.emv, mu_hat = mm.emv, n = nn){
  s1     <- s1_star(c2, s_hat, n)
  s2     <- s2_star(c2, s_hat, n)
  s_seq  <- seq(s1, s2, length = nsigma)
  # because we have a sqrt, to prevent NaNs we have to be sure that
  # the things inside are positive
  w <- -2*log(c2)/n-9/2*(1-(s_hat/s_seq)^(2/3))^2
  if(any(w<0)){
    k <- which(w<0)
    w[k] <- 0
  }
  p1_seq <- mu_hat-s_seq*sqrt(w)
  out    <- cbind(p1_seq, s_seq)
  return(out)
}

aprox_cont_rel_right <- function(c2, nsigma = 100,
                                 s_hat = ss.emv, mu_hat = mm.emv, n = nn){
  s1     <- s1_star(c2, s_hat, n)
  s2     <- s2_star(c2, s_hat, n)
  s_seq  <- seq(s1, s2, length = nsigma)
  # because we have a sqrt, to prevent NaNs we have to be sure that
  # the things inside are positive
  w <- -2*log(c2)/n-9/2*(1-(s_hat/s_seq)^(2/3))^2
  if(any(w<0)){
    k <- which(w<0)
    w[k] <- 0
  }
  p1_seq <- mu_hat+s_seq*sqrt(w)
  out    <- cbind(p1_seq, s_seq)
  return(out)
}

points_left  <- aprox_cont_rel_left(niveles[1])
points_right <- aprox_cont_rel_right(niveles[1])
#mu1 <- min(points_left[,1])
#mu2 <- 2*points_left[1,1]-min(points_left[,1])

x11()
plot(points_left,
     main = "Approximated Likelihood Contours",
     xlim = c(mu1,mu2), ylim = c(s1,s2),
     type = 'l',
     xlab = expression(mu),
     ylab = expression(sigma),
     xaxs = 'i',
     yaxs = 'i')
points(points_right, type = 'l')

for(cc in niveles[2:length(niveles)]){
  points_left  <- aprox_cont_rel_left(cc)
  points_right <- aprox_cont_rel_right(cc)
  
  points(points_left, type = 'l')
  points(points_right, type = 'l')
}

points(mm.emv, ss.emv, col = 'purple', pch = 19)
points(mm, ss, col = 'tomato', pch = 19)

legend('topright',
       legend = c(expression(paste('(', hat(mu), ',' , hat(sigma), ')')),
                  expression(paste('(', mu[0], ',' , sigma[0], ')'))),
       pch    = 19,
       col    = c('purple', 'tomato'),
       bty    = 'n')

# How well is this estimation?

# library scales is necessary to get the "alphas" function for colors
library(scales)

# Histogram
x11()
hist(muestra,
     freq = F,
     col = alpha('cornflowerblue', 0.1),
     main = 'Histogram',
     xlab = 'sample',
     xlim = c(-6,10),
     ylim = c(0,0.2),
     xaxs = 'i',
     yaxs = 'i')
curve(dnorm(x, mm.emv, ss.emv),
      col = 'purple',
      lwd = 2,
      add = T)
curve(dnorm(x, mm, ss),
      col = 'tomato',
      lwd = 2,
      add = T)

legend('topright',
       legend = c(expression(f[ML]),
                  expression(f[0])),
       lwd    = 2,
       col    = c('purple', 'tomato'),
       bty    = 'n')

# The bandwidth is determined with the Silverman(Scott)'s thumb rule
x11()
plot(density(muestra,
             bw     = 1.06*ss.emv*nn^(-1/5),
             kernel = 'gaussian'),
     main = "Kernel estimation",
     col  = 'cornflowerblue',
     lwd  = 2,
     xlim = c(-6,10),
     ylim = c(0,0.2),
     xaxs = 'i',
     yaxs = 'i')
curve(dnorm(x, mm.emv, ss.emv),
      col = 'purple',
      lwd = 2,
      add = T)
curve(dnorm(x, mm, ss),
      col = 'tomato',
      lwd = 2,
      add = T)

legend('topright',
       legend = c(expression(f[Kernel]),
                  expression(f[ML]),
                  expression(f[0])),
       lwd    = 2,
       col    = c('cornflowerblue', 'purple', 'tomato'),
       bty    = 'n')

# PP plot
alphas  <- seq(1/(nn+1), nn/(nn+1), length = nn)
pp      <- pnorm(sort(muestra), mean = mm.emv, sd = ss.emv)
pp_real <- pnorm(sort(muestra), mean = mm, sd = ss)
alphita <- 0.05 # Confidence level
us_l    <- qbeta(alphita/2, 1:nn, (nn+1)-(1:nn))
us_u    <- qbeta(1-alphita/2, 1:nn, (nn+1)-(1:nn))

x11()
par(mar = c(5, 5, 4, 2) + 0.1)
plot(alphas, pp,
     pch     = 19,
     col     = 'purple',
     main    = "PP plot",
     xlab    = expression(i/n+1),
     ylab    = expression(u[i]),
     cex.lab = 1.5,
     xlim    = c(-0.05,1.05),
     ylim    = c(-0.05,1.05),
     xaxs    = 'i',
     yaxs    = 'i')
points(alphas, pp_real,
       pch     = 19,
       col     = 'tomato')
curve(1*x, add = T)

points(alphas, us_l, type='l', col='forestgreen', lwd=2)
points(alphas, us_u, type='l', col='forestgreen', lwd=2)

legend('topleft',
       legend = c(expression(paste(i/n+1, ' X ', F[ML](x[(i)]))),
                  expression(paste(i/n+1, ' X ', F[0](x[(i)]))),
                  "Conf. Band"),
       lwd    = 2,
       col    = c('purple', 'tomato', 'forestgreen'),
       bty    = 'n')

# QQ plot
qq        <- qnorm(alphas, mean = mm.emv, sd = ss.emv)
qq_real   <- qnorm(alphas, mean = mm, sd = ss)
band_u_qq <- qnorm(us_u, mean = mm.emv, sd = ss.emv)
band_l_qq <- qnorm(us_l, mean = mm.emv, sd = ss.emv)

x11()
par(mar = c(5, 5, 4, 2) + 0.1)
plot(qq, sort(muestra),
     pch     = 19,
     col     = 'purple',
     main    = "QQ plot",
     xlab    = expression(Q[i/n+1]),
     ylab    = expression(x[i]),
     cex.lab = 1.5,
     xlim    = c(-6,10),
     ylim    = c(-6,10),
     xaxs    = 'i',
     yaxs    = 'i')
points(qq_real, sort(muestra),
       pch     = 19,
       col     = 'tomato')
curve(1*x, add = T)

points(qq, band_u_qq, type='l', col='forestgreen', lwd=2)
points(qq, band_l_qq, type='l', col='forestgreen', lwd=2)

legend('topleft',
       legend = c(expression(paste({F^{-1}}[ML](i/n+1), ' X ', x[(i)])),
                  expression(paste({F^{-1}}[0](i/n+1), ' X ', x[(i)])),
                  "Conf. Band"),
       lwd    = 2,
       col    = c('purple', 'tomato', 'forestgreen'),
       bty    = 'n')

# Empirical cumulative distribution function of the sample
F.emp <- ecdf(muestra)

# Non-parametric bands using
#Dvoretzky–Kiefer–Wolfowitz's & Massart's inequalities
U <- function(alpha = alphita, n = nn){
  epsilon <- sqrt(log(2/alpha)/(2*n))
  ecdf    <- seq(1/n, n/n, length = n)
  out     <- c()
  for (i in 1:n){
    out <- c(out, min(ecdf[i]+epsilon,1))
  }
  return(out)
}

L <- function(alpha = alphita, n = nn){
  epsilon <- sqrt(log(2/alpha)/(2*n))
  ecdf    <- seq(1/n, n/n, length = n)
  out     <- c()
  for (i in 1:n){
    out <- c(out, max(ecdf[i]-epsilon,0))
  }
  return(out)
} 

# "stepfun" makes a step function, giving the places of the jumps
# and the high of eacn one

# "sapply" applies function to a vector
xx <- seq(-6,10, length = 1000)

# Non-parametric bands
band_u <- sapply(xx,stepfun(sort(muestra),c(U(),1)))
band_l <- sapply(xx,stepfun(sort(muestra),c(0,L())))

x11()
par(mar = c(5, 5, 4, 2) + 0.1)
plot(F.emp,
     xlab = 'x',
     ylab = expression(paste(F[n](x), ', ', F[ML](x), ' & ', F[0](x))),
     main = "Cumulative distribution functions",
     col  = 'cornflowerblue',
     lwd  = 1,
     xaxs = 'i',
     yaxs = 'i')
curve(pnorm(x, mean = mm.emv, sd = ss.emv), col='purple', lwd=2, add=TRUE)
curve(pnorm(x, mean = mm, sd = ss), col='tomato', lwd=2, add=TRUE)
points(xx, band_u, type = 'l', col="forestgreen", lwd=2)
points(xx, band_l, type = 'l', col="forestgreen", lwd=2)

legend('topleft',
       legend = c(expression(F[n](x)),
                  expression(F[ML](x)),
                  expression(F[0](x)),
                  "Non-param. Conf. Band"),
       lwd    = 2,
       col    = c('cornflowerblue' ,'purple', 'tomato', 'forestgreen'),
       bty    = 'n')

# Parametric bands using CLT
band_u_param <- F.emp(xx)+
  qnorm(1-alphita/2)/sqrt(nn)*sqrt(F.emp(xx)*(1-F.emp(xx)))

band_u_param[which(band_u_param > 1)] <- 1

band_l_param <- F.emp(xx)-
  qnorm(1-alphita/2)/sqrt(nn)*sqrt(F.emp(xx)*(1-F.emp(xx)))

band_l_param[which(band_l_param < 0)] <- 0

x11()
par(mar = c(5, 5, 4, 2) + 0.1)
plot(F.emp,
     xlab = 'x',
     ylab = expression(paste(F[n](x), ', ', F[ML](x), ' & ', F[0](x))),
     main = "Cumulative distribution functions",
     col  = 'cornflowerblue',
     lwd = 1)
curve(pnorm(x, mean = mm.emv, sd = ss.emv), col='purple', lwd=2, add=TRUE)
curve(pnorm(x, mean = mm, sd = ss), col='tomato', lwd=2, add=TRUE)
points(xx, band_u_param, type = 'l', col="forestgreen", lwd=2)
points(xx, band_l_param, type = 'l', col="forestgreen", lwd=2)

legend('topleft',
       legend = c(expression(F[n](x)),
                  expression(F[ML](x)),
                  expression(F[0](x)),
                  "Param. Conf. Band"),
       lwd    = 2,
       col    = c('cornflowerblue' ,'purple', 'tomato', 'forestgreen'),
       bty    = 'n')

# How to build intervals for the estimated parameters

# We know that the variance of hat_mu is sigma^2/n
# and the variance of hat_sigma is sigma^2/(2n)
# And both estimators thends to a Normal distribution

like_level <- exp(-0.5*qchisq(1-alphita,1)) # 0.1465001

# Asymptptical confidence interval for mu
c(mm.emv-qnorm(1-alphita/2)*ss.emv/sqrt(nn),
  mm.emv+qnorm(1-alphita/2)*ss.emv/sqrt(nn)) # 1.196038 2.831823

LI_mu(like_level) # 1.180074 2.847787

# Asymptptical confidence interval for sigma
c(ss.emv-qnorm(1-alphita/2)*ss.emv/sqrt(2*nn),
  ss.emv+qnorm(1-alphita/2)*ss.emv/sqrt(2*nn)) # 2.372418 3.529092

interv_sigma_aux <- function(x){
  logprelver_sigma(x)-log(like_level)
}

uniroot(interv_sigma_aux, c(s1, ss.emv))$root # 2.454887
uniroot(interv_sigma_aux, c(ss.emv, s2))$root # 3.639122

# What happend if we do not know the Fisher Information?
# We can do bootstrap

# Parametric bootstrap intervals by the method of quantiles
B <- 1000
set.seed(111)
muestra_boot <- matrix(rnorm(nn*B, mm.emv, ss.emv), ncol = B)

mu_boot <- apply(muestra_boot, 2, mean)
ss_boot <- apply(muestra_boot, 2, sd)
ss_boot <- sqrt((nn-1)/nn)*ss_boot

quantile(mu_boot, c(alphita/2,1-alphita/2)) # 1.165320 2.811704 
quantile(ss_boot, c(alphita/2,1-alphita/2)) # 2.338606 3.478506 

# Non-parametric bootstrap intervals by the method of quantiles
B <- 1000
set.seed(111)
muestra_boot <- matrix(sample(muestra, nn*B, replace = T), ncol = B)

mu_boot <- apply(muestra_boot, 2, mean)
ss_boot <- apply(muestra_boot, 2, sd)
ss_boot <- sqrt((nn-1)/nn)*ss_boot

quantile(mu_boot, c(alphita/2,1-alphita/2)) # 1.153175 2.789515
quantile(ss_boot, c(alphita/2,1-alphita/2)) # 2.259858 3.493250 