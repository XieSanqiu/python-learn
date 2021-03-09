import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, r2_score, mean_absolute_error, \
    confusion_matrix, f1_score, average_precision_score
import matplotlib.pyplot as plt
import sys
import time
from sklearn.datasets import load_breast_cancer

from iforest.iForest import IsolationTreeEnsemble, find_TPR_threshold

if __name__ == '__main__':
    df = pd.read_csv("mytest.csv")
    X, y = df.drop('diagnosis', axis=1), df['diagnosis']
    it = IsolationTreeEnsemble(sample_size=5, n_trees=1000)
    it.fit(X, improved=True)
    scores = it.anomaly_score(X)
    print(scores)
    x = np.array([[4.3, 0.4, 6.1]])
    anomaly_score = it.anomaly_score(x)
    print(anomaly_score)

