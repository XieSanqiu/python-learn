import pymongo
from elasticsearch import Elasticsearch
import time
import datetime

mongo=pymongo.MongoClient('mongodb://211.65.197.70:27017')
es=Elasticsearch("211.65.197.70")

hosts=["211.65.197.175","211.65.197.233","211.65.193.23"]
db=mongo['pinfo']

utcnow_iso = datetime.datetime.utcnow().isoformat()
today=time.strftime('%Y.%m.%d',time.localtime(time.time()))
now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def parsing_pinfo(host):
    col1 = db['record_time']
    col2 = db['resources']
    idx = host + "-pinfo-" + today
    mg_query1 = {'type':'pinfo', 'host':host}
    last_utcnow_iso = col1.find_one(mg_query1, {'_id':0, 'last_time':1})['last_time']
    print(last_utcnow_iso)

    if es.indices.exists(index=idx):
        es_query1 = {
            "query": {
                "range": {
                    "@timestamp": {
                        "gt": last_utcnow_iso
                    }
                }
            },
            "size": 100
        }
        esData = es.search(index=idx, scroll='5m', timeout='3s', body=es_query1)
        scroll_id = esData["_scroll_id"]
        total = esData['hits']['total']
        datas = esData['hits']['hits']

        for i in range((int)(total / 100)):
            res = es.scroll(scroll_id=scroll_id, scroll='5m')
            datas += res["hits"]["hits"]

        new_utcnow_iso = {'$set': {'last_time':utcnow_iso}}
        col1.update_one(mg_query1, new_utcnow_iso)

        items = 0
        dds = []
        for data in datas:
            d = dict()
            d['HostIP'] = data['_source']['HostIP']
            d['host_name'] = data['_source']['host_name']
            d['start_date'] = data['_source']['start_date']
            d['start_time'] = data['_source']['start_time']
            d['c_date'] = data['_source']['c_date']
            d['proc_name'] = data['_source']['proc_name']
            d['proc_state'] = data['_source']['proc_state']
            d['pid'] = data['_source']['pid']
            d['ppid'] = data['_source']['ppid']
            d['user_name'] = data['_source']['user_name']
            if 'proc_param' in data['_source'].keys():
                d['proc_param'] = data['_source']['proc_param']
            if 'proc_exe' in data['_source'].keys():
                d['proc_exe'] = data['_source']['proc_exe']
            if 'proc_command' in data['_source'].keys():
                d['proc_command'] = data['_source']['proc_command']
            d['terminal'] = data['_source']['terminal']

            d['cpu_percent'] = data['_source']['cpu_percent']
            d['cpu_user_time'] = data['_source']['cpu_user_time']
            d['cpu_sys_time'] = data['_source']['cpu_sys_time']
            d['mem_percent'] = data['_source']['mem_percent']
            d['mem_vms'] = data['_source']['mem_vms']
            d['mem_rss'] = data['_source']['mem_rss']
            d['read_byte'] = data['_source']['read_byte']

            d['write_byte'] = data['_source']['write_byte']
            d['write_count'] = data['_source']['write_count']
            d['read_byte'] = data['_source']['read_byte']
            d['read_count'] = data['_source']['read_count']
            d['fds'] = data['_source']['fds']
            d['file_num'] = data['_source']['file_num']
            if 'open_files' in data['_source'].keys():
                d['open_files'] = data['_source']['open_files']
            d['connection_num'] = data['_source']['connection_num']
            if 'connections' in data['_source'].keys():
                d['connections'] = data['_source']['connections']
            d['ctx_sw_voluntary'] = data['_source']['ctx_sw_voluntary']
            d['ctx_sw_involuntary'] = data['_source']['ctx_sw_involuntary']
            d['threads'] = data['_source']['threads']
            dds.append(d)
            items += 1
        if len(dds) > 0:
            col2.insert_many(dds)
        print(now, host, "update pinfo", items)
    else:
        print(now, idx, "not exists")

def paring_audit(host):
    col1 = db['record_time']
    col2 = db['syscall']
    col3 = db['syscall_help']
    idx = host + "-audit-" + today
    mg_query1 = {'type': 'audit', 'host': host}

    last_utcnow_iso = col1.find_one(mg_query1, {'_id': 0, 'last_time': 1})['last_time']
    print(last_utcnow_iso)

    if es.indices.exists(index=idx):
        es_query1 = {
            "query": {
                "bool" :{
                    "must": [
                        {
                            "match": {
                                "Action_type": "SYSCALL"
                            }
                        }
                    ],
                    "filter": {
                        "range": {
                            "@timestamp": {
                                "gt": last_utcnow_iso
                            }
                        },
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
        esData = es.search(index=idx, scroll='5m', timeout='3s', body=es_query1)
        scroll_id = esData["_scroll_id"]
        total = esData['hits']['total']
        datas = esData['hits']['hits']

        for i in range((int)(total / 100)):
            res = es.scroll(scroll_id=scroll_id, scroll='5m')
            datas += res["hits"]["hits"]

        new_utcnow_iso = {'$set': {'last_time': utcnow_iso}}
        print(new_utcnow_iso)
        # col1.update_one(mg_query1, new_utcnow_iso)
        #
        # mg_query2 = {'hostIP': host}
        # num2syscall = {}
        # res = col3.find(mg_query2, {'_id': 0, 'syscall_num': 1, 'syscall': 1})
        # for one in res:
        #     num2syscall[one['syscall_num']] = one['syscall']
        #
        # items = 0
        # dds = []
        # for data in datas:
        #     d = dict()
        #     d['hostIP'] = data['_source']['HostIP']
        #     d['collect_date'] = data['_source']['collect_date']
        #     d['timestamp'] = float(data['_source']['time'])
        #
        #     message = data['_source']['message']
        #     message_fields = message.split(' ')
        #
        #     for field in message_fields:
        #         if field.startswith('syscall'):
        #             syscall_num = field.split('=')[1]
        #             d['syscall_num'] = syscall_num
        #             try:
        #                 d['syscall'] = num2syscall[syscall_num]
        #             except KeyError:
        #                 d['syscall'] = 'None'
        #         elif field.startswith('pid'):
        #             d['pid'] = int(field.split('=')[1])
        #         elif field.startswith('exe'):
        #             d['exe'] = field.split('=')[1][1:-1]
        #         elif field.startswith('ses'):
        #             d['session'] = int(field.split('=')[1])
        #         elif field.startswith('uid'):
        #             uid = field.split('=')[1]
        #         elif field.startswith('suid'):
        #             suid = field.split('=')[1]
        #     dds.append(d)
        #     items += 1
        # if len(dds) > 0:
        #     col2.insert_many(dds)
        # print(now, host, "update audit", items)
    else:
        print(now, idx, "not exists")

def delete1(host):
    thirty_days_timestamp = time.time() - 30 * 24 * 60 * 60
    # thirty_days_timestamp = time.time() - 3 * 60 * 60
    thirty_days_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(thirty_days_timestamp))
    mg_query3 = {"HostIP":host, "c_date":{"$lte":thirty_days_date}}
    col = db['resources']
    num = col.delete_many(mg_query3).deleted_count
    print(now, host, "delete resource before", thirty_days_date, "total", num)

if __name__ == '__main__':
    # time.sleep(60)
    for host in hosts:
        #parsing_pinfo(host)
        paring_audit(host)
        #delete1(host)