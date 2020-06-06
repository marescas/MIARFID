from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pandas as pd
import pickle
if __name__ == '__main__':
    print("cargando dataset....")
    ingles = pd.read_pickle("english.pkl")
    ingles["tweetsClean"] = [" #finTweet# ".join(tweets) for tweets in list(ingles.tweets)]
    print("Listo....")
    print("******************************************************")
    print("Probando Logistic regression")
    print("******************************************************")

    pipe = Pipeline([
        ("tfidf",TfidfVectorizer()),
        ("svm",LogisticRegression())
    ])
    
    parameters = {"tfidf__ngram_range" : [(1,2),(1,3),(2,3),(3,4),(3,5),(3,6),(4,5),(4,6)]
                  ,"tfidf__max_df":[0.2,0.3,0.4,0.5],
                  "tfidf__min_df":[2,3,4],
                  "tfidf__analyzer":["char_wb"],
                  #'svm__kernel':('linear', 'rbf'),
                  'svm__C':[10,100,1000,10000]}
    clf = GridSearchCV(pipe, parameters,cv=10,n_jobs=-1,verbose=2)
    clf.fit(ingles.tweetsClean, ingles.label)
    print("******************************************************")
    print("mejor clasificador: ",clf.best_params_)
    print("mejor score: ", clf.best_score_)

    print("******************************************************")
    print("Probando SVM")
    print("******************************************************")
    pipe = Pipeline([
        ("tfidf",TfidfVectorizer()),
        ("svm",svm.SVC())
    ])

    parameters = {"tfidf__ngram_range" : [(3,4),(3,5),(3,6),(4,5),(4,6)]
                  ,"tfidf__max_df":[0.2,0.3,0.4,0.5],
                  "tfidf__min_df":[2,3,4],
                  "tfidf__analyzer":["char_wb"],
                  'svm__kernel':['rbf'],
                  'svm__C':[10,100,1000,10000]}
    clf = GridSearchCV(pipe, parameters,cv=10,n_jobs=-1,verbose=1)
    clf.fit(ingles.tweetsClean, ingles.label)
    print("******************************************************")
    print("mejor clasificador: ",clf.best_params_)
    print("mejor score: ", clf.best_score_)