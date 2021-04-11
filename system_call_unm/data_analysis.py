'''
主要用于分析数据
'''
import os
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pymongo
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

#对状态画像
def profile3(data_x, data_y1, proc_name, threshold):
    plt.figure(figsize=(10, 5), dpi=80)  # 设置图形大小，分辨率
    # plt.plot(data_x, data_y1, 'b-.*', label='train normal others')
    plt.bar(data_x, data_y1, width=0.5)

    plt.xticks(rotation=310)
    plt.xlabel('system calls')
    plt.ylabel('probability')
    plt.legend(loc='upper left')
    title = proc_name + ' u=' + str(threshold)
    plt.title(title)

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

def main4():
    mongo = pymongo.MongoClient('mongodb://211.65.197.70:27017')
    db = mongo['pinfo']
    syscall_col = db['syscall']
    query = {'exe': '/bin/su', 'hostIP': '211.65.197.233', 'timestamp': {'$gt': 1617510758}}
    res = syscall_col.find(query).sort([('timestamp', 1), ('event_id',1)])
    syscalls_dict = dict()
    calls_set = set()
    for one in res:
        if 'event_id' not in one:
            continue
        pid = one['pid']
        session = one['session']
        syscall = one['syscall']
        event_id = one['event_id']
        key = (pid, session)
        calls_set.add(syscall)
        if key not in syscalls_dict:
            syscalls_dict[key] = []
            # syscalls_dict[key].append([syscall, event_id])
            syscalls_dict[key].append(syscall)
        else:
            syscalls_dict[key].append(syscall)

    print('syscalls_dict:', len(syscalls_dict))
    total_syscalls = 0
    all_calls_lsit = []
    for key in syscalls_dict:
        syscalls_len = len(syscalls_dict[key])
        print(key, syscalls_len)
        if syscalls_len < 10:
            continue
        total_syscalls += len(syscalls_dict[key])
        all_calls_lsit.append(syscalls_dict[key])
    print('序列个数:', len(all_calls_lsit))
    print('系统调用个数:', len(calls_set))
    print('系统调用总个数:', total_syscalls)
    # print(all_calls_lsit)

    calls_dict = {}
    count = 0
    calls_set2 = set()
    total_syscalls2 = 0
    for calls in all_calls_lsit[:70]:
        total_syscalls2 += len(calls)
        for call in calls:
            count += 1
            calls_set2.add(call)
            if call not in calls_dict:
                calls_dict[call] = 1
            else:
                calls_dict[call] += 1
    print('系统调用个数2:', len(calls_set2))
    print('系统调用总个数2:', total_syscalls2)
    for key in calls_dict:
        calls_dict[key] = calls_dict[key] / count

    other_threshold = 0.005
    old_calls_dict = calls_dict
    new_calls_dict = construct_hmm.get_new_calls_dict(old_calls_dict, other_threshold)

    new_calls_dict_order = sorted(new_calls_dict.items(), key=lambda x: x[1], reverse=True)
    new_calls_list = []
    new_calls_p_list = []
    for pair in new_calls_dict_order:
        print(pair)
        new_calls_list.append(pair[0])
        new_calls_p_list.append(pair[1])

    #画状态概率
    # profile3(new_calls_list, new_calls_p_list, 'su', other_threshold)

    A_dict = {}
    for calls in all_calls_lsit[:70]:
        for call, next_call in zip(calls[:-1], calls[1:]):
            if call not in new_calls_dict:
                call = 'others'
            if next_call not in new_calls_dict:
                next_call = 'others'
            if call not in A_dict:
                A_dict[call] = {}
            if next_call not in A_dict[call]:
                A_dict[call][next_call] = 1
            else:
                A_dict[call][next_call] += 1
    for key in A_dict:
        sum = 0
        for key_key in A_dict[key]:
            sum += A_dict[key][key_key]
        for key_key in A_dict[key]:
            A_dict[key][key_key] = A_dict[key][key_key] / sum

    print('A_dict', len(A_dict))
    for key in A_dict:
        print(key, len(A_dict[key]), A_dict[key])

    res = anomaly_detection.cal_prob(syscalls_dict[(19703, 245148)], new_calls_dict, A_dict, 6)
    min_res = min(res)
    print(min_res, res)
    plt.figure(figsize=(10, 5), dpi=80)  # 设置图形大小，分辨率
    plt.plot(np.arange(len(res)), res)
    plt.axhline(min_res, color='r', linestyle='--')
    plt.ylabel('转移概率')
    plt.legend(loc='upper left')

    plt.show()

    #3D画图，状态转移矩阵
    # threeD_matrix = np.zeros([len(new_calls_dict), len(new_calls_dict)])
    # x = 0
    # for callx in new_calls_list:
    #     y = 0
    #     for cally in new_calls_list:
    #         if cally in A_dict[callx]:
    #             threeD_matrix[x][y] = A_dict[callx][cally]
    #         y += 1
    #     x += 1
    # print(threeD_matrix)
    #
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # for i in range(len(new_calls_dict)):
    #     xs = np.arange(len(new_calls_dict))
    #     ys = threeD_matrix[i]
    #     ax.bar(xs, ys, zs=i, zdir='y')
    # plt.title('su u=0.005')
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    # plt.show()

