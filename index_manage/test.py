from elasticsearch import Elasticsearch
import pymongo
import time

es=Elasticsearch("211.65.197.70")
mongo=pymongo.MongoClient("mongodb://211.65.197.70:27017")
hosts=["211.65.197.175","211.65.197.233","211.65.193.23"]
today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
db=mongo["anomaly"]

def updateShell(host):
    col = db['shell']
    idx = host + "-user-" + today.replace("-", ".")
    if es.indices.exists(index=idx):
        esData = es.search(index=idx, scroll='5m', timeout='3s', size=100)
        scroll_id = esData["_scroll_id"]
        total = esData['hits']['total']
        datas = esData['hits']['hits']

        for i in range((int)(total / 100)):
            res = es.scroll(scroll_id=scroll_id, scroll='5m')
            datas += res["hits"]["hits"]

        times = set()
        for x in col.find({"time": {'$regex': r"" + str(today) + ".*"}}):
            times.add(x["time"])
        print(times)
        items = 0
        for data in datas:
            print(data)
            if data['_source']['cmdTime'] not in times:
                d = dict()
                d['location'] = data['_source']['executeLocation']
                d['command'] = data['_source']['cmdLine']
                d['orderNum'] = data['_source']['orderNum']
                d['clientIP'] = data['_source']['clientIP']
                d['tags'] = data['_source']['tags']
                d['userCmd'] = data['_source']['userCmd']
                d['time'] = data['_source']['cmdTime']
                d['host'] = host
                # col.insert_one(d)
                items += 1
        print(host, "update shell", items, now)
    else:
        print(idx, "not exists", now)

for host in hosts:
    # updateAuth(host)
	# updateSysinfo(host)
	updateShell(host)
	# updatePinfo(host)
mongo.close()