'''
用于一些测试
'''
import pymongo
from elasticsearch import Elasticsearch
import time
import datetime
from multiprocessing import Pool

def detect_process(host, from_time, to_time, today):
    try:
        print(host, from_time, to_time)
        es = Elasticsearch("211.65.197.70")
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
                }
            }
            esData = es.search(index=idx, scroll='5m', timeout='3s', body=es_query1)
            total = esData['hits']['total']
            print(host, total)
            return total > 0
        else:
            return False
    except Exception as ee:
        print('detect_process', ee)

# res = detect_process("211.65.197.233", "2021-03-06T07:30:06.365497", "2021-03-06T07:30:31.365497", "2021.03.06")

if __name__ == '__main__':
    try:
        hosts = ["211.65.197.175", "211.65.197.233", "211.65.193.23"]
        pool = Pool(3)
        for host in hosts:
            pool.apply_async(detect_process, args=(host,"2021-03-06T07:30:06.365497", "2021-03-06T07:30:31.365497", "2021.03.06"))
        print('Waiting for all subprocesses done...')
        pool.close()
        pool.join()
        print('All subprocesses done.')
    except Exception as ee:
        print('main', ee)