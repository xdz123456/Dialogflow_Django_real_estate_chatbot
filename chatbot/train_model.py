import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import ElasticNet
import joblib

import pandas as pd

report_data = open("model/model_report", "w")


# Dummy classifier(for random guess)
def dummy_classifier(X_train, X_test, y_train, y_test):
    dummy_prior = DummyClassifier(strategy='stratified')
    dummy_prior.fit(X_train, y_train)
    y_prediction = dummy_prior.predict(X_test)
    print("Dummy classifier: \n" + classification_report(y_test, y_prediction, digits=3, zero_division=0), file=report_data)


# Logistic Regression
def lr_classifier(X_train, X_test, y_train, y_test):
    LR = LogisticRegression(solver ='saga', C = 0.6, max_iter=5000)
    LR.fit(X_train, y_train)
    y_prediction = LR.predict(X_test)
    print("Logistic Regression: \n" + classification_report(y_test, y_prediction, digits=3, zero_division=0), file=report_data)
    joblib.dump(LR, 'model/LR.pkl')


# SVC
def svc_classifier(X_train, X_test, y_train, y_test):
    svc = SVC(kernel='rbf')
    svc.fit(X_train, y_train)
    y_prediction = svc.predict(X_test)
    print("SVC: \n" + classification_report(y_test, y_prediction, digits=3, zero_division=0), file=report_data)
    joblib.dump(svc, 'model/SVC.pkl')


# Multi-layer Perceptron(NN)
def neural_network(X_train, X_test, y_train, y_test):
    mlp_clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(20,), max_iter=10000, random_state=1)
    mlp_clf.fit(X_train, y_train)
    y_prediction = mlp_clf.predict(X_test)
    print("MLP: \n" + classification_report(y_test, y_prediction, digits=3, zero_division=0), file= report_data)
    joblib.dump(mlp_clf, 'model/MLP.pkl')


# Linear regression
def linear_regression(X_train, X_test, y_train, y_test):
    l_reg = LinearRegression()
    l_reg.fit(X_train, y_train)
    y_prediction = l_reg.predict(X_test)
    total_gap = 0
    y_test = np.array(y_test)

    for i in range(0, len(y_prediction)):
        gap = abs(y_test[i] - y_prediction[i])/max(y_test[i], y_prediction[i])
        total_gap += gap

    print("Linear regression's Mean Gap: ", total_gap/len(y_prediction)*100, "%", file=report_data)
    joblib.dump(l_reg, 'model/L_Regression.pkl')


# ElasticNet Regression
def elasticNet_regression(X_train, X_test, y_train, y_test):
    elaNet_reg = ElasticNet(l1_ratio = 0.4, alpha=10)
    elaNet_reg.fit(X_train, y_train)
    y_prediction = elaNet_reg.predict(X_test)
    total_gap = 0
    y_test = np.array(y_test)

    for i in range(0, len(y_prediction)):
        gap = abs(y_test[i] - y_prediction[i]) / max(y_test[i], y_prediction[i])
        total_gap += gap

    print("ElasticNet Regression Mean Gap: ", total_gap/len(y_prediction)*100, "%", file=report_data)
    joblib.dump(elaNet_reg, 'model/ElaNet_Regression.pkl')


total_data = pd.read_csv("data/rightmove_london_labeled.csv")

X = pd.DataFrame(total_data, columns=["number_bedrooms", "lat", "lng"])
y_clf = total_data["label"]
y_reg = total_data["price"]

type_meta = total_data["type"].value_counts().index.tolist()
postcode_meta = total_data["postcode"].value_counts().index.tolist()

type_encoder = preprocessing.LabelEncoder()
postcode_encoder = preprocessing.LabelEncoder()

type_encoder.fit(type_meta)
postcode_encoder.fit(postcode_meta)

type_labeled = type_encoder.transform(total_data["type"])
postcode_labeled = postcode_encoder.transform(total_data['postcode'])

X["type_labeled"] = type_labeled
X["postcode_labeled"] = postcode_labeled


X_train_clf, X_test_clf, y_train_clf, y_test_clf = train_test_split(X, y_clf, test_size=0.15, random_state=42)
X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X, y_reg, test_size=0.15, random_state=40)


dummy_classifier(X_train_clf, X_test_clf, y_train_clf, y_test_clf)

# Regression
linear_regression(X_train_reg, X_test_reg, y_train_reg, y_test_reg)
elasticNet_regression(X_train_reg, X_test_reg, y_train_reg, y_test_reg)

# Classifier
svc_classifier(X_train_clf, X_test_clf, y_train_clf, y_test_clf)
lr_classifier(X_train_clf, X_test_clf, y_train_clf, y_test_clf)
neural_network(X_train_clf, X_test_clf, y_train_clf, y_test_clf)

report_data.close()

