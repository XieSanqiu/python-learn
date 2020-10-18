'''
每天运行一次，更新进程活动信息
连续统计一个月
'''

import pymongo
from common.GetProcessInfo import query_by_index as es_query
from process_activity.Init import es_2_mg

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")
pinfo_col = my_client['pinfo']['activity']

def update(yesterday):
    hosts = ['211.65.193.23', '211.65.197.175', '211.65.197.233']

    for host in hosts:
        print('-------------------------' + host + '-------------------------')
        index = host + '-pinfo-' + yesterday
        process_infos = es_query(index)
        rem = dict()
        for one in process_infos:
            # 主机IP+进程名+进程参数+进程id+进程启动时间 唯一确定一次进程活动
            proc_name = one['_source']['proc_name']
            try:
                proc_param = one['_source']['proc_param']
            except KeyError as e:
                proc_param = '-None'
                print('exception:', e)

            proc_pid = one['_source']['pid']
            start_time = one['_source']['start_time']

            key = (host, proc_name, proc_param, proc_pid, start_time)

            mg_one = es_2_mg(one)

            if key not in rem:
                rem[key] = mg_one
                rem[key]['cpu_count'] = 1
                rem[key]['memory_count'] = 1
            else:
                rem[key]['max_cpu'] = max(rem[key]['max_cpu'], one['_source']['cpu_percent'])
                rem[key]['avg_cpu'] = (rem[key]['avg_cpu'] * rem[key]['cpu_count'] + one['_source']['cpu_percent']) \
                                      / (rem[key]['cpu_count'] + 1)
                rem[key]['cpu_count'] += 1

                rem[key]['max_memory'] = max(rem[key]['max_memory'], one['_source']['mem_percent'])
                rem[key]['avg_memory'] = (rem[key]['avg_memory'] * rem[key]['memory_count'] + one['_source']['mem_percent']) \
                                         / (rem[key]['memory_count'] + 1)
                rem[key]['memory_count'] += 1

                if 'files' in mg_one:
                    if 'files' not in rem:
                        rem[key]['files'] = list()
                    for file in mg_one['files']:
                        if file not in rem[key]['files']:
                            rem[key]['files'].append(file)
                if 'sockets' in mg_one:
                    if 'sockets' not in rem:
                        rem[key]['sockets'] = list()
                    for socket in mg_one['sockets']:
                        if socket not in rem[key]['sockets']:
                            rem[key]['sockets'].append(socket)
        write_2_mg(rem)

'''
如果是新的进程，则加入
否则 更新：max_cpu、avg_cpu、max_memory、avg_memory、sockets、files、cpu_count、memory_count、read_count、read_byte、write_count、write_byte
'''
def write_2_mg(rem):
    for key in rem:
        query_dict = dict()
        query_dict['host_ip'] = key[0]
        query_dict['proc_name'] = key[1]
        query_dict['proc_param'] = key[2]
        query_dict['proc_pid'] = key[3]
        query_dict['start_time'] = key[4]

        mg_one = pinfo_col.find_one(query_dict)
        rem_one = rem[key]

        if mg_one == None:
            pinfo_col.insert_one(rem[key])
        else:
            update_dict = dict()
            max_cpu = max(mg_one['max_cpu'], rem_one['max_cpu'])
            cpu_count = mg_one['cpu_count'] + rem_one['cpu_count']
            avg_cpu = (mg_one['avg_cpu'] * mg_one['cpu_count'] + rem_one['avg_cpu'] * rem_one['cpu_count']) / cpu_count
            update_dict['max_cpu'] = max_cpu
            update_dict['avg_cpu'] = avg_cpu
            update_dict['cpu_count'] = cpu_count

            max_memory = max(mg_one['max_memory'], rem_one['max_memory'])
            memory_count = mg_one['memory_count'] + rem_one['memory_count']
            avg_memory = (mg_one['avg_memory'] * mg_one['memory_count'] + rem_one['avg_memory'] * rem_one['memory_count']) / memory_count
            update_dict['max_memory'] = max_memory
            update_dict['avg_memory'] = avg_memory
            update_dict['memory_count'] = memory_count

            files = list()
            if 'files' in mg_one:
                files = mg_one['files']
            if 'files' in rem_one:
                for file in rem_one['files']:
                    if file not in files:
                        files.append(file)
            update_dict['files'] = files

            sockets = list()
            if 'sockets' in mg_one:
                sockets = mg_one['sockets']
            if 'sockets' in rem_one:
                for soc in rem_one['sockets']:
                    if soc not in sockets:
                        sockets.append(soc)
            update_dict['sockets'] = sockets

            read_count = max(mg_one['read_count'], rem_one['read_count'])
            write_count = max(mg_one['write_count'], rem_one['write_count'])
            read_byte = max(mg_one['read_byte'], rem_one['read_byte'])
            write_byte = max(mg_one['write_byte'], rem_one['write_byte'])
            update_dict['read_count'] = read_count
            update_dict['write_count'] = write_count
            update_dict['read_byte'] = read_byte
            update_dict['write_byte'] = write_byte

            new_values = {'$set':update_dict}
            pinfo_col.update_one(query_dict, new_values)



if __name__ == '__main__':
    yesterday = '2020.10.17'
    update(yesterday)
