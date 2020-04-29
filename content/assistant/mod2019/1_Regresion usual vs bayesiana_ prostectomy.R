library("lasso2")
data(Prostate)
dat = Prostate

# The data were collected on n=97 men before radical prostatectomy,
# which a major surgical operation that removes the entire prostate
# gland along with some surrounding tissue.

# lcavol  = log cancer volumne, measure in milliliters (cc). The area
#           of cancer was measure from digitized images and multiplied
#           by a thickness to produce a volume.
# lweight = log prostate weight
# age     = age
# lbph    = log of the amount of benign prostatic hyperplasia, a
#           noncancerous enlargement of the prostate gland, as an area in
#           a digitized image and reported in cm2.
# svi     = seminal vesicle invasion, a 0/1 indicator of whether prostate
#           cancer cells hae invaded the vesicle.
# lcp     = log capsular penetration, which represents the level of
#           extension of cancer into the capsule (the fibrous tissue
#           which acts as an outer lining of the prostate gland).
#           Measure as the linear extent of penetration, in cm.
# gleason = Gleason score, a measure of the degree of aggressiveness of
#           the tumor. The Gleason grading system assigns a grade
#           to each of the two largest areas of cancer in the tissue
#           samples with 1 being the least aggressive and 5 the most
#           aggressive; the two grades are then added together to produce
#           the Gleason score.
# pgg45   = percent of Gleason score 4 or 5.
# lpsa    = log prostate specific antigen

# See Hastie et al (2008) The Elements of Stat. Learning (pp. 49)
# and Wakefiled (2013) (pp. 5)

# PSA is a concentration and is measure in ng/ml.
# In Stamey et al (1989), PSA was proposed as a preoperative marker
# to predict  the clinical stage of cancer.
# PSA is a protein produced by the cells of the prostate gland.
# PSA is present in small quantities in the serum of men with healthy
# prostates, but is often elevated in the presence of prostate cancer
# and in other prostate disorders. A blood test to measure PSA is
# considered the most effective test currently available for the early
# detection of prostate cancer, but this effectivesness has also
# been questioned. Rising levels of PSA over time are associated
# with both localized and metastatic prostate cancer.

# dim(dat) # 97 x 9

head(dat)

#       lcavol  lweight age      lbph svi       lcp gleason
# 1 -0.5798185 2.769459  50 -1.386294   0 -1.386294       6
# 2 -0.9942523 3.319626  58 -1.386294   0 -1.386294       6
# 3 -0.5108256 2.691243  74 -1.386294   0 -1.386294       7
# 4 -1.2039728 3.282789  58 -1.386294   0 -1.386294       6
# 5  0.7514161 3.432373  62 -1.386294   0 -1.386294       6
# 6 -1.0498221 3.228826  50 -1.386294   0 -1.386294       6

#   pgg45       lpsa
# 1     0 -0.4307829
# 2     0 -0.1625189
# 3    20 -0.1625189
# 4     0 -0.1625189
# 5     0  0.3715636
# 6     0  0.7654678

corr = cor(dat)
corr

#           lcavol      lweight       age         lbph         svi
#lcavol  1.0000000  0.194128286 0.2249999  0.027349703  0.53884500
#lweight 0.1941283  1.000000000 0.3075286  0.434934636  0.10877851
#age     0.2249999  0.307528614 1.0000000  0.350185896  0.11765804
#lbph    0.0273497  0.434934636 0.3501859  1.000000000 -0.08584324
#svi     0.5388450  0.108778505 0.1176580 -0.085843238  1.00000000
#lcp     0.6753105  0.100237795 0.1276678 -0.006999431  0.67311118
#gleason 0.4324171 -0.001275658 0.2688916  0.077820447  0.32041222
#pgg45   0.4336522  0.050846821 0.2761124  0.078460018  0.45764762
#lpsa    0.7344603  0.354120390 0.1695928  0.179809410  0.56621822

#                 lcp      gleason      pgg45      lpsa
#lcavol   0.675310484  0.432417056 0.43365225 0.7344603
#lweight  0.100237795 -0.001275658 0.05084682 0.3541204
#age      0.127667752  0.268891599 0.27611245 0.1695928
#lbph    -0.006999431  0.077820447 0.07846002 0.1798094
#svi      0.673111185  0.320412221 0.45764762 0.5662182
#lcp      1.000000000  0.514830063 0.63152825 0.5488132
#gleason  0.514830063  1.000000000 0.75190451 0.3689868
#pgg45    0.631528245  0.751904512 1.00000000 0.4223159
#lpsa     0.548813169  0.368986803 0.42231586 1.0000000

