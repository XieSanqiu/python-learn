'''
从ES中获取进程资源使用信息、进程系统调用信息
'''

from elasticsearch import Elasticsearch

# 建立连接
es = Elasticsearch(hosts="211.65.197.70", port=9200)

def common_query(index, query_statement, all):
    # 查询结果，包括其他字段，scroll游标查询，5m游标查询的过期时间
    query = es.search(index=index, scroll='5m', body=query_statement)

    # es查询出的结果第一页
    results = query['hits']['hits']

    # es查询出的结果总量
    total = query['hits']['total']

    # 游标用于输出es查询出的所有结果
    scroll_id = query['_scroll_id']
    # 在发送查询请求的时候,就告诉ES需要使用游标,并定义每次返回数据量的大小
    # 定义一个list变量results用来存储数据结果,在代码中,可以另其为空list,即results=[],也可以先将返回结果
    # 的第一页存尽进来, 即results = query['hits']['hits']
    # 对于所有二级果数据写个分页加载到内存变量的循环
    if all:
        for i in range(0, int(total / 100) + 1):
            # scroll参数必须制定否则会报错
            query_scroll = es.scroll(scroll_id=scroll_id, scroll="5m")['hits']['hits']
            results += query_scroll
    return results

''' 
只根据 索引 查询进程信息 索引=IP+pinfo+date
'''
def query_by_index(index, size = 100, all = True):
    # 查询语句
    query = {
        "size": size
    }
    return common_query(index, query, all)


'''
根据 索引+进程名 查询进程信息 索引=IP+pinfo+date
'''
def query_by_index_process(index, proc_name, size = 100, all = True):
    # 查询语句
    query = {
        "query":{
            "term":{
                "proc_name": proc_name
            }
        },
        "size": size
    }
    return common_query(index, query, all)


'''
根据 索引+进程名+时间戳 查询进程信息，并根据时间戳从小到大排序 索引=IP+pinfo+date
'''
def query_by_index_process_timestamp(index, proc_name, timestamp, size = 100, all = True):
    # 查询语句
    query = {
        "query": {
            "bool":{
                "filter":{"range": {"start_time": {"gte": timestamp}}},
                "must":[{"term": {"proc_name": proc_name}}]
            }
        },
        "sort": [
            {
                "@timestamp": {
                    "order": "asc"
                }
            }
        ],
        "size": size
    }
    return common_query(index, query, all)


if __name__ == '__main__':
    # query_by_index('211.65.197.175-pinfo-2020.10.07')
    # results = query_by_index_process('211.65.197.175-pinfo-2020.10.07', 'init')
    results = query_by_index_process_timestamp('211.65.197.175-pinfo-2020.10.17', 'java', '1598515942', 1, False)

    for line in results:
        print(line)
        print(line['_source']['open_files'])
        connections = line['_source']['open_files'].split('popenfile')
        print(len(connections))
        for c in connections[1:]:
            print(c)