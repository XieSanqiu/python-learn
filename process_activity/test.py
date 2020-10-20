'''
用于一些测试
'''
import pymongo

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")

my_collection = my_client['pinfo']['activity']


# Mongodb 查询数据
# my_query = {"host_ip":"211.65.197.175", "proc_name": "sshd", "proc_param":"-None"}
# results = my_collection.find(my_query)
# for res in results:
#     print(res)

# 清空集合
x = my_collection.delete_many({})
print(x.deleted_count)