#阈值u的变化与状态数的变化
def main5():
    mongo = pymongo.MongoClient('mongodb://211.65.197.70:27017')
    db = mongo['pinfo']
    syscall_col = db['syscall']
    pairs = [('211.65.197.233', '/bin/su', 40), ('211.65.197.233', '/bin/ping', 40), ('211.65.197.233', '/bin/su', 70)]
    su_40_stat_num_list = []
    su_70_stat_num_list = []
    ping_40_stat_num_list = []
    u_list = []
    for p in pairs:
        query = {'exe': p[1], 'hostIP': p[0]}
        res = syscall_col.find(query).sort([('timestamp', 1), ('event_id', 1)])
        syscalls_dict = dict()
        calls_set = set()
        for one in res:
            if 'event_id' not in one:
                continue
            pid = one['pid']
            session = one['session']
            syscall = one['syscall']
            event_id = one['event_id']
            key = (pid, session)
            calls_set.add(syscall)
            if key not in syscalls_dict:
                syscalls_dict[key] = []
                # syscalls_dict[key].append([syscall, event_id])
                syscalls_dict[key].append(syscall)
            else:
                syscalls_dict[key].append(syscall)

        print(len(syscalls_dict))
        total_syscalls = 0
        all_calls_lsit = []
        for key in syscalls_dict:
            print(key, len(syscalls_dict[key]))
            total_syscalls += len(syscalls_dict[key])
            if len(syscalls_dict[key]) < 10:
                continue
            all_calls_lsit.append(syscalls_dict[key])
        print('序列个数:', len(all_calls_lsit))
        print('系统调用个数:', len(calls_set))
        print('系统调用总个数:', total_syscalls)
        # print(all_calls_lsit)

        calls_dict = {}
        count = 0
        for calls in all_calls_lsit[:p[2]]:
            for call in calls:
                count += 1
                if call not in calls_dict:
                    calls_dict[call] = 1
                else:
                    calls_dict[call] += 1
        for key in calls_dict:
            calls_dict[key] = calls_dict[key] / count
        for i in range(0, 11, 1):
            other_threshold = i / 1000
            u_list.append(other_threshold)
            old_calls_dict = calls_dict
            new_calls_dict = construct_hmm.get_new_calls_dict(old_calls_dict, other_threshold)
            if p == ('211.65.197.233', '/bin/su', 40):
                su_40_stat_num_list.append(len(new_calls_dict))
            elif p == ('211.65.197.233', '/bin/ping', 40):
                ping_40_stat_num_list.append(len(new_calls_dict))
            else:
                su_70_stat_num_list.append(len(new_calls_dict))
    print(u_list)
    print(su_40_stat_num_list)
    print(ping_40_stat_num_list)
    print(su_70_stat_num_list)
    plt.figure(figsize=(10, 5), dpi=80)  # 设置图形大小，分辨率
    plt.plot(u_list[:11], su_40_stat_num_list, 'b-.*', label='su-40')
    plt.plot(u_list[:11], ping_40_stat_num_list, 'g-.+', label='ping-40')
    plt.plot(u_list[:11], su_70_stat_num_list, 'y-.X', label='su-70')

    plt.xlabel('阈值u')
    plt.ylabel('状态个数')
    plt.ylim(0,60)
    plt.legend(loc='upper left')

    plt.show()

