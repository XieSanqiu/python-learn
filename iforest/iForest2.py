import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from lolviz import *
from multiprocessing import Pool

# Follows algo from https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf

'''
S(x, n) = 2exp(-(h(x)/c(n)))   
c(n) = 2 * H(n-1) - (2*(n-1)/n)
H(k) = ln(k) + euler_gamma(欧拉常数：0.5772156649015329)
'''

class CFactor:
    @classmethod
    def compute(cls, n_of_elements):
        n = n_of_elements
        if n > 2:
            return 2 * (np.log(n - 1) + np.euler_gamma) - (2 * (n - 1) / n)
        elif n == 2:
            return 1
        else:
            return 0


class IsolationTreeEnsemble:
    def __init__(self, sample_size, n_trees=10):
        self.sample_size = sample_size
        self.n_trees = n_trees
        self.trees = []
        self.height_limit = np.ceil(np.log2(self.sample_size))
        self.attr_weight = []

    #得到一棵树
    def make_tree(self, i):
        # 随机从[0, X.shape[0]) 中不重复的抽取 sample_size 个值，组成 sample_size 个随机实例
        X_sample = self.X[np.random.choice(self.X.shape[0], self.sample_size, replace=False)]
        return IsolationTree(X_sample, self.height_limit, self.good_features, self.improved)

    #将训练数据填充，得到孤立森林
    def fit(self, X:np.ndarray, improved=False):
        """
        Given a 2D matrix of observations, create an ensemble of IsolationTree
        objects and store them in a list: self.trees.  Convert XFrames to
        ndarray objects.
        """
        if isinstance(X, pd.DataFrame): X = X.values
        self.X = X
        self.improved = improved

        if self.improved:
            #计算沿 axis=0 轴的中位数，axis=0表示第一维 np.array([[10, 7, 4], [3, 2, 1]]) np.median(a, axis=0) = array([6.5, 4.5, 2.5])
            median_c = np.median(self.X, axis=0) #对每一列求中位数
            mean_c = np.mean(self.X, axis=0) #对每一列求均值
            # std = np.sqrt(((a - np.mean(a)) ** 2).sum() / a.size)  标准差表示自平均值分散开的程度，越大表示分散的越狠
            std_c = np.std(self.X, axis=0) #对每一列求标准差
            # result = 100 * (abs(median_c - mean_c) / std_c)
            median_c_list = median_c.tolist()
            mean_c_list = mean_c.tolist()
            std_c_list = std_c.tolist()
            result_list = []
            for i in range(self.X.shape[1]):
                if std_c_list[i] == 0:
                    r = 0
                else:
                    r = 100 * (abs(median_c_list[i] - mean_c_list[i]) / std_c_list[i])
                result_list.append(r)
            result = np.array(result_list)

            #good_features计算方法2，离散值越大，概率越大，包含所有特征
            gof = []
            ind = np.argsort(result)
            # print('ind', ind)
            for i in range(1, len(result)+1):
                for j in range(i):
                    gof.append(ind[i-1])
            # print('result', result)
            # print('gof', gof)

            self.good_features = np.array(gof)

            with Pool(5) as p:
                self.trees = p.map(self.make_tree, range(self.n_trees))  #创建 n_trees 颗树，传入的是array，返回的也是array

        else:
            for i in range(self.n_trees):
                X_sample = X[np.random.choice(X.shape[0], self.sample_size, replace=False)]
                self.trees.append(IsolationTree(X_sample, self.height_limit))

        return self

    def path_length(self, X:np.ndarray) -> np.ndarray:
        """
        Given a 2D matrix of observations, X, compute the average path length
        for each observation in X.  Compute the path length for x_i using every
        tree in self.trees then compute the average for each x_i.  Return an
        ndarray of shape (len(X),1).
        """
        if isinstance(X, pd.DataFrame): X = X.values

        length = []

        for x_i in X:  #计算每一个实例在森林上的
            x_len = []
            # print('x_i', x_i)
            for tree in self.trees:
                # print('tree', tree.root.num, tree.root.pre_attr)
                l, split_attr, num = tree.root.path_length(x_i)
                x_len.append(l)
                if split_attr != -1:
                    self.attr_weight[split_attr] += (1/num)
            avg_len = np.array(x_len).mean()
            # print('x_len', x_len)
            length.append(avg_len)
        return np.array(length)

    #计算 X 中每一个实例的异常分数
    def anomaly_score(self, X:np.ndarray) -> np.ndarray:
        """
        Given a 2D matrix of observations, X, compute the anomaly score
        for each x_i observation, returning an ndarray of them.
        """
        self.attr_weight = [0] * X.shape[1]
        avg_pathlen = self.path_length(X)
        c = CFactor.compute(self.sample_size)
        anom_score = np.exp2(-avg_pathlen/c)

        return anom_score

    def clear_attr_weight(self):
        self.attr_weight = []

    def predict_from_anomaly_scores(self, scores:np.ndarray, threshold:float) -> np.ndarray:
        """
        Given an array of scores and a score threshold, return an array of
        the predictions: 1 for any score >= the threshold and 0 otherwise.
        """
        return (scores>=threshold).astype(int)

    def predict(self, X:np.ndarray, threshold:float) -> np.ndarray:
        "A shorthand for calling anomaly_score() and predict_from_anomaly_scores()."
        return self.predict_from_anomaly_score(self, self.anomaly_score(self, X), threshold)


