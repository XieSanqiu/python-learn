import pymongo
from elasticsearch import Elasticsearch
import time
import datetime

mongo=pymongo.MongoClient('mongodb://211.65.197.70:27017')
es=Elasticsearch("211.65.197.70")

db=mongo['pinfo']

col = db['record_time']

utcnow_iso = datetime.datetime.utcnow().isoformat()

hostIP=["211.65.197.175","211.65.193.23","211.65.197.233"]

# for host in hostIP:
#     info = {'type':'pinfo', 'host':host, 'last_time':utcnow_iso}
#     col.insert_one(info)

query1 = {
    "query":{
        "range":{
            "@timestamp":{
                "gt":"2021-01-11T04:58:37.964546"
            }
        }
    },
    "size": 100
}
# esData = es.search(index='211.65.197.175-pinfo-2021.01.11', scroll='5m', timeout='3s',body=query1)
# print(esData)

# {c_date:{"$gt":"2021-01-11 15:40:01"}}

def write1(host):
    file_name = host + '_syscall'
    with open(file_name, 'r') as f:
        dd = []
        for line in f.readlines():
            d = dict()
            fields = line.strip().split('\t')
            syscall_num = fields[0]
            syscall = fields[1]
            d['syscall_num'] = syscall_num
            d['syscall'] = syscall
            d['hostIP'] = host
            d['type'] = 'num2syscall'
            dd.append(d)
    col = db['syscall_help']
    col.insert_many(dd)
    print(dd)

def delete1():
    query2 = {'last_time':{"$gt":"2021-01-11T08:35:52.513004"}}
    col.delete_many(query2)

if __name__ == '__main__':
    # for host in hostIP:
    #     write1(host)
    delete1()