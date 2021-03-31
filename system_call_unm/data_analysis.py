'''
主要用于分析数据
'''
import os
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from system_call_unm import anomaly_detection, construct_hmm
font = {
    'family':'SimHei',
    'weight':'bold',
    'size':12
}
matplotlib.rc("font", **font)  #解决中文乱码
matplotlib.rcParams['axes.unicode_minus'] =False  #解决负号显示乱码
# 分析系统调用中各个系统调用的占比
def analysis1(file):
    call_count = {}
    call_ratio = {}
    total_count = 0
    res = dict()
    with open(file) as f:
        for line in f.readlines():
            calls = line.strip().split(' ')
            for call in calls[1:]:
                if call not in call_count:
                    call_count[call] = 1
                else:
                    call_count[call] += 1
                total_count += 1
    for key in call_count:
        call_ratio[key] = call_count[key] / total_count
        # print(key, call_count[key], call_ratio[key])
    return dict(sorted(call_ratio.items(), key=lambda x:x[1], reverse=True))

def analysis3(files):
    call_count = {}
    call_ratio = {}
    total_count = 0
    for file in files:
        with open(file) as f:
            for line in f.readlines():
                calls = line.strip().split(' ')
                for call in calls[1:]:
                    if call not in call_count:
                        call_count[call] = 1
                    else:
                        call_count[call] += 1
                    total_count += 1
    for key in call_count:
        call_ratio[key] = call_count[key] / total_count
        # print(key, call_count[key], call_ratio[key])
    return dict(sorted(call_ratio.items(), key=lambda x: x[1], reverse=True))

# 分析系统调用序列第一个系统调用
def analysis2(file):
    first_call_count = {}
    with open(file) as f:
        for line in f.readlines():
            calls = line.strip().split(' ')
            first_call = calls[1]
            if first_call not in first_call_count:
                first_call_count[first_call] = 1
            else:
                first_call_count[first_call] += 1
    print(first_call_count)

def profile(data_x, data_y1, data_y2, data_y3):
    plt.figure(figsize=(10, 5), dpi=80)  # 设置图形大小，分辨率
    plt.plot(data_x, data_y1, 'b-.*', label='train normal')
    plt.plot(data_x, data_y2, 'g-.+', label='verify normal')
    plt.plot(data_x, data_y3, 'y-.X', label='verify abnormal')

    plt.xlabel('system calls')
    plt.ylabel('probability')
    plt.legend(loc='upper right')

    plt.show()

def profile2(data_x, data_y1, data_y2, data_y3, data_y4):
    plt.figure(figsize=(10, 5), dpi=80)  # 设置图形大小，分辨率
    plt.plot(data_x, data_y1, 'b-.*', label='train normal others')
    plt.plot(data_x, data_y2, 'g-.+', label='verify normal others')
    plt.plot(data_x, data_y3, 'y-.X', label='verify abnormal others')

    plt.xlabel('others threshold')
    plt.ylabel('probability')
    plt.legend(loc='upper left')

    plt.show()

    fig, ax1 = plt.subplots(figsize=(10, 5), dpi=80)
    ax2 = ax1.twinx()  # 做镜像处理
    ax1.plot(data_x, data_y1, 'b-.*', label='train normal others')
    ax1.plot(data_x, data_y2, 'g-.+', label='verify normal others')
    ax1.plot(data_x, data_y3, 'y-.X', label='verify abnormal others')
    ax1.legend(loc='upper left')


    ax2.plot(data_x, data_y4, 'r-.', label='状态个数')
    ax2.set_ylim(0, 50)
    ax2.legend(loc='center left')

    ax1.set_xlabel('u')  # 设置x轴标题
    ax1.set_ylabel('probability')  # 设置Y1轴标题
    ax2.set_ylabel('stat num')  # 设置Y2轴标题

    plt.show()

#分析前十个系统调用在训练数据、验证数据、异常数据中的概率
def main1():
    file1 = 'D:\毕业论文相关\数据集\sendmail-UNM\\normal\sendmail.log.txt'
    file2 = 'D:\毕业论文相关\数据集\sendmail-UNM\\normal\yanzheng.txt'
    dir = 'D:\毕业论文相关\数据集\sendmail-UNM\\abnormal'
    files = []
    for file in os.listdir(dir):
        if file.endswith('txt'):
            files.append(dir + '\\' + file)
    print(files)
    res_normal = analysis1(file1)
    print(res_normal)
    print('\n')

    res_normal2 = analysis1(file2)
    print(res_normal2)
    print('\n')

    res_abnormal = analysis3(files)
    print(res_abnormal)

    top_calls = []
    i = 0
    for call in res_normal:
        i += 1
        top_calls.append(call)
        if i == 10:
            break
    normal_ratio = []
    normal2_ratio = []
    abnormal_ratio = []
    for call in top_calls:
        normal_ratio.append(res_normal[call])
        normal2_ratio.append(res_normal2[call])
        abnormal_ratio.append(res_abnormal[call])
    print(normal_ratio)
    print(normal2_ratio)
    print(abnormal_ratio)
    profile(top_calls, normal_ratio, normal2_ratio, abnormal_ratio)

