import pymongo
from common.GetProcessInfo import query_by_index as es_query

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")


# 将es里的信息格式转为mongodb里的格式
def es_2_mg(es_one):
    mongo_one = dict()
    mongo_one['host_ip'] = es_one['_source']['HostIP']
    mongo_one['proc_name'] = es_one['_source']['proc_name']
    mongo_one['proc_pid'] = es_one['_source']['pid']
    mongo_one['proc_ppid'] = es_one['_source']['ppid']
    mongo_one['start_time'] = es_one['_source']['start_time'] #时间戳
    mongo_one['user_name'] = es_one['_source']['user_name']
    if 'proc_param' in es_one['_source']:
        mongo_one['proc_param'] = es_one['_source']['proc_param'] #进程启动参数
    else:
        mongo_one['proc_param'] = '-None'  # es中没有进程启动参数，我们给他赋值

    mongo_one['max_cpu'] = es_one['_source']['cpu_percent']
    mongo_one['avg_cpu'] = es_one['_source']['cpu_percent']

    mongo_one['max_memory'] = es_one['_source']['mem_percent']
    mongo_one['avg_memory'] = es_one['_source']['mem_percent']

    sockets_num = es_one['_source']['connection_num'] #进程没有网络连接，则没有对应key
    if sockets_num != 0:
        mongo_one['sockets'] = es_one['_source']['connections'].split('pconn')[1:]
    else:
        mongo_one['sockets'] = list()

    mongo_one['read_count'] = es_one['_source']['read_count']
    mongo_one['write_count'] = es_one['_source']['write_count']
    mongo_one['read_byte'] = es_one['_source']['read_byte']
    mongo_one['write_byte'] = es_one['_source']['write_byte']

    files_num = es_one['_source']['file_num']
    if files_num != 0:
        mongo_one['files'] = es_one['_source']['open_files'].split('popenfile')[1:]
    else:
        mongo_one['files'] = list()

    mongo_one['threads_num'] = es_one['_source']['threads']
    mongo_one['terminal'] = es_one['_source']['terminal']

    return mongo_one