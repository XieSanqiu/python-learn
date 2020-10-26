import pymongo

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")

my_collection = my_client['pinfo']['activity']

hosts = ['211.65.193.23', '211.65.197.175', '211.65.197.233']

all_proc = set()
for host in hosts:
    query = {'host_ip':host}
    results = my_collection.find(query)
    proc_set = set()
    for result in results:
        proc_name = result['proc_name']
        proc = proc_name
        proc_set.add(proc)
    file = host + '-process.txt'
    with open(file, 'w') as f:
        for proc in proc_set:
            f.write(proc+'\n')
    all_proc = all_proc | proc_set


with open('all_process.txt', 'w') as f:
    for proc in all_proc:
        f.write(proc + '\n')