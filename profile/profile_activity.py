from elasticsearch import Elasticsearch
import time
import datetime
import numpy as np
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
def get_all_process(host, today, proc_name, pid):
    try:
        # es = Elasticsearch("211.65.197.70")
        idx = host + "-pinfo-" + today
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
                            },
                            {
                                "match": {
                                    "pid": pid
                                }
                            }
                        ],
                        "filter": {
                            "range": {
                                "collect_date": {
                                    "gte": "2021-03-16T01:32:12.046851",
                                    "lte": "2021-03-16T23:32:37.046851"
                                }
                            }
                        }
                    }
                },
                "sort": [
                    {
                        "@timestamp": {
                            "order": "asc"
                        }
                    }
                ],
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
                d['HostIP'] = data['_source']['HostIP']
                d['start_date'] = data['_source']['start_date']
                d['start_time'] = float(data['_source']['start_time'])
                d['proc_name'] = data['_source']['proc_name']
                d['user_name'] = data['_source']['user_name']
                d['collect_date'] = data['_source']['collect_date']
                if 'proc_param' in data['_source'].keys():
                    d['proc_param'] = data['_source']['proc_param']
                else:
                    d['proc_param'] = '-None'
                if 'proc_exe' in data['_source'].keys():
                    d['proc_exe'] = data['_source']['proc_exe']
                else:
                    d['proc_exe'] = 'kernel'

                d['cpu_percent'] = data['_source']['cpu_percent']
                d['cpu_user_time'] = data['_source']['cpu_user_time']
                d['cpu_sys_time'] = data['_source']['cpu_sys_time']

                d['mem_percent'] = data['_source']['mem_percent']
                d['mem_rss'] = data['_source']['mem_rss']
                d['mem_vms'] = data['_source']['mem_vms']

                d['read_count'] = data['_source']['read_count']
                d['write_count'] = data['_source']['write_count']
                d['read_byte'] = data['_source']['read_byte']
                d['write_byte'] = data['_source']['write_byte']
                d['disk_read_rate'] = data['_source']['disk_read_rate']
                d['disk_write_rate'] = data['_source']['disk_write_rate']

                d['connection_num'] = data['_source']['connection_num']
                d['file_num'] = data['_source']['file_num']
                d['fds'] = data['_source']['fds']

                d['threads'] = data['_source']['threads']

                d['ctx_sw_voluntary'] = data['_source']['ctx_sw_voluntary']
                d['ctx_sw_involuntary'] = data['_source']['ctx_sw_involuntary']

                print(d)
                dds.append(d)
        else:
            print(idx, "not exists")
        return dds
    except Exception as ee:
        print('get_all_process', ee)

#对进程CPU、内存使用画像
def profile1(data_x, data_y1, data_y2):
    # plt.figure(figsize=(8, 4), dpi=80)  # 设置图形大小，分辨率
    # plt.plot(data_x, data_y1,data_x, data_y2)
    # plt.ylabel('cpu_percent')
    # plt.xlabel('time(hour)')
    # plt.ylim(0, 100)
    # plt.show()

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # 做镜像处理
    ax1.plot(data_x, data_y1, 'g-', label='cpu_percent(%)')
    ax1.legend(loc='upper left')
    ax2.plot(data_x, data_y2, 'b-', label='memory_percent(%)')
    ax2.legend(loc='upper right')

    ax1.tick_params(axis='y', labelcolor='g')
    ax2.tick_params(axis='y', labelcolor='b')

    # ax1.set_ylim(50, 120)
    # ax2.set_ylim(0, 10)

    ax1.set_xlabel('time(hour)')  # 设置x轴标题
    ax1.set_ylabel('cpu_percent(%)', color='g')  # 设置Y1轴标题
    ax2.set_ylabel('memory_percent(%)', color='b')  # 设置Y2轴标题
    plt.show()

#对CPU使用时间画像（用户模式、内核模式）
def profile2(data_x, data_y1, data_y2):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # 做镜像处理
    ax1.plot(data_x, data_y1, 'g-', color='g', label='cpu_user_time(秒)')
    ax1.legend(loc='upper left')
    ax2.plot(data_x, data_y2, 'b-', color='b', label='cpu_sys_time(秒)')
    ax2.legend(loc='upper right')

    ax1.tick_params(axis='y', labelcolor='g')
    ax2.tick_params(axis='y', labelcolor='b')

    # ax1.set_ylim(5600000, 5800000)
    # ax2.set_ylim(228000, 240000)

    ax1.set_xlabel('time(hour)')  # 设置x轴标题
    ax1.set_ylabel('cpu_user_time(秒)', color='g')  # 设置Y1轴标题
    ax2.set_ylabel('cpu_sys_time(秒)', color='b')  # 设置Y2轴标题
    plt.show()

#对内存画像（物理内存、虚拟内存）
def profile3(data_x, data_y1, data_y2):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # 做镜像处理
    ax1.plot(data_x, data_y1, 'g-', label='mem_rss(byte)')
    ax1.legend(loc='upper left')
    ax2.plot(data_x, data_y2, 'b-', label='mem_vms(byte)')
    ax2.legend(loc='upper right')

    ax1.tick_params(axis='y', labelcolor='g')
    ax2.tick_params(axis='y', labelcolor='b')

    # ax1.set_ylim(650000000, 654000000)
    # ax2.set_ylim(4229287500, 4229288000)

    ax1.set_xlabel('time(hour)')  # 设置x轴标题
    ax1.set_ylabel('mem_rss(byte)', color='g')  # 设置Y1轴标题
    ax2.set_ylabel('mem_vms(byte)', color='b')  # 设置Y2轴标题
    plt.show()

