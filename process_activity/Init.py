'''
初始化进程活动信息
以 主机IP+进程名+进程id 为主键确定一次进程活动信息
其中后面需要更新的是 max_cpu、avg_cpu、max_memory、avg_memory
'''
import pymongo
from common.GetProcessInfo import query_by_index as es_query

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")

def init():
    hosts = ['211.65.193.23', '211.65.197.175', '211.65.197.233']
    today = '2020.10.15'
    my_collection = my_client['pinfo']['activity']
    count = 1
    for host in hosts:
        print('-------------------------' + host + '-------------------------')
        index = host + '-pinfo-' + today
        process_infos = es_query(index)
        for one in process_infos:
            proc_name = one['_source']['proc_name']
            proc_pid = one['_source']['pid']

            my_query = {"host_ip":host, "proc_name":proc_name, "proc_pid":proc_pid} #主机IP+进程名+进程id唯一确定一次进程活动
            doc_count = my_collection.count_documents(my_query)
            if doc_count == 0:
                mongo_one = es_2_mongodb_add(one)
                my_collection.insert_one(mongo_one)
                count += 1
                if count % 100 == 0:
                    print(count)

# 将es里的信息格式转为mongodb里的格式
def es_2_mongodb_add(es_one):
    mongo_one = dict()
    mongo_one['host_ip'] = es_one['_source']['HostIP']
    mongo_one['proc_name'] = es_one['_source']['proc_name']
    mongo_one['proc_pid'] = es_one['_source']['pid']
    mongo_one['start_time'] = es_one['_source']['start_time'] #时间戳
    mongo_one['update_time'] = es_one['_source']['start_time']
    mongo_one['user_name'] = es_one['_source']['user_name']
    mongo_one['proc_param'] = es_one['_source']['proc_param'] #进程启动参数

    mongo_one['max_cpu'] = es_one['_source']['cpu_percent']
    mongo_one['min_cpu'] = es_one['_source']['cpu_percent']
    mongo_one['avg_cpu'] = es_one['_source']['cpu_percent']

    mongo_one['max_memory'] = es_one['_source']['mem_percent']
    mongo_one['min_memory'] = es_one['_source']['mem_percent']
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


if __name__ == '__main__':
    init()
    # my_collection = my_client['pinfo']['activity']
    # my_query = {"proc_name": "apache2", "proc_pid": 3133}
    # doc_count = my_collection.count_documents(my_query)
    # print(doc_count)

    # 清空集合
    # x = my_collection.delete_many({})
    # print(x.deleted_count)