'''
决策树训练模块
'''
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
import pydotplus


def pc_convert(pc):
    it = {'service':0, 'application':1, 'user':2}
    pc = str(pc, encoding="utf-8")
    return it[pc]

def get_decision_tree(host_ip):
    play_feature_E = ['user_type', 'max_cpu', 'avg_cpu', 'max_memory', 'avg_memory', 'read_count', 'read_byte', 'write_count',
                      'write_byte', 'sockets_num', 'files_num', 'threads_num', 'collect_rate', 'activity_rate']
    play_class = ['service', 'application', 'user']

    train_file = host_ip + '-pdt.txt'

    # 1、读入数据，并将原始数据中的数据转换为数字形式
    data = np.loadtxt(train_file, delimiter=", ", dtype=float, converters={14: pc_convert})
    x, y = np.split(data, (14,), axis=1)

    # 2、拆分训练数据与测试数据，为了进行交叉验证
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3,random_state=2)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # 3、使用信息熵作为划分标准，对决策树进行训练
    clf = tree.DecisionTreeClassifier(criterion='gini')
    print(clf)
    clf.fit(x_train, y_train)

    # 4、把决策树结构写入文件
    # file_name = host_ip+ '-proc_class'
    # dot_data = tree.export_graphviz(clf, out_file=None, feature_names=play_feature_E, class_names=play_class,
    #                                 filled=True, rounded=True, special_characters=True)
    # graph = pydotplus.graph_from_dot_data(dot_data)
    # graph.write_pdf(file_name +'.pdf')

    # 5、使用训练数据预测，预测结果完全正确
    answer = clf.predict(x_train)
    y_train = y_train.reshape(-1)
    print(answer)
    print(y_train)
    print(np.mean(answer == y_train))

    # 6、对测试数据进行预测，准确度较低，说明过拟合
    answer = clf.predict(x_test)
    y_test = y_test.reshape(-1)
    print(answer)
    print(y_test)
    print(np.mean(answer == y_test))


if __name__ == '__main__':
    # host_ip = '211.65.197.175'
    # host_ip = '211.65.193.23'
    # host_ip = '211.65.197.233'
    host_ip = '211.65'
    get_decision_tree(host_ip)