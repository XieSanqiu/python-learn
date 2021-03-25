import pymongo
from elasticsearch import Elasticsearch
import time, datetime

es=Elasticsearch("211.65.197.70")
today=time.strftime('%Y.%m.%d',time.localtime(time.time()))


def test1():
    mongo = pymongo.MongoClient("mongodb://211.65.197.70:27017")
    record_time_col = mongo['pinfo']['record_time']
    #record_time_col.insert_one({'type':'collect_rate', 'host':'211.65.197.175', 'rate':300})
    query1 = {'type':'collect_rate', 'host':'211.65.197.175'}
    x = record_time_col.find_one(query1, {'_id':0, 'rate':1})['rate']
    print(x)

def exception_test():
    x = 0
    try:
        y = 10 / x
    except ZeroDivisionError as ee:
        print('211 ', ee)
    print('dfdf')

def detect_process(host, from_time, to_time):
    idx = host + "-pinfo-" + today
    total = 0
    if es.indices.exists(index=idx):
        es_query1 = {
            "query": {
                "range": {
                    "@timestamp": {
                        "gt": from_time,
                        "lte": to_time
                    }
                }
            }
        }
        esData = es.search(index=idx, scroll='5m', timeout='3s', body=es_query1)
        total = esData['hits']['total']
    print(total)
    return total > 0

def get_all_process(host, from_time, to_time):
    idx = host + "-pinfo-" + today
    if es.indices.exists(index=idx):
        es_query1 = {
            "query": {
                "range": {
                    "@timestamp": {
                        "gt": from_time,
                        "lte": to_time
                    }
                }
            },
            "size": 100
        }
        esData = es.search(index=idx, scroll='5m', timeout='10s', body=es_query1)
        scroll_id = esData["_scroll_id"]
        total = esData['hits']['total']
        datas = esData['hits']['hits']
        print(datas)

        for i in range((int)(total / 100)):
            res = es.scroll(scroll_id=scroll_id, scroll='5m')
            datas += res["hits"]["hits"]
        dds = []
        for data in datas:
            d = dict()
            d['HostIP'] = data['_source']['HostIP']
            d['start_date'] = data['_source']['start_date']
            d['start_time'] = float(data['_source']['start_time'])
            d['proc_name'] = data['_source']['proc_name']
            d['user_name'] = data['_source']['user_name']
            if 'proc_param' in data['_source'].keys():
                d['proc_param'] = data['_source']['proc_param']
            else:
                d['proc_param'] = '-None'
            if 'proc_exe' in data['_source'].keys():
                d['proc_exe'] = data['_source']['proc_exe']
            else:
                d['proc_exe'] = 'kernel'
            d['cpu_percent'] = data['_source']['cpu_percent']
            d['mem_percent'] = data['_source']['mem_percent']
            d['disk_read_rate'] = data['_source']['disk_read_rate']
            d['disk_write_rate_result'] = data['_source']['disk_write_rate_result']
            if 'open_files' in data['_source'].keys():
                d['open_files'] = set(data['_source']['open_files'].split('popenfile')[1:])
            else:
                d['open_files'] = set()
            if 'connections' in data['_source'].keys():
                d['connections'] = set(data['_source']['connections'].split('pconn')[1:])
            else:
                d['connections'] = set()
            d['threads'] = data['_source']['threads']
            dds.append(d)
    else:
        print(idx, "not exists")
    print('len', len(dds))
    return dds


if __name__ == '__main__':
    mongo = pymongo.MongoClient('mongodb://211.65.197.70:27017')
    db = mongo['pinfo']
    col = db['activity']
    while(True):
        from_time = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(time.time()-8*60*60-25))
        to_time = time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(time.time()-8*60*60))
        res = {}
        print("bool", detect_process('211.65.197.233', from_time, to_time))
        if detect_process('211.65.197.233', from_time, to_time):
            time.sleep(5)
            from_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time() - 8 * 60 * 60 - 30))
            to_time = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time() - 8 * 60 * 60))
            all_process = get_all_process('211.65.197.233', from_time, to_time)
            for proc in all_process:
                key = (proc['HostIP'], proc['proc_exe'], proc['proc_param'])
                if key in res:
                    if proc['start_time'] < res[key]['start_time']:
                        res[key]['start_time'] = proc['start_time']
                        res[key]['start_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(proc['start_time']))
                        res[key]['user_name'] = proc['user_name']
                    res[key]['cpu_percent'] += proc['cpu_percent']
                    res[key]['mem_percent'] += proc['mem_percent']
                    res[key]['disk_read_rate'] += proc['disk_read_rate']
                    res[key]['disk_write_rate_result'] += proc['disk_write_rate_result']
                    res[key]['open_files'] |= proc['open_files']
                    res[key]['connections'] |= proc['connections']
                    res[key]['threads'] |= proc['threads']
                    res[key]['proc_num'] += 1
                else:
                    res[key] = proc
                    res[key]['start_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(proc['start_time']))
                    res[key]['proc_num'] = 1
            for app_key in res:
                res[app_key]['files_num'] = len(res[app_key]['open_files'])
                res[app_key]['connections_num'] = len(res[app_key]['connections'])
            print(res.values())
            print(len(res), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            time.sleep(25)
        else:
            time.sleep(20)