def main2():
    file1 = 'D:\毕业论文相关\数据集\sendmail-UNM\\normal\sendmail.log.txt'
    file2 = 'D:\毕业论文相关\数据集\sendmail-UNM\\normal\yanzheng.txt'
    dir = 'D:\毕业论文相关\数据集\sendmail-UNM\\abnormal'
    files = []
    for file in os.listdir(dir):
        if file.endswith('txt'):
            files.append(dir + '\\' + file)
    res_normal = analysis1(file1)
    print(res_normal)
    print('\n')

    res_normal2 = analysis1(file2)
    print(res_normal2)
    print('\n')

    res_abnormal = analysis3(files)
    print(res_abnormal)
    print('\n')
    other_threshold_list = []
    normal_other_list = []
    normal2_other_list = []
    abnormal_other_list = []
    stat_list = []
    for i in range(1, 11, 1):
        other_threshold = i/1000
        other_threshold_list.append(other_threshold)
        old_calls_dict = construct_hmm.get_calls_dict([file1])
        new_calls_dict = construct_hmm.get_new_calls_dict(old_calls_dict, other_threshold)
        print('new_calls_dict', len(new_calls_dict), new_calls_dict)
        stat_list.append(len(new_calls_dict))
        normal_other = new_calls_dict['others']
        normal_other_list.append(normal_other)
        normal2_other = 0.0
        for call in res_normal2:
            if call not in new_calls_dict:
                normal2_other += res_normal2[call]
        abnormal_other = 0.0
        for call in res_abnormal:
            if call not in new_calls_dict:
                abnormal_other += res_abnormal[call]
        print(normal_other, normal2_other, abnormal_other)
        normal2_other_list.append(normal2_other)
        abnormal_other_list.append(abnormal_other)
    profile2(other_threshold_list, normal_other_list, normal2_other_list, abnormal_other_list, stat_list)

def main3():
    file1 = 'D:\毕业论文相关\数据集\sendmail-UNM\\normal\sendmail.log.txt'
    dir = 'D:\毕业论文相关\数据集\sendmail-UNM\\abnormal'
    files = []
    for file in os.listdir(dir):
        if file.endswith('txt'):
            files.append(dir + '\\' + file)

    other_threshold = 0.005
    old_calls_dict = construct_hmm.get_calls_dict([file1])
    new_calls_dict = construct_hmm.get_new_calls_dict(old_calls_dict, other_threshold)
    call_num_dict = dict()
    num = 0
    for call in new_calls_dict:
        call_num_dict[call] = num
        num += 1
    print(call_num_dict)
    # print('new_calls_dict', len(new_calls_dict), new_calls_dict)
    A_dict = construct_hmm.get_A_dict(new_calls_dict, [file1])
    print('A_dict', A_dict)
    threeD_matrix = np.zeros([len(new_calls_dict), len(new_calls_dict)])

    for d in A_dict:
        print(d)
        x = call_num_dict[d]
        sorted_dict = dict(sorted(A_dict[d].items(), key=lambda x: x[1], reverse=True))
        for call in sorted_dict:
            y = call_num_dict[call]
            threeD_matrix[x][y] = sorted_dict[call]
    print(threeD_matrix)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(new_calls_dict)):
        xs = np.arange(len(new_calls_dict))
        ys = threeD_matrix[i]
        ax.bar(xs, ys, zs=i, zdir='y')
    plt.show()

    A_dict_abnormal = construct_hmm.get_A_dict(new_calls_dict, files)
    print('A_dict_abnormal', A_dict_abnormal)
    threeD_matrix = np.zeros([len(new_calls_dict), len(new_calls_dict)])

    for d in A_dict_abnormal:
        print(d)
        x = call_num_dict[d]
        sorted_dict = dict(sorted(A_dict_abnormal[d].items(), key=lambda x: x[1], reverse=True))
        for call in sorted_dict:
            y = call_num_dict[call]
            threeD_matrix[x][y] = sorted_dict[call]
    print(threeD_matrix)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(new_calls_dict)):
        xs = np.arange(len(new_calls_dict))
        ys = threeD_matrix[i]
        ax.bar(xs, ys, zs=i, zdir='y')
    plt.show()


if __name__ == '__main__':
    main3()