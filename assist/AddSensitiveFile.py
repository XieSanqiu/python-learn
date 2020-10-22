'''
添加敏感文件到mongodb中
格式：所属主机、类型、文件或目录路径、描述
'''

import pymongo

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")
my_collection = my_client['pinfo']['hosts']

# 从文件中添加
def add_from_file(file_name):
    inserts = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            params = line.strip().split(' ')
            file_path = params[0]
            file_type = params[1]
            file_explain = params[2]
            add_one = {'host':'all', 'file_type':file_type, 'file_name':file_path, 'file_explain':file_explain}
            inserts.append(add_one)
    my_collection.insert_many(inserts)

# 后期通过配置添加
def add_from_config(host, file_type, file_path, file_explain):
    add_one = {'host': host, 'file_type': file_type, 'file_name': file_path, 'file_explain': file_explain}
    my_collection.insert_one(add_one)

if __name__ == '__main__':
    add_from_file('sensitive-files.txt')