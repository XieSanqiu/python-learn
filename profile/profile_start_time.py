from elasticsearch import Elasticsearch
import time
import datetime
import numpy as np
import matplotlib
from matplotlib import pyplot as plt

font = {
    'family': 'SimHei',
    'weight': 'bold',
    'size': 12
}
matplotlib.rc("font", **font)  # 解决中文乱码
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示乱码

es = Elasticsearch("211.65.197.70")


# 还是根据 ip+进程exe+进程参数确定一个进程
def get_all_process(host, proc_name):
    try:
        # es = Elasticsearch("211.65.197.70")
        idx = host + "-pinfo-*"
        dds = []
        if es.indices.exists(index=idx):
            es_query1 = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "match": {
                                    "proc_name": proc_name
                                }
                            }
                        ],
                        "filter": {
                            "range": {
                                "collect_date": {
                                    "gte": "2021-03-18T00:00:00.046851",
                                    "lte": "2021-03-24T00:00:00.046851"
                                }
                            }
                        }
                    }
                },
                "size": 100
            }
            esData = es.search(index=idx, scroll='5m', timeout='5s', body=es_query1)
            scroll_id = esData["_scroll_id"]
            total = esData['hits']['total']
            print(total)
            datas = esData['hits']['hits']

            for i in range((int)(total / 100)):
                res = es.scroll(scroll_id=scroll_id, scroll='5m')
                datas += res["hits"]["hits"]
            for data in datas:
                d = dict()
                d['start_date'] = data['_source']['start_date']
                d['start_time'] = float(data['_source']['start_time'])
                d['user_name'] = data['_source']['user_name']
                d['collect_date'] = data['_source']['collect_date']

                # print(d)
                dds.append(d)
        else:
            print(idx, "not exists")
        return dds
    except Exception as ee:
        print('get_all_process', ee)


def get_all_process2(host):
    try:
        idx = host + "-pinfo-*"
        if es.indices.exists(index=idx):
            es_query1 = {
                "query": {
                    "range": {
                        "collect_date": {
                            "gte": "2021-03-19T00:00:00.046851",
                            "lte": "2021-03-25T00:00:00.046851"
                        }
                    }
                },
                "size": 100
            }
            esData = es.search(index=idx, scroll='5m', timeout='5s', body=es_query1)
            scroll_id = esData["_scroll_id"]
            total = esData['hits']['total']
            print(total)
            datas = esData['hits']['hits']

            for i in range((int)(total / 100)):
                res = es.scroll(scroll_id=scroll_id, scroll='5m')
                datas += res["hits"]["hits"]
            process_start_date = dict()
            for data in datas:
                d = dict()
                pid = data['_source']['pid']
                ppid = data['_source']['ppid']
                if pid == 2 or ppid == 2:
                    continue
                proc_exe = data['_source']['proc_exe']
                proc_param = data['_source']['proc_param']
                key = (proc_exe, proc_param)
                start_date = data['_source']['start_date']
                if key not in process_start_date:
                    process_start_date[key] = set()
                    process_start_date[key].add(start_date)
                else:
                    process_start_date[key].add(start_date)
        else:
            print(idx, "not exists")
        return process_start_date
    except Exception as ee:
        print('get_all_process', ee)


def profile_start_date(data_x, data_y, proc_name):
    for i in range(len(data_y)):
        data_y[i] *= 2
    # plt.plot(data_x, data_y)
    plt.figure(figsize=(10, 5), dpi=80)  # 设置图形大小，分辨率
    plt.title(proc_name)
    plt.bar(range(len(data_x)), data_y, width=0.4, alpha=0.8, color='green')
    plt.xticks(range(len(data_x)), data_x)
    plt.ylabel('times')
    plt.xlabel('time(hour)')
    plt.show()


def profile_proc(host_ip, proc_name):
    dds = get_all_process(host_ip, proc_name)
    start_date_set = set()
    start_date_dict = dict()
    for dd in dds:
        start_date_set.add(dd['start_date'])
    for start_date in start_date_set:
        hour = int(start_date.split('T')[1].split(':')[0])
        if hour not in start_date_dict:
            start_date_dict[hour] = 1
        else:
            start_date_dict[hour] += 1
    start_hour_list = [0] * 24
    for key in start_date_dict:
        print(key, start_date_dict[key])
        start_hour_list[(key + 8) % 24] = start_date_dict[key]
    x = range(0, 24)
    # start_hour_list = [0, 0, 0, 0, 0, 0, 0, 0, 2, 10, 18, 4, 2, 4, 19, 22, 54, 2, 0, 18, 18, 4, 0, 0]
    profile_start_date(x, start_hour_list, proc_name)


if __name__ == '__main__':
    # profile_proc('211.65.197.233', 'sshd')
    process_start_date = get_all_process2('211.65.197.233')
    for key in process_start_date:
        print(key)
        print(process_start_date[key])