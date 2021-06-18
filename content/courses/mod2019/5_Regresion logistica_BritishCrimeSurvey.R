# Regresion logistica

# Ejemplo tomado de:
# Tarling, R. (2009) Statistical modelling for social researchers.
# Routledge.

library(foreign)
library(Amelia)

dat = read.spss("BritishCrimeSurvey2000.sav")

names(dat)

# [1] "rowlabel" "rubbcomm" "vandcomm" "poorhou" 
# [5] "sex"      "agegrp"   "marst"    "educat2" 
# [9] "sc2"      "yrsarea"  "yrsaddr"  "wcarstol"
#[13] "wfromcar" "arealive" "region"   "weighta" 
#[17] "weightb"  "victcar"  "agegrpr"  "numcarr" 
#[21] "ethnicr"  "tenurer" 

#rowlabel	Serial: Full serial Number/Rowlabel

#rubbcomm	How common - litter or rubbish lying 
#         around in the immediate area

#vandcomm	How common - vandalism, graffiti or
#         deliberate damage to property

#poorhou	How common - homes in poor conditions

#         1 = "Very commom"
#         2 = "Fairly commom"
#         3 = "Not very commom"
#         4 = "Not at all commom"
#         8 = "Refusal"
#         9 = "Don't know"

#sex	  	Sex (1="Male", 2="Female")

#agegrp		Age (grouped)

#         1 = "16-19"
#         2 = "20-24"
#         3 = "25-34"
#         4 = "35-44"
#         5 = "45-54"
#         6 = "55-64"
#         7 = "65-74"
#         8 = "75-84"
#         9 = "85-over"
#         998 = "Refusal"
#         999 = "Don't know"

#marst	  Marital status

#         1 = "Single, that is, never married"
#         2 = "Married & living with HusbWife"
#         3 = "Married & separated from HusbWife"
#         4 = "Divorced"
#         5 = "Widowed"
#         8 = "Refusal"
#         9 = "Don't know"

#educat2	Highest educational qualification

#         1 = Higher degree/postgraduate qualification
#         2 = First degree (incl. B.Ed); Postgraduate
#         3 = Diplomas in higher education/other H.E.
#         4 = A/AS levels/SCE Higher/Scottish Certific
#         5 = Trade Apprenticeships
#         6 = O level/GCSE grade A-C/SCE Standard/Ordi
#         7 = O level/GCSE grade D-G/SCE Standard/Ordi
#         8 = Other qualifications (incl. overseas)
#         98 = Refusal
#         99 = Don't know

#sc2	    Social class

#         0.0 = Not classified
#         1.0 = Professional 3,4
#         2.0 = Managerial 1,2,13
#         3.1 = Skilled Non-Manual 5,6
#         3.2 = Skilled Manual 8,9,12,14
#         4.0 = Semi skilled 7,10,15
#         5.0 = Unskilled 11
#         6.0 = Armed Forces

#yrsarea	How long lived in this area

#yrsaddr	How long lived at this address

#         1 = less than 12 months
#         2 = 12 months but less than 2 years
#         3 = 2 years but less than 3 years
#         4 = 3 years but less than 5 years
#         5 = 5 years but less than 10 years
#         6 = 10 years but less than 20 years
#         7 = 20 years or longer
#         8 = Refusal
#         9 = Don't know

#wcarstol	Worried about having the car stolen

#wfromcar	Worried about having things stolen from the car

#         1 = "Very worried"
#         2 = "Fairly worried"
#         3 = "Not very worried"
#         4 = "Not at all worried"
#         5 = "(Not applicable)"
#         8 = "Refusal"
#         9 = "Don't know"

#arealive	Respondent's view about this area as place to live in

#         1 = "A very good place tolive"
#         2 = "A fairly good place to live"
#         3 = "Neither good nor bad"
#         4 = "A fairly bad place to live"
#         5 = "A very bad place to live"
#         8 = "Refusal"
#         9 = "Don't know"

#region		Standard Region

#         1 = "North"
#         2 = "Yorks & Humberside"
#         3 = "North West"
#         4 = "East Midlands"
#         5 = "West Midlands"
#         6 = "East Anglia"
#         7 = "Greater London"
#         8 = "South East"
#         9 = "South West"
#         10 = "Wales"
#         11 = "Scotland"