library(corrplot)
library(scales)

x11()
corrplot.mixed(corr, lower="ellipse", upper="number")

# Plot histogram in the panel pairs
panel.hist <- function(x, ...) {
  usr <- par("usr"); on.exit(par(usr))
  par(usr = c(usr[1:2], 0, 1.5) )
  h <- hist(x, plot = FALSE)
  breaks <- h$breaks; nB <- length(breaks)
  y <- h$counts; y <- y/max(y)
  rect(breaks[-nB], 0, breaks[-1], y, ...)
}

x11()
pairs(dat, diag.panel = panel.hist, col=alpha("purple", 0.7), upper.panel = NULL, pch=16)

## Making regression
X <- as.matrix(dat[,1:8])
X <- cbind(rep(1, dim(X)[1]), X)
y <- as.matrix(dat[,9])

n <- dim(X)[1]
p <- dim(X)[2]

bets <- solve(t(X)%*%X, t(X)%*%y)

#                [,1]
#         0.669399027
#lcavol   0.587022881
#lweight  0.454460641
#age     -0.019637208
#lbph     0.107054351
#svi      0.766155885
#lcp     -0.105473570
#gleason  0.045135964
#pgg45    0.004525324

SCT <- t(y-mean(y)) %*% (y-mean(y))
SCE <- t(y-X %*% bets) %*% (y-X %*% bets)

R2 <- 1-SCE/SCT  # 0.6547535
R2_adjust <- 1-(SCE/(n-p))/(SCT/(n-1))  # 0.6233674

## unbiased estimator of sigma^2
s2 <- as.numeric(SCE/(n-p))  ## 0.5018537
## Residual standard error:
sqrt(s2)  ## 0.7084164

# Standanrd errors for the coeff.
Errors <- solve(t(X) %*% X)
Std_Errors <- sqrt(s2*diag(Errors))

# Confidence Intervals
lev <- 0.95
alpha <- 1-lev
tt <- qt(1-alpha/2, n-p)

round(cbind(bets - tt*Std_Errors, bets + tt*Std_Errors),3)

#          [,1]  [,2]
#        -1.907 3.246
#lcavol   0.412 0.762
#lweight  0.117 0.792
#age     -0.042 0.003
#lbph    -0.009 0.223
#svi      0.281 1.252
#lcp     -0.286 0.075
#gleason -0.268 0.358
#pgg45   -0.004 0.013

# Hyp. tests

# t statistics with n-p degrees of freedom under H0: bet_j = 0
abs(bets)/Std_Errors

#             [,1]
#        0.5163597
#lcavol  6.6767560
#lweight 2.6731081
#age     1.7575995
#lbph    1.8315753
#svi     3.1360054
#lcp     1.1588785
#gleason 0.2866422
#pgg45   1.0235545

# p-value
2*(1-pt(abs(bets)/Std_Errors, n-p))
#        6.068984e-01
#lcavol  2.110634e-09
#lweight 8.956206e-03
#age     8.229321e-02
#lbph    7.039819e-02
#svi     2.328823e-03
#lcp     2.496408e-01
#gleason 7.750601e-01
#pgg45   3.088513e-01

# F statistic with p and n-p degrees of freedom under H0: all bet = 0
num <- (SCT-SCE)/(p-1)
den <- SCE/(n-p)

ftest <- as.numeric(num/den) # 20.86129
1-pf(ftest, p-1, n-p) # 0

## Prediction Intervals

# punctual predicton
y_hat <- X%*%bets
y_hat <- as.numeric(y_hat)

lev <- 0.95
alpha <- 1-lev
tt <- qt(1-alpha/2, n-p)
aux <- sqrt(1+diag(X %*% Errors %*% t(X)))

P_int <- cbind(y_hat-tt*sqrt(s2)*aux, y_hat+tt*sqrt(s2)*aux)
head(P_int)
#           [,1]     [,2]
#[1,] -0.5877934 2.336606
#[2,] -0.7305662 2.178678
#[3,] -0.9567726 2.044193
#[4,] -0.8772698 2.045678
#[5,]  0.2892399 3.153747
#[6,] -0.6580372 2.272573

## While the confidence intervals
aux2 <- sqrt(diag(X %*% Errors %*% t(X)))

C_int <- cbind(y_hat-tt*sqrt(s2)*aux2, y_hat+tt*sqrt(s2)*aux2)
head(C_int)
#           [,1]      [,2]
#[1,] 0.47937891 1.2694337
#[2,] 0.35807267 1.0900388
#[3,] 0.02460792 1.0628124
#[4,] 0.19187151 0.9765369
#[5,] 1.45811454 1.9848722
#[6,] 0.40089705 1.2136385

