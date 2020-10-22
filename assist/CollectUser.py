'''
收集各个主机用户并保存到mongodb
passwd文件格式
    name:password:uid:gid:comment:home:shell
保存格式：
    host_ip、user、uid、gid、type、comment、home、shell
超级用户：root，uid=0
系统用户（伪用户）：uid 1-499
普通用户：uid 500-60000
'''

import pymongo

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")
my_collection = my_client['pinfo']['hosts']

def collect_user(host_ip):
    file = host_ip + '-passwd.txt'
    inserts = []
    with open(file, 'r') as f:
        for line in f.readlines():
            insert = dict()
            params = line.strip().split(':')
            insert['host_ip'] = host_ip
            insert['user'] = params[0]
            uid = int(params[2])
            insert['uid'] = uid
            insert['gid'] = int(params[3])
            insert['comment'] = params[4]
            insert['home'] = params[5]
            insert['shell'] = params[6]
            if uid == 0:
                type = 'super'
            elif uid >= 1 and uid <= 499:
                type = 'system'
            else:
                type = 'normal'
            insert['type'] = type
            print(insert)
            inserts.append(insert)
    my_collection.insert_many(inserts)

if __name__ == '__main__':
    host_ip = '211.65.197.233'
    collect_user(host_ip)