#weighta	To be used when analyzing individual-level data 
#         from core sample
#weightb	To be used when analyzing household-level data
#         from core sample

#victcar	Victim of car crime

#         0 = "Not victim car crime"
#         1 = "Victim car crime"

#agegrpr	Age recoded

#         1 = "16-44"
#         2 = "45-54"
#         3 = "55 - over"

#numcarr	Number of cars recoded

#         1 = 1
#         2 = 2
#         3 = 3
#         4 = 4 or more

#ethnicr	Ethnic group recoded

#         1 = White
#         2 = BME = Black orminority ethnicity

#tenurer	Accommodation recoded

#         1 = "Owner"
#         2 = "Rented ocuppied"

##############################################

datos = cbind(dat$rubbcomm, dat$vandcomm, dat$poorhou,
              dat$sex, dat$agegrp, dat$marst, dat$educat2,
              dat$sc2, dat$yrsarea, dat$yrsaddr,
              dat$wcarstol, dat$wfromcar, dat$arealive,
              dat$region, dat$weighta, dat$weightb,
              dat$victcar, dat$agegrpr, dat$numcarr,
              dat$ethnicr, dat$tenurer)

rownames(datos) = dat$rowlabel
colnames(datos) = names(dat)[-1]

datos = data.frame(datos)

# Primero veamos donde hay datos faltantes
x11()
missmap(data.frame(datos))

# Las variables con datos faltantes son:
# educat2
# wfromcar
# sc2
# numcarr
# tenurer
# ethnicr

# Expliquemos la proba. de que alguien sea victima según
# el número de autos que tiene

# Quitemos los datos perdidos (15081 -> 14971)
sel = !is.na(dat$numcarr)
vic = dat$victcar[sel]
nca = as.numeric(dat$numcarr[sel])

out = glm(vic ~ nca, family=binomial)
summary(out)

#Call:
#glm(formula = vic ~ as.numeric(nca), family = binomial)

#Deviance Residuals: 
#    Min       1Q   Median       3Q      Max  
#-1.0355  -0.7694  -0.6560  -0.6560   1.8122  

#Coefficients:
#                Estimate Std. Error z value Pr(>|z|)
#(Intercept)     -1.78820    0.04693  -38.11   <2e-16
#as.numeric(nca)  0.36123    0.02692   13.42   <2e-16

#(Intercept)     ***
#as.numeric(nca) ***
#---
#Signif. codes:  
#0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

#(Dispersion parameter for binomial family taken to be 1)

#Null deviance: 15995  on 14970  degrees of freedom
#Residual deviance: 15820  on 14969  degrees of freedom
#AIC: 15824

#Number of Fisher Scoring iterations: 4

# Resolviendo ecuaciones de verosimilitud

y  = as.numeric(vic)-1           # 0 not victim  1 victim
n  = length(y)
x1 = nca
X  = cbind(rep(1,n),x1)
b  = c(1,0) # valores iniciales

# Las 4 lineas anteriores son especificas para los datos analizados.
#Las siguientes son generales y se aplican para cualquier otra y y X's
#(incluso X con mas variables predictoras)

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

#           [,1]      [,2]
#histo  1.000000 0.0000000
#b     -2.085673 0.3451822
#b     -1.748043 0.3570311
#b     -1.787689 0.3611024
#b     -1.788204 0.3612336
#b     -1.788204 0.3612336

# Calculo de errores estandar
p = 1/(1+exp(-as.vector(X%*%b)))
W = p*(1-p)
V = solve(t(X*W)%*%X)
es = sqrt(diag(V))

tabla = cbind(b, es)
colnames(tabla) = c("Estimate", "Std. Error")

tabla

#     Estimate Std. Error
#   -1.7882036 0.04692505
#x1  0.3612336 0.02692482

# Calculo de la devianza residual (o simplemente, la devianza)
# -2*loglik

# -2logVero con covariables
aa = -2*sum(y*log(p)+(1-y)*log(1-p)) # 15820.03
out$deviance                         # 15820.03

# -2logVero sin covariables
bb  = -2*(sum(y)*log(mean(y))+(n-sum(y))*log(1-mean(y))) # 15994.91
out =  glm(y ~ 1, family = binomial)
out$deviance                                             # 15994.91

