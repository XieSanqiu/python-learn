import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error, \
    confusion_matrix, f1_score, average_precision_score
import matplotlib.pyplot as plt
import sys
import time
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import IsolationForest

from iforest.iForest2 import IsolationTreeEnsemble


if __name__ == '__main__':
    df = pd.read_csv("mytest.csv")
    # df = pd.read_csv("cancer.csv")
    X, y = df.drop('diagnosis', axis=1), df['diagnosis']
    it = IsolationTreeEnsemble(sample_size=5, n_trees=1000)
    it.fit(X, improved=True)
    scores = it.anomaly_score(X)
    print('scores', scores)
    train_attr_weight = np.array(it.attr_weight)
    print('attr_weight', it.attr_weight)
    attr_weight = np.array(it.attr_weight)
    print(np.argsort(-attr_weight))

    it.clear_attr_weight()

    x = np.array([[4.3, 0.4, 6.1, 0, 0]])
    anomaly_score = np.array(it.anomaly_score(x))
    detect_attr_weight = it.attr_weight
    print(anomaly_score)
    print('attr_weight', it.attr_weight)
    print(detect_attr_weight / train_attr_weight)

    X_train = X
    rng = np.random.RandomState(42)  # 随机数生成器
    clf = IsolationForest(max_samples=5, random_state=rng)
    clf.fit(X_train)
    y_pred_train = clf.predict(X_train)
    print(y_pred_train)
    X_train_scores = clf.decision_function(X_train)
    print('X_train_scores', X_train_scores)
    X_test = np.array([[4.3, 0.4, 6.1, 0, 0]])
    y_pred_test = clf.predict(X_test)
    print(y_pred_test)
    X_test_scores = clf.decision_function(X_test)
    print('X_test_scores', X_test_scores)