#对磁盘读写次数画像
def profile4(data_x, data_y1, data_y2):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # 做镜像处理
    ax1.plot(data_x, data_y1, 'g-', label='read_count')
    ax1.legend(loc='upper left')
    ax2.plot(data_x, data_y2, 'b-', label='write_count')
    ax2.legend(loc='upper right')

    # ax1.set_ylim(7866000, 7880000)
    # ax2.set_ylim(217081000, 217085000)

    ax1.tick_params(axis='y', labelcolor='g')
    ax2.tick_params(axis='y', labelcolor='b')

    ax1.set_xlabel('time(hour)')  # 设置x轴标题
    ax1.set_ylabel('read_count', color='g')  # 设置Y1轴标题
    ax2.set_ylabel('write_count', color='b')  # 设置Y2轴标题
    plt.show()

#对磁盘读写字节数画像
def profile5(data_x, data_y1, data_y2):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # 做镜像处理
    ax1.plot(data_x, data_y1, 'g-', label='read_byte')
    ax1.legend(loc='upper left')
    ax2.plot(data_x, data_y2, 'b-', label='write_byte')
    ax2.legend(loc='upper right')

    ax1.tick_params(axis='y', labelcolor='g')
    ax2.tick_params(axis='y', labelcolor='b')

    # ax1.set_ylim(5894000000, 5900000000)
    # ax2.set_ylim(1275740000000, 1275814876800)

    ax1.set_xlabel('time(hour)')  # 设置x轴标题
    ax1.set_ylabel('read_byte', color='g')  # 设置Y1轴标题
    ax2.set_ylabel('write_byte', color='b')  # 设置Y2轴标题
    plt.show()

#对磁盘读写速度画像
def profile6(data_x, data_y1, data_y2):
    # plt.figure(figsize=(8, 4), dpi=80)  # 设置图形大小，分辨率
    plt.plot(data_x, data_y1, 'b-', label='disk read rate(kb/s)')
    plt.plot(data_x, data_y2, 'g-', label='disk write rate(kb/s)')
    plt.ylabel('kb/s')
    plt.xlabel('time(hour)')
    # plt.ylim(0, 50)
    plt.legend(loc='best')
    plt.show()

#对磁盘读写速度画像
def profile7(data_x, data_y1, data_y2, data_y3, data_y4):
    # plt.figure(figsize=(8, 4), dpi=80)  # 设置图形大小，分辨率
    plt.plot(data_x, data_y1, 'b-', label='connection num')
    plt.plot(data_x, data_y2, 'g-', label='file num')
    plt.plot(data_x, data_y3, 'r-', label='fds num')
    plt.plot(data_x, data_y4, 'y-', label='threads num')
    plt.xlabel('time(hour)')
    plt.legend(loc='upper right')
    plt.show()

#对磁盘读写字节数画像
def profile8(data_x, data_y1, data_y2):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()  # 做镜像处理
    ax1.plot(data_x, data_y1, 'g-', label='ctx_sw_voluntary')
    ax1.legend(loc='upper left')
    ax2.plot(data_x, data_y2, 'b-', label='ctx_sw_involuntary')
    ax2.legend(loc='best')

    ax1.tick_params(axis='y', labelcolor='g')
    ax2.tick_params(axis='y', labelcolor='b')

    # ax1.set_ylim(5894000000, 5900000000)
    # ax2.set_ylim(1275740000000, 1275814876800)

    ax1.set_xlabel('time(hour)')  # 设置x轴标题
    ax1.set_ylabel('ctx_sw_voluntary', color='g')  # 设置Y1轴标题
    ax2.set_ylabel('ctx_sw_involuntary', color='b')  # 设置Y2轴标题
    plt.show()

if __name__ == '__main__':
    dds = get_all_process('211.65.197.233', '2021.03.16', 'mysqld', 833)
    collect_time = []
    cpu_percent = []
    memory_percent = []
    cpu_user_time = []
    cpu_sys_time = []
    mem_rss = []
    mem_vms = []
    read_count = []
    write_count = []
    read_byte = []
    write_byte = []
    disk_read_rate = []
    disk_write_rate = []
    connection_num = []
    file_num = []
    fds = []
    threads = []
    ctx_sw_voluntary = []
    ctx_sw_involuntary = []
    for dd in dds:
        time = dd['collect_date'].split('T')[1].split(':')
        time = int(time[0]) + (int(time[1]) * 1/60)
        collect_time.append(time)

        cpu_percent.append(dd['cpu_percent'])
        memory_percent.append(dd['mem_percent'])

        cpu_user_time.append(dd['cpu_user_time'])
        cpu_sys_time.append(dd['cpu_sys_time'])

        mem_rss.append(dd['mem_rss'])
        mem_vms.append(dd['mem_vms'])

        read_count.append([dd['read_count']])
        write_count.append([dd['write_count']])

        read_byte.append(dd['read_byte'])
        write_byte.append(dd['write_byte'])

        disk_read_rate.append(dd['disk_read_rate'])
        disk_write_rate.append(dd['disk_write_rate'])

        connection_num.append(dd['connection_num'])
        file_num.append(dd['file_num'])
        fds.append(dd['fds'])
        threads.append(dd['threads'])

        ctx_sw_voluntary.append(dd['ctx_sw_voluntary'])
        ctx_sw_involuntary.append(dd['ctx_sw_involuntary'])


    profile1(collect_time, cpu_percent, memory_percent)
    profile2(collect_time, cpu_user_time, cpu_sys_time)
    profile3(collect_time, mem_rss, mem_vms)
    profile4(collect_time, read_count, write_count)
    profile5(collect_time, read_byte, write_byte)
    profile6(collect_time, disk_read_rate, disk_write_rate)
    profile7(collect_time, connection_num, file_num, fds, threads)
    profile8(collect_time, ctx_sw_voluntary, ctx_sw_involuntary)
