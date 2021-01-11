#!/usr/bin/python3
# -*- coding:utf-8 -*-
from elasticsearch import Elasticsearch
import datetime
es = Elasticsearch([{'host':'211.65.197.70','port':9200}])

def getDeleteDate(days):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days)
        ddate = now - delta
        ddate = ddate.strftime("%Y.%m.%d")
        return ddate

hostIP=["211.65.197.175","211.65.193.23","211.65.197.233"]

#保留7天
logType1 = ["sysinfo","pinfo", "audit"]
for i in range(7,30):
    ddate=getDeleteDate(i)
    for host in hostIP:
        for log in logType1:
            index_name = host + "-" + log + "-"+ddate
            if es.indices.exists(index=index_name):
                es.indices.delete(index=index_name)
                print(index_name)
        index_name = "grokparsefailure-" + ddate + "-" + host
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            print(index_name)


#保留60天
logType2=["access_log","auth", "cron", "daemon", "error_log", "kern", "mail", "syslog", "user"]
for i in range(60,80):
    ddate=getDeleteDate(i)
    for host in hostIP:
        for log in logType2:
            index_name = host + "-" + log + "-"+ddate
            if es.indices.exists(index=index_name):
                print(index_name)
                es.indices.delete(index=index_name)

#保留3天
logType3 = [".monitoring-es-6", ".monitoring-kibana-6", ".watcher-history-7"]
for i in range(3, 30):
    ddate = getDeleteDate(i)
    for log in logType3:
        index_name = log + "-" + ddate
        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name)
            print(index_name)