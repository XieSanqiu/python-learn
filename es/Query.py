from elasticsearch import Elasticsearch

# 建立连接
es = Elasticsearch(hosts="211.65.197.70", port=9200)

# 查询语句
query1 = {
    "size": 100
}

# 查询结果，包括其他字段，scroll游标查询，5m游标查询的过期时间
query = es.search(index="test_index", scroll='5m', body=query1)
print('query:', query)

# 所需要的查询结果值
value = query["hits"]["hits"]
print('value:', value)

# es查询出的结果第一页
results = query['hits']['hits']
print('results:', results)

# es查询出的结果总量
total = query['hits']['total']
print('total:', total)

# 游标用于输出es查询出的所有结果
scroll_id = query['_scroll_id']
# 在发送查询请求的时候,就告诉ES需要使用游标,并定义每次返回数据量的大小
# 定义一个list变量results用来存储数据结果,在代码中,可以另其为空list,即results=[],也可以先将返回结果
# 的第一页存尽进来, 即results = query['hits']['hits']
# 对于所有二级果数据写个分页加载到内存变量的循环
for i in range(0, int(total / 100) + 1):
    # scroll参数必须制定否则会报错
    query_scroll = es.scroll(scroll_id=scroll_id, scroll="5m")['hits']['hits']
    results += query_scroll
print('results:', results)

