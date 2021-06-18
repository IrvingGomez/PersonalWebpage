#########################
##                     ##
## Irving Gomez Mendez ##
##     May 06, 2021    ##
##                     ##
#########################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.manifold import MDS

def levenshtein(str1, str2):
  d = dict()
  for i in range(len(str1)+1):
     d[i] = dict()
     d[i][0] = i
  for i in range(len(str2)+1):
     d[0][i] = i
  for i in range(1, len(str1)+1):
     for j in range(1, len(str2)+1):
        d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
  return d[len(str1)][len(str2)]

def disimilar_levenshtein(str1, str2):
    return(levenshtein(str2, str1)/(len(str1) + len(str2)))

disimilar_vect = np.vectorize(disimilar_levenshtein)

# Data taken from Batagelj, V., Kerzic, D., & Pisanski, T. (1992) Automatic Clustering of Languages.
# The data correspond to 16 words in 65 languages
# I added the linguistic family for each language
dat = pd.read_csv('words_languages.csv')
dat

dat[['Language', 'Family']].groupby('Family').agg('count')

# Let's make logistic regression using germanic and romance languages
# Let's use eseranto words as the basis for the levenshtein distance
dat_simpl = dat[dat['Family'].isin(['Germanic','Romance','Esperanto'])]

dat_simpl

y = dat_simpl['Family'].loc[dat_simpl['Family'].isin(['Germanic','Romance'])]
y = y.replace(['Romance', 'Germanic'], [0,1])
y = y.reset_index(drop=True)

y

# 0 is Romance
# 1 is Germanic

base_words = dat_simpl[dat_simpl['Language'] == 'Esperanto'].filter(regex=('w.'))

base_words

X = dat_simpl.filter(regex=('w.'))
X = pd.DataFrame(disimilar_vect(X, base_words))
X = X.drop(4,axis=0).reset_index(drop=True)

X

# Let's take out Spanish and English from the training data set
dat_simpl['Language'].loc[dat_simpl['Family'].isin(['Germanic','Romance'])].reset_index(drop=True)

# Creation of traning and testing data set
X_train = X.drop([3,15], axis=0).reset_index(drop=True)
X_test = X.iloc[[3,15]].reset_index(drop=True)

y_train = y.drop([3,15]).reset_index(drop=True)
y_test = y[[3,15]].reset_index(drop=True)

# Using LogisticRegression
logreg = LogisticRegression(penalty='none', fit_intercept=False)
logreg.fit(X_train,y_train)

logreg.predict(X_train)
np.array(y_train)

logreg.predict(X_test)
np.array(y_test)

## Let's plot using MDS
mds_model = MDS(n_components=2, random_state=111)
X_mds = mds_model.fit_transform(np.vstack([X_train, X_test]))

y_mds = y_train.replace([0,1], ['Romance', 'Germanic'])
y_mds = np.concatenate([y_mds, ['Testing', 'Testing']])

plt.figure(figsize=(10,10))
sns.scatterplot(x=X_mds[:,0], y=X_mds[:,1], hue=y_mds, s=100)

###
