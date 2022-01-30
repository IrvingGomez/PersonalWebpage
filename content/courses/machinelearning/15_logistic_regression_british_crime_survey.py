#########################
##                     ##
## Irving Gomez Mendez ##
##     May 04, 2021    ##
##                     ##
#########################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn import metrics

# Example from:
# Tarling, R. (2009) Statistical modelling for social researchers.
dat = pd.read_spss('BritishCrimeSurvey2000.sav')

#rowlabel	Serial: Full serial Number/Rowlabel

#rubbcomm	How common - litter or rubbish lying around in the immediate area
#vandcomm	How common - vandalism, graffiti or deliberate damage to property
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

#weighta	To be used when analyzing individual-level data from core sample
#weightb	To be used when analyzing household-level data from core sample

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
#         2 = BME = Black or minority ethnicity

#tenurer	Accommodation recoded
#         1 = "Owner"
#         2 = "Rented ocuppied"

##############################################

# Find rows with missing values
dat = dat[~ dat.isnull().any(axis=1)]
dat = dat.reset_index(drop=True)

X = dat[['rubbcomm', 'vandcomm', 'poorhou', 'sex', 'agegrp', 'marst',
       'educat2', 'sc2', 'yrsarea', 'yrsaddr', 'arealive', 'region',
       'numcarr', 'ethnicr', 'tenurer']]

y = dat['victcar']

enc = OneHotEncoder(handle_unknown='ignore')
enc.fit(X)
enc.categories_

X_with_dummies = enc.transform(X)

# Logistic Regression
logreg = LogisticRegression(penalty='none', multi_class='multinomial',
    solver='lbfgs', verbose=2, # output progress
    n_jobs=4) # parallelize over 4 processes)
logreg.fit(X_with_dummies,y)

confusion_matrix = metrics.confusion_matrix(y_true = y,
    y_pred = logreg.predict(X_with_dummies))
accuracy_reg_log = logreg.score(X_with_dummies, y)
accuracy_reg_log

plt.figure(figsize=(10,10))
ax = plt.subplot()
sns.heatmap(confusion_matrix, annot=True,
            linewidths=.5, square = True, cmap='BuPu', fmt='g', ax=ax)
plt.ylabel('Actual label')
plt.xlabel('Predicted label')
ax.yaxis.set_ticklabels(y.unique())
ax.xaxis.set_ticklabels(y.unique())
plt.title('Accuracy Score: {0}'.format(round(accuracy_reg_log,4)))

ttt = np.array(X.iloc[0,])
ttt_trans = enc.transform(ttt[:,None].T)
logreg.predict(ttt_trans)



###
