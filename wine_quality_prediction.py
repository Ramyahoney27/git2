# -*- coding: utf-8 -*-
"""Wine Quality prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q3L6sIYU-LnlUk6L0TW8Mai45xf7OWt8
"""

#import libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from math import pi
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

#loading the data
df = pd.read_csv("/content/archive.zip")

df.sample(5)

# check for null values
df.isna().sum()

df['fixed acidity'].fillna(df['fixed acidity'].median(), inplace=True)
df['fixed acidity'].isna().sum()

df['volatile acidity'].fillna(df['volatile acidity'].mean(), inplace=True)
df['volatile acidity'].isna().sum()

df['citric acid'].fillna(df['citric acid'].mean(), inplace=True)
df['citric acid'].isna().sum()

df['residual sugar'].fillna(df['residual sugar'].mean(), inplace=True)
df['residual sugar'].isna().sum()

df['chlorides'].fillna(df['chlorides'].median(), inplace=True)
df['chlorides'].isna().sum()

df['pH'].fillna(df['pH'].mean(), inplace=True)
df['pH'].isna().sum()

df['sulphates'].fillna(df['sulphates'].median(), inplace=True)
df['sulphates'].isna().sum()

df.isna().sum()

"""# New Section"""

df['quality'].min()
df['quality'].value_counts()

df['quality']=df['quality'].map({3:'low', 4:'low', 5:'medium', 6:'medium', 7:'medium', 8:'high', 9:'high'})

df['quality']=df['quality'].map({'low':0,'medium':1,'high':2})

df.sample(5)

sn.set()
plt.figure(figsize=(30,15))
sn.boxplot(data=df)
plt.show()

fig, ax =plt.subplots(1,3)
plt.subplots_adjust(right=2.5, top=1.5)
sn.boxplot(df['residual sugar'], df['type'], ax=ax[0])
sn.boxplot(df['free sulfur dioxide'], df['type'], ax=ax[1])
sn.boxplot(df['total sulfur dioxide'], df['type'], ax=ax[2])
plt.show()

#Removing outliers in residual sugar
lower = df['residual sugar'].mean()-3*df['residual sugar'].std()
upper = df['residual sugar'].mean()+3*df['residual sugar'].std()
df = df[(df['residual sugar']>lower) & (df['residual sugar']<upper)]

#Removing outliers in free sulfur dioxide
lower = df['free sulfur dioxide'].mean()-3*df['free sulfur dioxide'].std()
upper = df['free sulfur dioxide'].mean()+3*df['free sulfur dioxide'].std()
df = df[(df['free sulfur dioxide']>lower) & (df['free sulfur dioxide']<upper)]

#Removing outliers in total sulfur dioxide
lower = df['total sulfur dioxide'].mean()-3*df['total sulfur dioxide'].std()
upper = df['total sulfur dioxide'].mean()+3*df['total sulfur dioxide'].std()
df = df[(df['total sulfur dioxide']>lower) & (df['total sulfur dioxide']<upper)]

dummies = pd.get_dummies(df['type'], drop_first=True)
df = pd.concat([df, dummies], axis=1)
df.drop('type', axis=1, inplace=True)

#Checking relationship between features
cor=df.corr()
plt.figure(figsize=(20,10))
sn.heatmap(cor,xticklabels=cor.columns,yticklabels=cor.columns,annot=True)
cor

X = df.loc[:,df.columns!='quality']
y = df['quality']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20, random_state=0)

from sklearn.ensemble import RandomForestClassifier
rfc=RandomForestClassifier()
print(rfc.get_params())

# Fit the model
rfc.fit(X_train,y_train)

from sklearn.model_selection import RandomizedSearchCV

n_estimators = [int(x) for x in np.linspace(start=90, stop=200, num=12)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(start=10, stop=110, num=11)]
max_depth.append(None)
min_samples_split=[2, 5, 10]
min_samples_leaf=[1, 2, 4]
bootstrap=[True, False]

random_search_grid = {'n_estimators': n_estimators,
                      'max_features': max_features,
                      'max_depth': max_depth,
                      'min_samples_split': min_samples_split,
                      'min_samples_leaf': min_samples_leaf,
                      'bootstrap': bootstrap}
print(random_search_grid)

rfc=RandomForestClassifier()
rf_random = RandomizedSearchCV(estimator=rfc, param_distributions = random_search_grid, n_iter=100,
                          cv=3, verbose=2, random_state=0, n_jobs=-1)

rf_random.fit(X_train, y_train)

rf_random.best_params_

rfc = RandomForestClassifier(n_estimators=90, min_samples_split=2, min_samples_leaf=1,max_features='auto', max_depth=50, bootstrap=True, random_state = 42)

rfc.fit(X_train,y_train)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
classify(model, X, y)

print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print('\nClassification Report:\n', classification_report(y_test, y_pred))