def help_main6(all_calls_lsit, syscalls):
    calls_dict = {}
    count = 0
    calls_set2 = set()
    total_syscalls2 = 0
    for calls in all_calls_lsit:
        total_syscalls2 += len(calls)
        for call in calls:
            count += 1
            calls_set2.add(call)
            if call not in calls_dict:
                calls_dict[call] = 1
            else:
                calls_dict[call] += 1
    print('系统调用个数2:', len(calls_set2))
    print('系统调用总个数2:', total_syscalls2)
    for key in calls_dict:
        calls_dict[key] = calls_dict[key] / count

    other_threshold = 0.005
    old_calls_dict = calls_dict
    new_calls_dict = construct_hmm.get_new_calls_dict(old_calls_dict, other_threshold)

    A_dict = {}
    for calls in all_calls_lsit:
        for call, next_call in zip(calls[:-1], calls[1:]):
            if call not in new_calls_dict:
                call = 'others'
            if next_call not in new_calls_dict:
                next_call = 'others'
            if call not in A_dict:
                A_dict[call] = {}
            if next_call not in A_dict[call]:
                A_dict[call][next_call] = 1
            else:
                A_dict[call][next_call] += 1
    for key in A_dict:
        sum = 0
        for key_key in A_dict[key]:
            sum += A_dict[key][key_key]
        for key_key in A_dict[key]:
            A_dict[key][key_key] = A_dict[key][key_key] / sum

    print('A_dict', len(A_dict))
    for key in A_dict:
        print(key, len(A_dict[key]), A_dict[key])

    res = anomaly_detection.cal_prob(syscalls, new_calls_dict, A_dict, 6)
    return res