#Prueba global sobre el modelo
G = bb-aa           # 174.88

#p-valor
1-pchisq(G,df=1)    # 0

# Se prefiere el modelo con covariable

# Akaike AIC
aic = 2*2+aa        # 15824.03

xx = seq(1,5,length=200)
X  = cbind(rep(1,200),xx)
p  = 1/(1+exp(-as.vector(X%*%b)))

x11()
plot(xx,p,xlab="Número de vehículos en el hogar",
     ylab="Probabilidad de robo / vandalismo",
     ylim=c(-0.1,1), cex=0.7, lwd=2,
     col="purple", type="l",
     main="Datos: British Crime Survey")

# Proporciones observadas de crímenes por  num de carros
pp = by(y, INDICES = nca, FUN=mean)
points(1:4, pp, pch=19, col="tomato")

# Regresion logistica (un modelo más completo)

# eliminando datos faltantes
sely  = !is.na(dat$victcar)  #15081
selx1 = !is.na(dat$sex)      #15081
selx2 = !is.na(dat$ethnicr)  #15054
selx3 = !is.na(dat$agegrpr)  #15072
selx4 = !is.na(dat$tenurer)  #15045
selx5 = !is.na(dat$numcarr)  #14971
sel   = (selx2)&(selx3)&(selx4)&(selx5)
# 14918 registros completos (del total de 15081)

vic = dat$victcar[sel]
sex = dat$sex[sel]
sex = relevel(sex, ref="Female")
etn = dat$ethnicr[sel]
etn = relevel(etn, ref="BME")
age = dat$agegrpr[sel]
age = relevel(age, ref="55 and over")
own = dat$tenurer[sel]
own = relevel(own, ref="rented")
nca = as.numeric(dat$numcarr[sel])

out = glm(vic~sex+etn+age+own+nca, family=binomial)
summary(out)

#Call:
#glm(formula = vic ~ sex + etn + age + own + nca, family = binomial)

#Deviance Residuals: 
#    Min       1Q   Median       3Q      Max  
#-1.3362  -0.7380  -0.6215  -0.4865   2.0942  

#Coefficients:
#                  Estimate Std. Error z value Pr(>|z|)    
#(Intercept)       -1.83693    0.10772 -17.053  < 2e-16 ***
#sexMale            0.08513    0.04012   2.122   0.0338 *  
#etnwhite          -0.05460    0.08790  -0.621   0.5345    
#age16 to 44        0.79083    0.05005  15.801  < 2e-16 ***
#age45 to 54        0.48245    0.06262   7.704 1.32e-14 ***
#ownowner occupied -0.52826    0.05100 -10.359  < 2e-16 ***
#nca                0.34537    0.02836  12.176  < 2e-16 ***
#---
#Signif. codes:  
#0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

#(Dispersion parameter for binomial family taken to be 1)

#Null deviance: 15926  on 14917  degrees of freedom
#Residual deviance: 15326  on 14911  degrees of freedom
#AIC: 15340

#Number of Fisher Scoring iterations: 4

# Resolviendo ecuaciones de verosimilitud

y   = as.numeric(vic)-1           # 0 not victim  1 victim
n   = length(y)
x1  = as.numeric(sex)-1           # 0 Female      1 Male
x2  = as.numeric(etn)-1           # 0 BME         1 White
x3  = as.numeric(age)
x31 = ifelse(x3==2,1,0)           # 1 if 16 to 44
x32 = ifelse(x3==3,1,0)           # 1 if 45 to 54
x4  = as.numeric(own)-1           # 0 rented      1 owner occupied
x5  = nca
X   = cbind(rep(1,n),x1,x2,x31,x32,x4,x5)
b   = c(1,0,0,0,0,0,0) # valores iniciales

#Las lineas anteriores son especificas para los datos analizados.
#Las siguientes son generales y se aplican para cualquier otra y y X's
#(incluso X con mas variables predictoras)

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

round(histo,4)

