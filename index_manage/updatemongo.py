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
	col=db['shell']
	idx=host+"-user-"+today.replace("-",".")
	if es.indices.exists(index=idx):
		esData = es.search(index=idx, scroll='5m', timeout='3s', size=100)
		scroll_id=esData["_scroll_id"]
		total=esData['hits']['total']
		datas=esData['hits']['hits']
		
		for i in range((int)(total/100)):
			res = es.scroll(scroll_id=scroll_id, scroll='5m')
			datas += res["hits"]["hits"]
		
		times=set()
		for x in col.find({"time":{'$regex':r""+str(today)+".*"}}):
			times.add(x["time"])
		items=0
		for data in datas:
			if data['_source']['cmdTime'] not in times:
				d=dict()
				d['location']=data['_source']['executeLocation']
				d['command']=data['_source']['cmdLine']
				d['orderNum']=data['_source']['orderNum']
				d['clientIP']=data['_source']['clientIP']
				d['tags']=data['_source']['tags']
				d['userCmd']=data['_source']['userCmd']
				d['time']=data['_source']['cmdTime']
				d['host']=host
				col.insert_one(d)
				items+=1
		print(host,"update shell",items,now)
	else:
		print(idx, "not exists",now)

def updateAuth(host):
	col=db['authinfo']
	idx=host+"-auth-"+today.replace("-",".")
	if es.indices.exists(index=idx):
		esData = es.search(index=idx, scroll='5m', timeout='3s', size=100)
		scroll_id=esData["_scroll_id"]
		total=esData['hits']['total']
		datas=esData['hits']['hits']
		
		for i in range((int)(total/100)):
			res = es.scroll(scroll_id=scroll_id, scroll='5m')
			datas += res["hits"]["hits"]
		
		times=set()
		for x in col.find({"time":{'$regex':r""+str(today)+".*"}}):
			times.add(x["time"])
		items=0
		for data in datas:
			if data['_source']['time'] not in times and 'CRON' not in data['_source']['program']:
				d=dict()
				d['tags']=data['_source']['tags']
				d['program']=data['_source']['program']
				if 'pid' in data['_source'].keys():
					d['pid']=data['_source']['pid']
				d['info']=data['_source']['info']
				d['type']=data['_source']['type']
				d['time']=data['_source']['time']
				d['host']=host
				col.insert_one(d)
				items+=1
		print(host,"update auth",items,now)
		
	else:
		print(idx, "not exists")
			
def updateSysinfo(host):
	col=db['sysinfo']
	idx=host+"-sysinfo-"+today.replace("-",".")
	if es.indices.exists(index=idx):
		esData = es.search(index=idx, scroll='5m', timeout='3s', size=100)
		scroll_id=esData["_scroll_id"]
		total=esData['hits']['total']
		datas=esData['hits']['hits']
		
		for i in range((int)(total/100)):
			res = es.scroll(scroll_id=scroll_id, scroll='5m')
			datas += res["hits"]["hits"]
		
		times=set()
		for x in col.find({"time":{'$regex':r""+str(today)+".*"}}):
			times.add(x["time"])
		items=0
		for data in datas:
			if data['_source']['cdate'] not in times and 'processNum' in data['_source'].keys():
				d=dict()
				d["processNum"]=data['_source']['processNum']
				d["ports"]=data['_source']['ports']
				d['byteRecv']=data['_source']['byteRecv']
				d['byteSent']=data['_source']['byteSent']
				d['packetRecv']=data['_source']['packetRecv']
				d['packetSent']=data['_source']['packetSent']
				d['readCount']=data['_source']['readCount']
				d['writeCount']=data['_source']['writeCount']
				d['readByte']=data['_source']['readByte']
				d['writeByte']=data['_source']['writeByte']
				d['cpuPercent']=data['_source']['cpuPercent']
				d['memPercent']=data['_source']['memPercent']
				d['diskPercent']=data['_source']['diskPercent']
				d['readTime']=data['_source']['readTime']
				d['writeTime']=data['_source']['writeTime']
				d["time"]=data["_source"]["cdate"]
				d['host']=host
				col.insert_one(d)
				items+=1
		print(host,"update sysinfo",items,now)
	else:
		print(idx, "not exists",now)

def updatePinfo(host):
	col=db['pinfo']
	idx=host+"-pinfo-"+today.replace("-",".")
	if es.indices.exists(index=idx):
		esData = es.search(index=idx, scroll='5m', timeout='3s', size=100)
		scroll_id=esData["_scroll_id"]
		total=esData['hits']['total']
		datas=esData['hits']['hits']
		
		for i in range((int)(total/100)):
			res = es.scroll(scroll_id=scroll_id, scroll='5m')
			datas += res["hits"]["hits"]
		
		times=set()
		for x in col.find({"c_date":{'$regex':r""+str(today)+".*"}}):
			times.add(x["c_date"])
		items=0
		for data in datas:
			if data['_source']['c_date'] not in times:
				d=dict()
				d['start_time']=data['_source']['start_time']
				d['proc_name']=data['_source']['proc_name']
				d['egid']=data['_source']['egid']
				d['sgid']=data['_source']['sgid']
				d['ctx_sw_voluntary']=data['_source']['ctx_sw_voluntary']
				d['write_byte']=data['_source']['write_byte']
				d['pid']=data['_source']['pid']
				d['ppid']=data['_source']['ppid']
				d['start_date']=data['_source']['start_date']
				d['fds']=data['_source']['fds']
				d['file_num']=data['_source']['file_num']
				d['cpu_sys_time']=data['_source']['cpu_sys_time']
				d['mem_vms']=data['_source']['mem_vms']
				d['terminal']=data['_source']['terminal']
				d['nice']=data['_source']['nice']
				if 'proc_command' in data['_source'].keys():
					d['proc_command']=data['_source']['proc_command']
				d['read_byte']=data['_source']['read_byte']
				d['ctx_sw_involuntary']=data['_source']['ctx_sw_involuntary']
				d['HostIP']=data['_source']['HostIP']
				d['threads']=data['_source']['threads']
				d['write_count']=data['_source']['write_count']
				d['suid']=data['_source']['suid']
				d['host_name']=data['_source']['host_name']
				d['mem_percent']=data['_source']['mem_percent']
				d['ruid']=data['_source']['ruid']
				d['host']=data['_source']['host']
				d['connection_num']=data['_source']['connection_num']
				d['c_date']=data['_source']['c_date']
				d['rgid']=data['_source']['rgid']
				if 'proc_param' in data['_source'].keys():
					d['proc_param']=data['_source']['proc_param']
				d['read_count']=data['_source']['read_count']
				d['proc_state']=data['_source']['proc_state']
				d['mem_rss']=data['_source']['mem_rss']
				if 'connections' in data['_source'].keys():
					d['connections']=data['_source']['connections']
				d['cpu_user_time']=data['_source']['cpu_user_time']
				d['user_name']=data['_source']['user_name']
				d['host']=data['_source']['host']
				d['cpu_percent']=data['_source']['cpu_percent']
				if 'environment' in data['_source'].keys():
					d['environment']=data['_source']['environment']
				col.insert_one(d)
				items+=1
		print(host,"update pinfo",items,now)
	else:
		print(idx, "not exists",now)
		
for host in hosts:
	updateAuth(host)
	updateSysinfo(host)
	updateShell(host)
	updatePinfo(host)
mongo.close()
	
	
