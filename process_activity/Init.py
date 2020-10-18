'''
初始化进程活动信息
以 主机IP+进程名+进程参数+进程id+进程启动时间 为主键确定一次进程活动信息
其中后面需要更新的是 max_cpu、avg_cpu、max_memory、avg_memory
'''
import pymongo
from common.GetProcessInfo import query_by_index as es_query
import math

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")

def init():
    hosts = ['211.65.193.23', '211.65.197.175', '211.65.197.233']
    today = '2020.10.15'

    for host in hosts:
        print('-------------------------' + host + '-------------------------')
        index = host + '-pinfo-' + today
        process_infos = es_query(index)
        rem = dict()
        for one in process_infos:
            # 主机IP+进程名+进程参数+进程id+进程启动时间 唯一确定一次进程活动
            proc_name = one['_source']['proc_name']
            proc_param = one['_source']['proc_param']
            proc_pid = one['_source']['pid']
            start_time = one['_source']['start_time']

            key = (host, proc_name, proc_param, proc_pid, start_time)

            mg_one = es_2_mg(one)

            if key not in rem:
                rem[key] = mg_one
                rem[key]['cpu_count'] = 1
                rem[key]['memory_count'] = 1
            else:
                rem[key]['max_cpu'] = max(rem[key]['max_cpu'], one['_source']['cpu_percent'])
                rem[key]['avg_cpu'] = (rem[key]['avg_cpu'] * rem[key]['cpu_count'] + one['_source']['cpu_percent']) \
                                      / (rem[key]['cpu_count'] + 1)
                rem[key]['cpu_count'] += 1

                rem[key]['max_memory'] = max(rem[key]['max_memory'], one['_source']['mem_percent'])
                rem[key]['avg_memory'] = (rem[key]['avg_memory'] * rem[key]['memory_count'] + one['_source']['mem_percent']) \
                                         / (rem[key]['memory_count'] + 1)
                rem[key]['memory_count'] += 1

                if 'files' in mg_one:
                    if 'files' not in rem:
                        rem[key]['files'] = list()
                    for file in mg_one['files']:
                        if file not in rem[key]['files']:
                            rem[key]['files'].append(file)
                if 'sockets' in mg_one:
                    if 'sockets' not in rem:
                        rem[key]['sockets'] = list()
                    for socket in mg_one['sockets']:
                        if socket not in rem[key]['sockets']:
                            rem[key]['sockets'].append(socket)
        write_2_mongodb(rem)


# 将es里的信息格式转为mongodb里的格式
def es_2_mg(es_one):
    mongo_one = dict()
    mongo_one['host_ip'] = es_one['_source']['HostIP']
    mongo_one['proc_name'] = es_one['_source']['proc_name']
    mongo_one['proc_pid'] = es_one['_source']['pid']
    mongo_one['start_time'] = es_one['_source']['start_time'] #时间戳
    mongo_one['user_name'] = es_one['_source']['user_name']
    if 'proc_param' in es_one['_source']:
        mongo_one['proc_param'] = es_one['_source']['proc_param'] #进程启动参数


    mongo_one['max_cpu'] = es_one['_source']['cpu_percent']
    mongo_one['avg_cpu'] = es_one['_source']['cpu_percent']

    mongo_one['max_memory'] = es_one['_source']['mem_percent']
    mongo_one['avg_memory'] = es_one['_source']['mem_percent']

    sockets_num = es_one['_source']['connection_num'] #进程没有网络连接，则没有对应key
    if sockets_num != 0:
        mongo_one['sockets'] = es_one['_source']['connections'].split('pconn')[1:]

    mongo_one['read_count'] = es_one['_source']['read_count']
    mongo_one['write_count'] = es_one['_source']['write_count']
    mongo_one['read_byte'] = es_one['_source']['read_byte']
    mongo_one['write_byte'] = es_one['_source']['write_byte']

    files_num = es_one['_source']['file_num']
    if files_num != 0:
        mongo_one['files'] = es_one['_source']['open_files'].split('popenfile')[1:]

    mongo_one['threads_num'] = es_one['_source']['threads']
    mongo_one['terminal'] = es_one['_source']['terminal']

    return mongo_one

def write_2_mongodb(rem):
    my_collection = my_client['pinfo']['activity']
    for one in rem:
        my_collection.insert_one(rem[one])

if __name__ == '__main__':
    init()