#         [,1]   [,2]    [,3]   [,4]   [,5]    [,6]   [,7]
#histo  1.0000 0.0000  0.0000 0.0000 0.0000  0.0000 0.0000
#b     -1.9931 0.0716 -0.0532 0.6288 0.3367 -0.4938 0.3228
#b     -1.8276 0.0861 -0.0536 0.8103 0.5051 -0.5238 0.3423
#b     -1.8369 0.0851 -0.0546 0.7910 0.4827 -0.5281 0.3453
#b     -1.8369 0.0851 -0.0546 0.7908 0.4825 -0.5283 0.3454
#b     -1.8369 0.0851 -0.0546 0.7908 0.4825 -0.5283 0.3454

# Calculo de errores estandar
p = 1/(1+exp(-as.vector(X%*%b)))
W = p*(1-p)
V = solve(t(X*W)%*%X)
es = sqrt(diag(V))

tabla = cbind(b, es)
colnames(tabla) = c("Estimate", "Std. Error")

tabla

#       Estimate Std. Error
#    -1.83693182 0.10771838
#x1   0.08513420 0.04011827
#x2  -0.05459973 0.08789665
#x31  0.79082905 0.05004978
#x32  0.48245408 0.06262310
#x4  -0.52826388 0.05099507
#x5   0.34537121 0.02836436

# Calculo de la devianza residual (o simplemente, la devianza)
# -2*loglik

# -2logVero con covariables
aa = -2*sum(y*log(p)+(1-y)*log(1-p)) # 15325.96
out$deviance                         # 15325.96

# -2logVero sin covariables
bb  = -2*(sum(y)*log(mean(y))+(n-sum(y))*log(1-mean(y))) # 15925.88
out =  glm(y ~ 1, family = binomial)
out$deviance                                             # 15925.88

#Prueba global sobre el modelo
G = bb-aa           # 599.9233

#p-valor
1-pchisq(G,df=6)    # 0

# Se prefiere el modelo con covariables

# Akaike AIC
aic = 2*7+aa        # 15339.96

# Seleccion de modelos
# Modelo 1
out1 = glm(vic~sex+etn+age+own+nca, family=binomial)
aa   = summary(out1)
aa$deviance  # 15325.96     (+2*7 = AIC)
aa$aic       # 15339.96

# eliminamos etnicidad
out2 = glm(vic~sex+age+own+nca, family = binomial)
bb   = summary(out2)
bb$deviance  # 15326.34     (+2*6 = AIC)
bb$aic       # 15338.34
G    = bb$deviance-aa$deviance
1-pchisq(G, 1)  # 0.5359
# No rechazamos que los mdoelos son iguales

# eliminamos sexo
out3 = glm(vic~age+own+nca, family = binomial)
cc   = summary(out3)
cc$deviance  # 15330.87     (+2*5 = AIC)
cc$aic       # 15340.87
G    = cc$deviance-bb$deviance
1-pchisq(G, 1)  # 0.03327
# Conservamos factor sexo en el modelo

#Estadistico G, eliminando 1 variable a la vez es
#equivalente al estadistico de Wald
#(Wald:ver columna de p-valores Pr(>|z|))

#Modelo final (out2)

#Coefficients:
#                  Estimate Std. Error z value Pr(>|z|)    
#(Intercept)       -1.88805    0.06958 -27.136  < 2e-16 ***
#sexMale            0.08539    0.04012   2.129   0.0333 *  
#age16 to 44        0.79385    0.04981  15.938  < 2e-16 ***
#age45 to 54        0.48401    0.06257   7.735 1.03e-14 ***
#ownowner occupied -0.53015    0.05090 -10.415  < 2e-16 ***
#nca                0.34466    0.02834  12.161  < 2e-16 ***


# Se pueden calcular proba. segun los perfiles

perf = expand.grid(
            nca    = c(1,2,3,4),
            own    = c(0,1),
            age2   = c(0,1),
            age1   = c(0,1),
            sex    = c(0,1),
            interc = 1)

perfiles = cbind(perf[,6],perf[,5],
                 perf[,3],perf[,4],
                 perf[,2],perf[,1])

colnames(perfiles) = c("interc", "sex",
                       "age1", "age2",
                       "own", "nca")

Noper = which(perfiles[,3]==1 & perfiles[,4]==1)
perfiles = perfiles[-Noper,]

bg   = bb$coef[,1]
eta  = perfiles%*%bg
prob = 1/(1+exp(-eta))

perfiles = cbind(perfiles, round(prob,2))
colnames(perfiles)[7]="prob"
    
perfiles



