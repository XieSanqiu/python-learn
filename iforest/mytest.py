import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error, \
    confusion_matrix, f1_score, average_precision_score
import matplotlib.pyplot as plt
import sys
import time
from sklearn.datasets import load_breast_cancer

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
    x = np.array([[4.3, 0.4, 6.1]])
    anomaly_score = np.array(it.anomaly_score(x))
    detect_attr_weight = it.attr_weight
    print(anomaly_score)
    print('attr_weight', it.attr_weight)
    print(detect_attr_weight / train_attr_weight)
