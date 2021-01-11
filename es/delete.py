from elasticsearch import Elasticsearch

# 建立连接
es = Elasticsearch(hosts="211.65.197.70", port=9200)

# 获取所有索引列表
# for index in es.indices.get('*'):
#   print(index)

# 删除索引
res = es.indices.delete('*pinfo-2020*')  # 删除索引
print(res)