mod = lm(lpsa~lcavol+lweight+age+lbph+svi+lcp+gleason+pgg45, dat)

summary(mod)
#Call:
#  lm(formula = lpsa ~ lcavol + lweight + age + lbph + svi + lcp + 
#       gleason + pgg45, data = dat)

#Residuals:
#     Min       1Q   Median       3Q      Max 
#-1.73316 -0.37133 -0.01702  0.41414  1.63811 

#Coefficients:
#             Estimate Std. Error t value Pr(>|t|)    
#(Intercept)  0.669399   1.296381   0.516  0.60690    
#lcavol       0.587023   0.087920   6.677 2.11e-09 ***
#lweight      0.454461   0.170012   2.673  0.00896 ** 
#age         -0.019637   0.011173  -1.758  0.08229 .  
#lbph         0.107054   0.058449   1.832  0.07040 .  
#svi          0.766156   0.244309   3.136  0.00233 ** 
#lcp         -0.105474   0.091013  -1.159  0.24964    
#gleason      0.045136   0.157464   0.287  0.77506    
#pgg45        0.004525   0.004421   1.024  0.30885    
#---
#Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

#Residual standard error: 0.7084 on 88 degrees of freedom
#Multiple R-squared:  0.6548,	Adjusted R-squared:  0.6234 
#F-statistic: 20.86 on 8 and 88 DF,  p-value: < 2.2e-16

round(confint(mod),3)
#             2.5 % 97.5 %
#(Intercept) -1.907  3.246
#lcavol       0.412  0.762
#lweight      0.117  0.792
#age         -0.042  0.003
#lbph        -0.009  0.223
#svi          0.281  1.252
#lcp         -0.286  0.075
#gleason     -0.268  0.358
#pgg45       -0.004  0.013

# punctual prediction
as.numeric(predict(mod, dat))

# Interval prediction
head(predict(mod, dat, interval = "prediction"))
#        fit        lwr      upr
#1 0.8744063 -0.5877934 2.336606
#2 0.7240557 -0.7305662 2.178678
#3 0.5437102 -0.9567726 2.044193
#4 0.5842042 -0.8772698 2.045678
#5 1.7214934  0.2892399 3.153747
#6 0.8072678 -0.6580372 2.272573

# Confidence interval
head(predict(mod, dat, interval = "confidence"))
#        fit        lwr       upr
#1 0.8744063 0.47937891 1.2694337
#2 0.7240557 0.35807267 1.0900388
#3 0.5437102 0.02460792 1.0628124
#4 0.5842042 0.19187151 0.9765369
#5 1.7214934 1.45811454 1.9848722
#6 0.8072678 0.40089705 1.2136385

x11()
plot(y, pch = 20)
points(y_hat, pch = 18, col = "tomato")
polygon(c(1:n,rev(1:n)),
        c(C_int[,2],rev(C_int[,1])),
        col=alpha("tomato", 0.2))
polygon(c(1:n,rev(1:n)),
        c(P_int[,2],rev(P_int[,1])),
        col=alpha("skyblue", 0.2))



# Inferencia bayesiana
library("mvtnorm")
bg  <- mod$coefficients
M   = 10000;                         set.seed(74747)
bp  = matrix(0, M, p)
s2p = (n-p)*s2/rchisq(M, n-p)
for (i in 1:M){
  bp[i,] = rmvnorm(1,mean=bg, sigma=s2p[i]*Errors)
}
qbi = function(x){quantile(x, probs=c(0.025, 0.975))}
int = t(apply(bp, 2, qbi))
nom = c("intercept", colnames(dat[1:8]))
rownames(int) = nom
round(int,3)

# Intervalos de Probabilidad del 95% (bayesiana)

#            2.5% 97.5%
#intercept -1.938 3.226
#lcavol     0.413 0.760
#lweight    0.124 0.803
#age       -0.041 0.003
#lbph      -0.009 0.225
#svi        0.275 1.256
#lcp       -0.284 0.070
#gleason   -0.267 0.362
#pgg45     -0.004 0.013

# Intervalos de Confianza del 95% (frecuentista)

#             2.5 % 97.5 %
#(Intercept) -1.907  3.246
#lcavol       0.412  0.762
#lweight      0.117  0.792
#age         -0.042  0.003
#lbph        -0.009  0.223
#svi          0.281  1.252
#lcp         -0.286  0.075
#gleason     -0.268  0.358
#pgg45       -0.004  0.013