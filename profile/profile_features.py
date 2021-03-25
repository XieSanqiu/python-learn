from elasticsearch import Elasticsearch
import time
import datetime
import numpy as np
import pymongo
import matplotlib
from matplotlib import pyplot as plt
font = {
    'family':'SimHei',
    'weight':'bold',
    'size':12
}
matplotlib.rc("font", **font)  #解决中文乱码
matplotlib.rcParams['axes.unicode_minus'] =False  #解决负号显示乱码

es = Elasticsearch("211.65.197.70")


# 还是根据 ip+进程exe+进程参数确定一个进程
def get_all_process(host, start_time, stop_time):
    mongo = pymongo.MongoClient('mongodb://211.65.197.70:27017')
    db = mongo['pinfo']
    activity_col = db['activity']
    fields = {'_id': 0, 'start_time': 0, 'collect_time': 0, 'connections': 0, 'open_files': 0,
                              'collect_date': 0, 'user_name': 0, 'HostIP':0}
    query = {'HostIP':host, 'collect_time': {'$gt': start_time, '$lte': stop_time}}
    res = activity_col.find(query, fields)
    all_processes = dict()
    for one in res:
        key = (one['proc_exe'], one['proc_param'])
        start_date = one['start_date']
        cpu_percent = round(one['cpu_percent'], 3)
        mem_percent = round(one['mem_percent'], 3)
        disk_read_rate = round(one['disk_read_rate'], 3)
        disk_write_rate = round(one['disk_write_rate'], 3)
        connections_num = one['connections_num']
        files_num = one['files_num']
        threads_num = one['threads']
        if key not in all_processes:
            start_date_set = set()
            start_date_set.add(start_date)
            cpu_percent_list = [cpu_percent]
            mem_percent_list = [mem_percent]
            disk_read_rate_list = [disk_read_rate]
            disk_write_rate_list = [disk_write_rate]
            connections_num_list = [connections_num]
            files_num_list = [files_num]
            threads_num_list = [threads_num]
            all_processes[key] = dict()
            all_processes[key]['start_date_set'] = start_date_set
            all_processes[key]['cpu_percent_list'] = cpu_percent_list
            all_processes[key]['mem_percent_list'] = mem_percent_list
            all_processes[key]['disk_read_rate_list'] = disk_read_rate_list
            all_processes[key]['disk_write_rate_list'] = disk_write_rate_list
            all_processes[key]['connections_num_list'] = connections_num_list
            all_processes[key]['files_num_list'] = files_num_list
            all_processes[key]['files_num_list'] = files_num_list
            all_processes[key]['threads_num_list'] = threads_num_list
        else:
            all_processes[key]['start_date_set'].add(start_date)
            all_processes[key]['cpu_percent_list'].append(cpu_percent)
            all_processes[key]['mem_percent_list'].append(mem_percent)
            all_processes[key]['disk_read_rate_list'].append(disk_read_rate)
            all_processes[key]['disk_write_rate_list'].append(disk_write_rate)
            all_processes[key]['connections_num_list'].append(connections_num)
            all_processes[key]['files_num_list'].append(files_num)
            all_processes[key]['threads_num_list'].append(threads_num)
    print(type(all_processes), len(all_processes))
    return all_processes

def calc_ent(x):
    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    prob = dict()
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        logp = np.log2(p)
        ent -= p * logp
        prob[x_value] = p
    return ent, prob

def analysis_start_date(key, start_date_set):
    start_times = len(start_date_set)
    start_hour_list = [0] * 24
    hour_list = []
    for start_date in start_date_set:
        hour = int(start_date.split(' ')[1].split(':')[0])
        start_hour_list[hour] += 1
        hour_list.append(hour)
    start_hour_array = np.array(hour_list)
    ent, prob = calc_ent(start_hour_array)
    prob = [0] * 24
    for i in range(len(start_hour_list)):
        prob[i] = start_hour_list[i] / start_times
    return start_times, ent, prob

def analysis_cpu_percent(key, cpu_percent_list):
    cpu_percent_array = np.array(cpu_percent_list)
    max = cpu_percent_array.max()
    min = cpu_percent_array.min()
    avg = cpu_percent_array.mean()
    ent, prob = calc_ent(cpu_percent_array)
    std = cpu_percent_array.std()
    return min, max, avg, std, ent, prob

def analysis_syscall(proc_exe):
    mongo = pymongo.MongoClient('mongodb://211.65.197.70:27017')
    db = mongo['pinfo']
    syscall_col = db['syscall']
    query = {'exe':proc_exe}
    res = syscall_col.find(query)
    syscalls_dict = dict()
    for one in res:
        pid = one['pid']
        session = one['session']
        syscall = one['syscall']
        key = (pid, session)
        if key not in syscalls_dict:
            syscalls_dict[key] = []
            syscalls_dict[key].append(syscall)
        else:
            syscalls_dict[key].append(syscall)
    print(len(syscalls_dict))
    call_dict = dict()
    count = 0
    for key in syscalls_dict:
        # print(key)
        # print(syscalls_dict[key])
        for call in syscalls_dict[key]:
            count += 1
            if call not in call_dict:
                call_dict[call] = 1
            else:
                call_dict[call] += 1
    prob = []
    for call in call_dict:
        print(call, call_dict[call], call_dict[call]/count)
        prob.append(call_dict[call]/count)
    prob.sort(reverse=True)
    plt.figure(figsize=(10, 5), dpi=80)  # 设置图形大小，分辨率
    plt.plot(prob, 'b-', label='syscall ')
    plt.legend(loc='upper left')
    plt.show()



if __name__ == '__main__':
    '''
    all_processes = get_all_process('211.65.197.233', 1616169600, 1616428800)
    for key in all_processes:
        # start_times, ent, prob = analysis_start_date(key, all_processes[key]['start_date_set'])
        # print(start_times, ent, prob)
        print(key)
        print(analysis_cpu_percent(key, all_processes[key]['threads_num_list']))
    '''
    analysis_syscall('/bin/su')