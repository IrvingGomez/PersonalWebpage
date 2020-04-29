## Regresion Poisson

library(acp)
data(polio)
dat = polio

# Time series of Polio incidences in U.S.A. from 1970 to 1983.

dim(dat) #168x1

Month = seq(0,167)
Count = dat$polio

x11()
plot(Month, Count, pch=16, xlab="Mes", ylab="Número de casos",
     main="Casos de Polio")

x11()
plot(Month, Count, type="l", xlab="Mes", ylab="Número de casos",
     main="Casos de Polio")

aa   = matrix(Count,12,14)
med  = apply(aa,1,mean)
vari = apply(aa,1,var)

x11()
plot(med, vari, pch=16, xlab="Promedio mensual de casos de Polio",
     ylab="Varianza", main="Relación Media X Varianza")
curve(1*x,lwd=1.5,col="blue",add=T)

x11()
plot(1:12, med, pch=16, xlab="Mes",
     ylab="Promedio mensual de casos de Polio",
     main="Casos de Polio por Mes")

# Ajuste del modelo Poisson y Cuasi-Poisson

MM = rep(seq(1:12),14)

# GLM Poisson
out1 = glm(Count~MM, family=poisson)
summary(out1)

#Coefficients:
#            Estimate Std. Error z value Pr(>|z|)    
#(Intercept) -0.60065    0.17483  -3.436 0.000591 ***
#MM           0.12304    0.02041   6.028 1.66e-09 ***
#---
#Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

#(Dispersion parameter for poisson family taken to be 1)

#Null deviance: 343.00  on 167  degrees of freedom
#Residual deviance: 304.69  on 166  degrees of freedom
#AIC: 565.73

#Number of Fisher Scoring iterations: 5

x11()
plot(MM[1:12], med,
     xlab="Número de casos registrados",
     ylab="Número de casos predichos",
     pch="o", font=2,
     main="Relación de predichos X registrados",
     col="purple")
points(MM[1:12], out1$fitted.values[1:12],pch="p",col="tomato", font=2)

head(residuals(out1))

# Cuasi-Poisson
out2 = glm(Count~MM, family=quasipoisson)
summary(out2)

#Coefficients:
#            Estimate Std. Error t value Pr(>|t|)    
#(Intercept) -0.60065    0.26026  -2.308   0.0222 *  
#MM           0.12304    0.03039   4.049 7.87e-05 ***
#---
#Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

#(Dispersion parameter for quasipoisson family taken to be 2.215995)

#Null deviance: 343.00  on 167  degrees of freedom
#Residual deviance: 304.69  on 166  degrees of freedom
#AIC: NA

#Number of Fisher Scoring iterations: 5

x11()
plot(MM[1:12], med,
     xlab="Número de casos registrados",
     ylab="Número de casos predichos",
     pch="o", font=2,
     main="Relación de predichos X registrados, QuasiPoisson",
     col="purple")
points(MM[1:12], out2$fitted[1:12],pch="p",col="tomato", font=2)