class Node:
    def __init__(self, left=None, right=None, split_attr=None, split_point=None, c_factor=None):
        self.left = left
        self.right = right
        self.split_attr = split_attr
        self.split_point = split_point
        self.c_factor = c_factor
        self.num = 0
        self.pre_attr = -1

    def path_length(self, x, current_height=0): #用于计算一个实例 x 在一颗树上的路径长度
        if self.left == None and self.right == None:
            return current_height + self.c_factor, self.pre_attr, self.num
            # return current_height

        if x[self.split_attr] < self.split_point:
            return self.left.path_length(x, current_height + 1)
        else:
            return self.right.path_length(x, current_height + 1)


class IsolationTree:
    def __init__(self, X:np.ndarray, height_limit, good_features=[], improved=False):
        self.height_limit = height_limit
        self.n_nodes = 0
        self.split_attr = None
        self.split_point = None
        self.good_features = good_features
        self.improved = improved
        self.root = self.fit(X, 0)

    #c_factor：本棵树的c(n)
    def fit(self, X:np.ndarray, current_height):
        if ((current_height >= self.height_limit) or (len(X) <= 1)):
            c_factor = CFactor.compute(X.shape[0])  #X.shape[0] X行数
            return Node(None, None, -1, None, c_factor)

        self.n_nodes += 1
        node = Node()
        node.num = X.shape[0]

        if self.improved:
            tooBalanced = True

            while tooBalanced: #这一步的目的就是找哪个特征能够很大的区分数据
                q = np.random.choice(self.good_features, replace=False) #随机选择一个特征

                X_column = X[:, q]  #第 q 个特征列
                minv = X_column.min()
                maxv = X_column.max()

                if minv == maxv: #该个节点不再往下分
                    c_factor = CFactor.compute(X.shape[0])
                    r_node = Node(None, None, -1, None, c_factor)
                    r_node.num = X.shape[0]
                    r_node.pre_attr = q
                    return r_node

                p = float(np.random.uniform(minv, maxv)) #随机从[minv, maxv)中取值

                X_l = X[X_column < p, :] #第 q 个特征小于 p 的行
                X_r = X[X_column >= p, :] #第 q 个特征大于 p 的行

                node.split_attr = q
                node.split_point = p

                total = X.shape[0]
                ls = X_l.shape[0]
                rs = X_r.shape[0]

                diff = float(abs(ls - rs)/total)

                if diff >= 0.25 or total == 2: #总共只有两个实例或者q特征区分度很大停止循环
                    tooBalanced = False

        else:
            node.split_attr = np.random.randint(0, X.shape[1]) #随机选择第几个属性

            X_column = X[:, node.split_attr] #选择属性的属性值列
            minv = X_column.min()
            maxv = X_column.max()

            if minv == maxv: #找到的特征发现不能分了
                c_factor = CFactor.compute(X.shape[0])
                r_node = Node(None, None, -1, None, c_factor)
                r_node.num = X.shape[0]
                r_node.pre_attr = node.split_attr
                return r_node

            node.split_point = float(np.random.uniform(minv, maxv))

            X_l = X[X_column < node.split_point, :]
            X_r = X[X_column >= node.split_point, :]

        node.left = self.fit(X_l, current_height + 1)
        node.left.pre_attr = node.split_attr
        node.left.num = X_l.shape[0]
        node.right = self.fit(X_r, current_height + 1)
        node.right.pre_attr = node.split_attr
        node.right.num = X_r.shape[0]

        return node