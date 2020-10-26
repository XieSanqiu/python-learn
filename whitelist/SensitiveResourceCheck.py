'''
敏感资源检查模块
'''

import pymongo

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")
my_collection = my_client['pinfo']['hosts']

# 检测是否使用敏感文件
def sensitive_file_check(host, use_file):
    query = {'$or':[{'host':'all'}, {'host':host}]}
    res = my_collection.find(query, {'_id':0, 'file_type':1, 'file_path':1})
    for re in res:
        if re['file_type'] == 'file' and re['file_path'] == use_file:
            return True
        elif re['file_type'] == 'dir':
            if use_file.startswith(re['file_path']):
                return True
    return False

def sensitive_cpu_and_memory_check(max_cpu, avg_cpu, max_memory, avg_memory):
    if max_cpu > 50 or avg_cpu > 30 or max_memory > 50 or avg_memory > 30:
        return True
    else:
        return False

if __name__ == '__main__':
    is_use = sensitive_file_check('123', '/var/log/audit/audit.log')
    print(is_use)