def main6():
    mongo = pymongo.MongoClient('mongodb://211.65.197.70:27017')
    db = mongo['pinfo']
    syscall_col = db['syscall']
    query = {'exe': '/bin/su', 'hostIP': '211.65.197.233', 'timestamp': {'$gt': 1617510758}}
    res = syscall_col.find(query).sort([('timestamp', 1), ('event_id', 1)])
    syscalls_dict = dict()
    calls_set = set()
    for one in res:
        if 'event_id' not in one:
            continue
        pid = one['pid']
        session = one['session']
        syscall = one['syscall']
        event_id = one['event_id']
        key = (pid, session)
        calls_set.add(syscall)
        if key not in syscalls_dict:
            syscalls_dict[key] = []
            # syscalls_dict[key].append([syscall, event_id])
            syscalls_dict[key].append(syscall)
        else:
            syscalls_dict[key].append(syscall)

    print('syscalls_dict:', len(syscalls_dict))
    total_syscalls = 0
    all_calls_lsit = []
    for key in syscalls_dict:
        syscalls_len = len(syscalls_dict[key])
        print(key, syscalls_len)
        if syscalls_len < 10:
            continue
        total_syscalls += len(syscalls_dict[key])
        all_calls_lsit.append(syscalls_dict[key])
    print('序列个数:', len(all_calls_lsit))
    print('系统调用个数:', len(calls_set))
    print('系统调用总个数:', total_syscalls)
    print(all_calls_lsit)

    su_syscalls = syscalls_dict[((4295, 537))]
    ping_syscalls = ['execve', 'access', 'brk', 'fcntl', 'fcntl', 'fcntl', 'access', 'access', 'openat', 'fstat', 'mmap', 'close', 'openat', 'read', 'fstat', 'mmap', 'mmap', 'mprotect', 'mmap', 'close', 'openat', 'read', 'fstat', 'mmap', 'mprotect', 'mmap', 'close', 'openat', 'read', 'fstat', 'mmap', 'mprotect', 'mmap', 'close', 'openat', 'read', 'fstat', 'mmap', 'mprotect', 'mmap', 'mmap', 'mmap', 'mmap', 'close', 'openat', 'read', 'fstat', 'mmap', 'mmap', 'mmap', 'mmap', 'close', 'openat', 'read', 'fstat', 'mmap', 'mprotect', 'mmap', 'mmap', 'mmap', 'mmap', 'close', 'mmap', 'arch_prctl', 'mprotect', 'mprotect', 'mprotect', 'mprotect', 'mprotect', 'mprotect', 'mprotect', 'mprotect', 'munmap', 'brk', 'brk', 'capget', 'capget', 'capget', 'capset', 'prctl', 'getuid', 'setuid', 'prctl', 'getuid', 'geteuid', 'openat', 'fstat', 'mmap', 'close', 'capget', 'capget', 'capset', 'socket', 'socket', 'socket', 'socket', 'capget', 'capget', 'capset', 'openat', 'fstat', 'mmap', 'close', 'socket', 'connect', 'close', 'socket', 'connect', 'close', 'openat', 'fstat', 'read', 'read', 'close', 'stat', 'openat', 'fstat', 'read', 'read', 'close', 'openat', 'fstat', 'read', 'read', 'close', 'uname', 'openat', 'fstat', 'mmap', 'close', 'openat', 'read', 'fstat', 'mmap', 'mprotect', 'mmap', 'mmap', 'mmap', 'mmap', 'close', 'mprotect', 'munmap', 'openat', 'lseek', 'fstat', 'read', 'lseek', 'read', 'close', 'openat', 'fstat', 'mmap', 'close', 'openat', 'read', 'fstat', 'mmap', 'mmap', 'mmap', 'mmap', 'close', 'mprotect', 'munmap', 'socket', 'connect', 'poll', 'sendmmsg', 'poll', 'ioctl', 'recvfrom', 'poll', 'ioctl', 'recvfrom', 'close', 'openat', 'fstat', 'mmap', 'close', 'openat', 'read', 'fstat', 'mmap', 'mprotect', 'mmap', 'close', 'openat', 'stat', 'openat', 'stat', 'openat', 'stat', 'openat', 'stat', 'openat', 'stat', 'openat', 'stat', 'openat', 'stat', 'openat', 'read', 'fstat', 'mmap', 'mprotect', 'mmap', 'mmap', 'close', 'mprotect', 'mprotect', 'munmap', 'munmap', 'munmap', 'openat', 'fstat', 'fstat', 'read', 'read', 'close', 'socket', 'bind', 'getsockname', 'sendto', 'recvmsg', 'recvmsg', 'recvmsg', 'close', 'socket', 'connect', 'getsockname', 'connect', 'connect', 'getsockname', 'connect', 'connect', 'getsockname', 'connect', 'connect', 'getsockname', 'close', 'socket', 'connect', 'getsockname', 'close', 'setsockopt', 'setsockopt', 'setsockopt', 'getsockopt', 'setsockopt', 'setsockopt', 'setsockopt', 'stat', 'openat', 'lseek', 'fstat', 'read', 'lseek', 'read', 'close', 'socket', 'connect', 'poll', 'sendto', 'poll', 'ioctl', 'recvfrom', 'close', 'fstat', 'write', 'setsockopt', 'setsockopt', 'setsockopt', 'getpid', 'rt_sigaction', 'rt_sigaction', 'rt_sigaction', 'rt_sigprocmask', 'ioctl', 'ioctl', 'capget', 'capset', 'sendto', 'recvmsg', 'stat', 'openat', 'lseek', 'fstat', 'read', 'lseek', 'read', 'close', 'socket', 'connect', 'poll', 'sendto', 'poll', 'ioctl', 'recvfrom', 'close', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'sendto', 'recvmsg', 'write', 'poll', 'rt_sigreturn', 'write', 'write', 'write', 'write', 'exit_group']

    su_40 = help_main6(all_calls_lsit[:40], su_syscalls)
    su_70 = help_main6(all_calls_lsit[:70], su_syscalls)
    ping_40 = help_main6(all_calls_lsit[:40], ping_syscalls)
    print(su_40)
    print(su_70)
    print(ping_40)
    plt.figure(figsize=(10, 5), dpi=80)  # 设置图形大小，分辨率
    x_len = min(len(su_40), len(ping_40))
    plt.plot(np.arange(x_len), su_40[:x_len], 'b-', label='su syscalls on su-40')
    plt.plot(np.arange(x_len), su_70[:x_len], 'g-', label='su syscalls on su-70')
    plt.plot(np.arange(x_len), ping_40[:x_len], 'r-.', label='ping syscalls on su-40')

    # plt.axhline(min_res, color='r', linestyle='--')
    plt.ylabel('转移概率')
    plt.legend(loc='upper left')

    plt.show()

if __name__ == '__main__':
    main6()