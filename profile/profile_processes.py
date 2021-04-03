from elasticsearch import Elasticsearch
import time
import datetime
import xlwt, xlrd
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
                              'collect_date': 0, 'HostIP':0}
    query = {'HostIP':host, 'collect_time': {'$gt': start_time, '$lte': stop_time}}
    res = activity_col.find(query, fields)
    all_processes = dict()
    for one in res:
        key = (one['proc_exe'], one['proc_param'])
        proc_name = one['proc_name']
        proc_user = one['user_name']
        start_date = one['start_date']
        cpu_percent = round(one['cpu_percent'], 3)
        mem_percent = round(one['mem_percent'], 3)
        disk_read_rate = round(one['disk_read_rate'], 3)
        disk_write_rate = round(one['disk_write_rate'], 3)
        connections_num = one['connections_num']
        files_num = one['files_num']
        threads_num = one['threads']
        if key not in all_processes:
            proc_name_set = set()
            proc_name_set.add(proc_name)
            proc_user_set = set()
            proc_user_set.add(proc_user)
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
            all_processes[key]['proc_name_set'] = proc_name_set
            all_processes[key]['proc_user_set'] = proc_user_set
            all_processes[key]['start_date_set'] = start_date_set
            all_processes[key]['cpu_percent_list'] = cpu_percent_list
            all_processes[key]['mem_percent_list'] = mem_percent_list
            all_processes[key]['disk_read_rate_list'] = disk_read_rate_list
            all_processes[key]['disk_write_rate_list'] = disk_write_rate_list
            all_processes[key]['connections_num_list'] = connections_num_list
            all_processes[key]['files_num_list'] = files_num_list
            all_processes[key]['threads_num_list'] = threads_num_list
        else:
            all_processes[key]['proc_name_set'].add(proc_name)
            all_processes[key]['proc_user_set'].add(proc_user)
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

#计算一个数组信息熵 np.array
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

def analysis_start_date(start_date_set):
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

def analysis_features(features_list):
    features_array = np.array(features_list)
    max = features_array.max()
    min = features_array.min()
    avg = features_array.mean()
    ent, prob = calc_ent(features_array)
    std = features_array.std()
    return min, max, avg, std, ent, prob

