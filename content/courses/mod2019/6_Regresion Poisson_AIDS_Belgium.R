# El siguiente ejemplo considera el número de casos nuevos de SIDA
# en Bélgica (datos de los 80’s).
# Supondremos que es razonable considerar el modelo Poisson
# (Ver libro Wood, S.N. (2006) Generalized Additive Models).

y<- c(12,14,33,50,67,74,123,141,165,204,253,246,240)
t<-1:13

x11()
plot(t+1980,y,xlab="Year",ylab="New AIDS cases",ylim=c(0,280))

m0 = glm(y~t,poisson)
m0

#Call:  glm(formula = y ~ t, family = poisson)

#Coefficients:
# (Intercept)            t  
#      3.1406       0.2021  

#Degrees of Freedom: 12 Total (i.e. Null);  11 Residual
#Null Deviance:	     872.2 
#Residual Deviance: 80.69 	AIC: 166.4

x11()
par(mfrow=c(2,2))
plot(m0, which = 1:4)

x11()
plot(t+1980, y, xlab="Year", ylab="New AIDS cases", ylim=c(0,280),
     pch="o", font=2,
     main="Relación de predichos X registrados",
     col="purple")
points(t+1980, m0$fitted, pch="p", col="tomato", font=2)

#Puede servir agregar un término cuadrático en t, para obtener
m1 <- glm(y~t+I(t^2),poisson)
summary(m1)

x11()
par(mfrow=c(2,2))
plot(m1, which = 1:4)

#Para decidir con cuál de los dos modelos elegir, se puede hacer un anova
anova(m0,m1,test="Chisq")

#Analysis of Deviance Table
#Model 1: y ~ t
#Model 2: y ~ t + I(t^2)
#Resid. Df Resid. Dev Df Deviance  Pr(>Chi)    
#1        11     80.686                          
#2        10      9.240  1   71.446 < 2.2e-16 ***
#---
#Signif. codes:  
#0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

x11()
plot(t+1980, y, xlab="Year", ylab="New AIDS cases", ylim=c(0,280),
     pch="o", font=2,
     main="Relación de predichos X registrados",
     col="purple")
points(t+1980, m1$fitted, pch="p", col="tomato", font=2)

alpha=0.15
int1 <- qpois(alpha/2, m1$fitted)
int2 <- qpois(1-alpha/2, m1$fitted)

x11()
plot(t+1980, y, xlab="Year", ylab="New AIDS cases", ylim=c(0,280),
     pch="o", font=2,
     main="Relación de predichos X registrados",
     col="purple")
points(t+1980, m1$fitted, pch="p", col="tomato", font=2)
lines(t+1980, int1, lty=2, col="tomato")
lines(t+1980, int2, lty=2, col="tomato")
