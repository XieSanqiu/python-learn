# -*- coding: utf-8 -*-
import pymongo
from elasticsearch import Elasticsearch
import time
import datetime
from multiprocessing import Pool

es = Elasticsearch("211.65.197.70")

#探测一个时间范围 (from_time, to_time] 是否有进程信息
def detect_process(host, from_time, to_time, today):
    try:
        idx = host + "-pinfo-" + today
        if es.indices.exists(index=idx):
            es_query1 = {
                "query": {
                    "range": {
                        "@timestamp": {
                            "gte": from_time,
                            "lte": to_time
                        }
                    }
                },
                "size": 0
            }
            esData = es.search(index=idx, timeout='3s', body=es_query1)
            # print(esData)
            total = esData['hits']['total']
            # print(host, total, from_time, to_time, today, idx)
            return total > 0
        else:
            return False
    except Exception as ee:
        print('detect_process', ee)

def get_all_process(host, from_time, to_time, today):
    try:
        idx = host + "-pinfo-" + today
        dds = []
        if es.indices.exists(index=idx):
            es_query1 = {
                "query": {
                    "range": {
                        "@timestamp": {
                            "gte": from_time,
                            "lte": to_time
                        }
                    }
                },
                "size": 100
            }
            esData = es.search(index=idx, scroll='5m', timeout='5s', body=es_query1)
            scroll_id = esData["_scroll_id"]
            total = esData['hits']['total']
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
                d['disk_write_rate'] = data['_source']['disk_write_rate']
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
        return dds
    except Exception as ee:
        print('get_all_process', ee)

def process_activity(host):
    mongo = pymongo.MongoClient('mongodb://211.65.197.70:27017')
    db = mongo['pinfo']
    col = db['activity']
    while (True):
        try:
            today = time.strftime('%Y.%m.%d', time.localtime(time.time()))
            from_time = (datetime.datetime.utcnow() - datetime.timedelta(seconds=25)).isoformat()
            to_time = datetime.datetime.utcnow().isoformat()
            res = {}
            if detect_process(host, from_time, to_time, today):
                time.sleep(5)
                from_time = (datetime.datetime.utcnow() - datetime.timedelta(seconds=35)).isoformat()
                to_time = datetime.datetime.utcnow().isoformat()
                all_process = get_all_process(host, from_time, to_time, today)
                if len(all_process) == 0:
                    print('get all process is None')
                    continue
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
                        res[key]['disk_write_rate'] += proc['disk_write_rate']
                        res[key]['open_files'] |= proc['open_files']
                        res[key]['connections'] |= proc['connections']
                        res[key]['threads'] |= proc['threads']
                        res[key]['proc_num'] += 1
                    else:
                        res[key] = proc
                        res[key]['start_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(proc['start_time']))
                        res[key]['proc_num'] = 1

                current_time = time.time()
                current_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
                for app_key in res:
                    res[app_key]['open_files'] = list(res[app_key]['open_files'])
                    res[app_key]['files_num'] = len(res[app_key]['open_files'])
                    res[app_key]['connections'] = list(res[app_key]['connections'])
                    res[app_key]['connections_num'] = len(res[app_key]['connections'])
                    res[app_key]['collect_time'] = current_time
                    res[app_key]['collect_date'] = current_date
                #插入到mongodb
                if len(res.values()) == 0:
                    print('res.values is none')
                    continue
                col.insert_many(list(res.values()))
                with open('pa2.log', 'a') as f:
                    line = current_date + ' ' + host + ' ' + str(len(res)) +' '+ '条插入成功\n'
                    f.write(line)
                time.sleep(25)
            else:
                time.sleep(20)
        except Exception as e:
            print('process_activity', e)


if __name__ == '__main__':
    try:
        hosts = ["211.65.197.175", "211.65.197.233", "211.65.193.23"]
        # hosts = ["211.65.197.233"]
        pool = Pool(3) #线程池大小，跟主机数一致
        for host in hosts:
            pool.apply_async(process_activity, args=(host,))
        print('Waiting for all subprocesses done...')
        pool.close()
        pool.join()
        print('All subprocesses done.')
    except Exception as ee:
        print('main', ee)