if __name__ == '__main__':
    all_processes = get_all_process('211.65.197.233', 1616688000, 1617206400)
    # 创建workbook和sheet对象
    workbook = xlwt.Workbook()  # 注意Workbook的开头W要大写
    sheet1 = workbook.add_sheet('startup information', cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet('cpu percent', cell_overwrite_ok=True)
    sheet3 = workbook.add_sheet('memory percent', cell_overwrite_ok=True)
    sheet4 = workbook.add_sheet('disk read rate', cell_overwrite_ok=True)
    sheet5 = workbook.add_sheet('disk write rate', cell_overwrite_ok=True)
    sheet6 = workbook.add_sheet('connections num', cell_overwrite_ok=True)
    sheet7 = workbook.add_sheet('files num', cell_overwrite_ok=True)
    sheet8 = workbook.add_sheet('threads num', cell_overwrite_ok=True)
    # 向sheet页中写入数据
    sheet1.write(0, 0, 'proc_exe')
    sheet1.write(0, 1, 'proc_param')
    sheet1.write(0, 2, 'proc_name')
    sheet1.write(0, 3, 'proc_user')
    sheet1.write(0, 4, 'start time times')
    sheet1.write(0, 5, 'start time set')
    sheet1.write(0, 6, 'start time probability entropy ')
    sheet1.write(0, 7, 'start time distribution')

    sheet2.write(0, 0, 'proc_exe')
    sheet2.write(0, 1, 'proc_param')
    sheet2.write(0, 2, 'range')
    sheet2.write(0, 3, 'average')
    sheet2.write(0, 4, 'standard deviation')
    sheet2.write(0, 5, 'Information entropy')
    sheet2.write(0, 6, 'distribution probability')

    sheet3.write(0, 0, 'proc_exe')
    sheet3.write(0, 1, 'proc_param')
    sheet3.write(0, 2, 'range')
    sheet3.write(0, 3, 'average')
    sheet3.write(0, 4, 'standard deviation')
    sheet3.write(0, 5, 'Information entropy')
    sheet3.write(0, 6, 'distribution probability')

    sheet4.write(0, 0, 'proc_exe')
    sheet4.write(0, 1, 'proc_param')
    sheet4.write(0, 2, 'range')
    sheet4.write(0, 3, 'average')
    sheet4.write(0, 4, 'standard deviation')
    sheet4.write(0, 5, 'Information entropy')
    sheet4.write(0, 6, 'distribution probability')

    sheet5.write(0, 0, 'proc_exe')
    sheet5.write(0, 1, 'proc_param')
    sheet5.write(0, 2, 'range')
    sheet5.write(0, 3, 'average')
    sheet5.write(0, 4, 'standard deviation')
    sheet5.write(0, 5, 'Information entropy')
    sheet5.write(0, 6, 'distribution probability')

    sheet6.write(0, 0, 'proc_exe')
    sheet6.write(0, 1, 'proc_param')
    sheet6.write(0, 2, 'range')
    sheet6.write(0, 3, 'average')
    sheet6.write(0, 4, 'standard deviation')
    sheet6.write(0, 5, 'Information entropy')
    sheet6.write(0, 6, 'distribution probability')

    sheet7.write(0, 0, 'proc_exe')
    sheet7.write(0, 1, 'proc_param')
    sheet7.write(0, 2, 'range')
    sheet7.write(0, 3, 'average')
    sheet7.write(0, 4, 'standard deviation')
    sheet7.write(0, 5, 'Information entropy')
    sheet7.write(0, 6, 'distribution probability')

    sheet8.write(0, 0, 'proc_exe')
    sheet8.write(0, 1, 'proc_param')
    sheet8.write(0, 2, 'range')
    sheet8.write(0, 3, 'average')
    sheet8.write(0, 4, 'standard deviation')
    sheet8.write(0, 5, 'Information entropy')
    sheet8.write(0, 6, 'distribution probability')

    i = 1
    for key in all_processes:
        # start_times, ent, prob = analysis_start_date(key, all_processes[key]['start_date_set'])
        # print(start_times, ent, prob)
        proc_exe = key[0]
        proc_param = key[1]
        if proc_exe == '/bin/ls' or proc_exe == '/usr/bin/tshark':
            continue
        proc_name_set = all_processes[key]['proc_name_set']
        proc_user_set = all_processes[key]['proc_user_set']
        start_date_set = all_processes[key]['start_date_set']
        start_times, ent, prob= analysis_start_date(start_date_set)
        sheet1.write(i, 0, proc_exe)
        sheet1.write(i, 1, proc_param)
        sheet1.write(i, 2, ', '.join(list(proc_name_set)))
        sheet1.write(i, 3, ', '.join(list(proc_user_set)))
        sheet1.write(i, 4, start_times)
        sheet1.write(i, 5, ', '.join(list(start_date_set)))
        sheet1.write(i, 6, ent)
        sheet1.write(i, 7, ', '.join([str(x) for x in prob]))

        cpu_min, cpu_max, cpu_avg, cpu_std, cpu_ent, cpu_prob = analysis_features(
            all_processes[key]['cpu_percent_list'])
        sheet2.write(i, 0, proc_exe)
        sheet2.write(i, 1, proc_param)
        sheet2.write(i, 2, '[' + str(cpu_min) + ', ' + str(cpu_max) + ']')
        sheet2.write(i, 3, cpu_avg)
        sheet2.write(i, 4, cpu_std)
        sheet2.write(i, 5, cpu_ent)
        sheet2.write(i, 6, str(cpu_prob))

        mem_min, mem_max, mem_avg, mem_std, mem_ent, mem_prob = analysis_features(
            all_processes[key]['mem_percent_list'])
        sheet3.write(i, 0, proc_exe)
        sheet3.write(i, 1, proc_param)
        sheet3.write(i, 2, '[' + str(mem_min) + ', ' + str(mem_max) + ']')
        sheet3.write(i, 3, mem_avg)
        sheet3.write(i, 4, mem_std)
        sheet3.write(i, 5, mem_ent)
        sheet3.write(i, 6, str(mem_prob))

        drr_min, drr_max, drr_avg, drr_std, drr_ent, drr_prob = analysis_features(
            all_processes[key]['disk_read_rate_list'])
        sheet4.write(i, 0, proc_exe)
        sheet4.write(i, 1, proc_param)
        sheet4.write(i, 2, '[' + str(drr_min) + ', ' + str(drr_max) + ']')
        sheet4.write(i, 3, drr_avg)
        sheet4.write(i, 4, drr_std)
        sheet4.write(i, 5, drr_ent)
        sheet4.write(i, 6, str(drr_prob))

        dwr_min, dwr_max, dwr_avg, dwr_std, dwr_ent, dwr_prob = analysis_features(
            all_processes[key]['disk_write_rate_list'])
        sheet5.write(i, 0, proc_exe)
        sheet5.write(i, 1, proc_param)
        sheet5.write(i, 2, '[' + str(dwr_min) + ', ' + str(dwr_max) + ']')
        sheet5.write(i, 3, dwr_avg)
        sheet5.write(i, 4, dwr_std)
        sheet5.write(i, 5, dwr_ent)
        sheet5.write(i, 6, str(dwr_prob))

        cn_min, cn_max, cn_avg, cn_std, cn_ent, cn_prob = analysis_features(
            all_processes[key]['connections_num_list'])
        sheet6.write(i, 0, proc_exe)
        sheet6.write(i, 1, proc_param)
        sheet6.write(i, 2, '[' + str(cn_min) + ', ' + str(cn_max) + ']')
        sheet6.write(i, 3, cn_avg)
        sheet6.write(i, 4, cn_std)
        sheet6.write(i, 5, cn_ent)
        sheet6.write(i, 6, str(cn_prob))

        fn_min, fn_max, fn_avg, fn_std, fn_ent, fn_prob = analysis_features(
            all_processes[key]['files_num_list'])
        sheet7.write(i, 0, proc_exe)
        sheet7.write(i, 1, proc_param)
        sheet7.write(i, 2, '[' + str(fn_min) + ', ' + str(fn_max) + ']')
        sheet7.write(i, 3, fn_avg)
        sheet7.write(i, 4, fn_std)
        sheet7.write(i, 5, fn_ent)
        sheet7.write(i, 6, str(fn_prob))

        tn_min, tn_max, tn_avg, tn_std, tn_ent, tn_prob = analysis_features(
            all_processes[key]['threads_num_list'])
        sheet8.write(i, 0, proc_exe)
        sheet8.write(i, 1, proc_param)
        sheet8.write(i, 2, '[' + str(tn_min) + ', ' + str(tn_max) + ']')
        sheet8.write(i, 3, tn_avg)
        sheet8.write(i, 4, tn_std)
        sheet8.write(i, 5, tn_ent)
        sheet8.write(i, 6, str(tn_prob))

        i += 1

    # 保存该excel文件,有同名文件时直接覆盖
    workbook.save('test2.xls')
    print('创建excel文件完成！')