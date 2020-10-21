'''
决策树训练模块
'''
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
import pydotplus


def pc_convert(pc):
    it = {'kernel':0, 'service':1, 'application':2, 'interactive':3,  'user':4}
    pc = str(pc, encoding="utf-8")
    return it[pc]

def get_decision_tree(host_ip):
    play_feature_E = ['user_type', 'max_cpu', 'avg_cpu', 'max_memory', 'avg_memory', 'read_count', 'read_byte', 'write_count',
                      'write_byte', 'sockets_num', 'files_num', 'collect_rate', 'activity_rate']
    play_class = ['kernel', 'service', 'application', 'interactive',  'user']

    data = np.loadtxt("pdt.txt", delimiter=", ", dtype=float, converters={13: pc_convert})
    x, y = np.split(data, (13,), axis=1)

    clf = tree.DecisionTreeClassifier(criterion='gini')
    print(clf)
    clf.fit(x, y)

    file_name = host_ip+ '-proc_class'
    f = open(file_name + '.dot', 'w')

    dot_data = tree.export_graphviz(clf, out_file=f, feature_names=play_feature_E, class_names=play_class,
                                    filled=True, rounded=True, special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)

    graph.write_pdf(file_name +'.pdf')


    # tree.export_graphviz(clf.get_params('DTC')['DTC'], out_file=f)


if __name__ == '__main__':
    get_decision_tree('211.65.197.175')