import pandas as pd
from sklearn import preprocessing
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import numpy as np

X_train = pd.read_csv("train_isot.csv", ",", usecols=['text', 'label'])
y_train = X_train['label'].values.flatten()
X_train = X_train['text'].values.flatten()
print("Read")

stopwords = set(ENGLISH_STOP_WORDS)


vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.73, stop_words=stopwords)
X_train = vectorizer.fit_transform(X_train)
print("Vectorized.")

#SVM parameters
# parameters = [  
#   {'C': [ 10], 'kernel': ['linear']},
#   {'C': [1, 10, 100], 'gamma': [10], 'kernel': ['rbf']},
#  ]



# knn_vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.56, stop_words=stopwords)
# X_train = knn_vectorizer.fit_transform(X_train)
# print("Vectorized.")

#KNN parameters
# parameters = [
#     {'n_neighbors' : [2, 4],  'metric' : ['euclidean', 'manhattan']},
#     {'n_neighbors' : [2, 4], 'metric' : ['minkowski'], 'p':[6] }
# ]

# LR_vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.65, stop_words=stopwords)
# X_train = LR_vectorizer.fit_transform(X_train)
# print("Vectorized.")

#Logistic Regression parameters
# parameters = [
#     {'C': [10, 100], 'penalty' : ['l2', 'l1'], 'solver' : [ 'saga'] },
#     {'C': [10, 100], 'penalty' : ['l2'], 'solver' : ['lbfgs'] }     
# ]

# DT_vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.25, stop_words=stopwords)
# X_train = DT_vectorizer.fit_transform(X_train)
# print("Vectorized.")

#Decision Trees parameters
# parameters = [
#     { 'criterion' : ['entropy', 'gini'], 'min_samples_split' : range(10,101,10),'max_depth': [10] }
# ]

# RF_vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.21, stop_words=stopwords)
# X_train = RF_vectorizer.fit_transform(X_train)
# print("Vectorized.")

#Random forest parameters
parameters = [
    { 'n_estimators' : range(300, 501, 50), 'min_samples_split': range(2, 13), 'max_depth' : range(20, 24),  'criterion' : ['entropy', 'gini'] }   
]                                                                             



# vectorizer = TfidfVectorizer(sublinear_tf = True, max_df = 0.5, stop_words=stopwords)
# X_train = vectorizer.fit_transform(X_train)
# print("Vectorized.")

svd = TruncatedSVD(n_components=200,algorithm='arpack', random_state=42)
X_train = svd.fit_transform(X_train)
print("SVD performed.")


scores = [ 'f1']

for score in scores:

    print("# Tuning hyper-parameters for %s" % score)
    print()
    
    #clf = SVC(random_state=42)
    #clf = KNeighborsClassifier(weights='distance')
    #clf = LogisticRegression(random_state=42, max_iter=1000)
    #clf = DecisionTreeClassifier(random_state=42)
    clf = RandomForestClassifier(random_state=42)
    clf = GridSearchCV(clf, parameters, scoring='%s' % score, cv=5, return_train_score=True, verbose=10000, n_jobs=-1)
    
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)

dict_res = clf.cv_results_
df = pd.DataFrame()
for key in dict_res:
    df[key] = list(dict_res[key])

df.to_csv("gridsearch_RF.csv", sep=',',index = False ,header = True)