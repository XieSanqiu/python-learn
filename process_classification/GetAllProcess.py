import pymongo

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")

my_collection = my_client['pinfo']['activity']

def get_all_process(host_ip):
    # 记录所有的进程集合  进程名+进程启动参数
    process = set()
    # Mongodb 查询数据
    my_query = {"host_ip": host_ip}
    results = my_collection.find(my_query)

    for one in results:
        proc_name = one['proc_name']
        if 'proc_param' in one:
            proc_param = one['proc_param']
        else:
            proc_param = '-None'
        p = (proc_name, proc_param)
        if p not in process:
            process.add(p)

    return process

if __name__ == '__main__':
    host_ip = '211.65.197.175'
    process = get_all_process(host_ip)
    print(len(process))
    for p in process:
        print(p)