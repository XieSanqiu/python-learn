'''
白名单创建
字段：[合法用户列表、最高CPU使用率、最高内存使用率、最高磁盘读速度、最高磁盘写速度、合法网络连接、合法打开文件、最高相关进程数、是否可以构建孤立森林]
白名单作用：
1、只有白名单里的进程才通过使用孤立森林进行异常检测
2、每个进入白名单的进程都记录其合法的进程信息，用于不能使用孤立森林算法进行异常检测时，使用临界资源进行检测
    [合法用户列表、最高CPU使用率、最高内存使用率、最高磁盘读速度、最高磁盘写速度、合法网络连接、合法打开文件、最高相关进程数]
'''
import pymongo, time

class Whitelist:
    def __init__(self):
        self.mongo = pymongo.MongoClient('mongodb://211.65.197.70:27017')
        self.db = self.mongo['pinfo']
        self.activity_col = self.db['activity']
        self.whitelist_col = self.db['whitelist']

    #初步性的将所有进程加入白名单
    def add_process(self):
        query = {'collect_time': {'$gt': 1615645223}}
        all_processes = self.activity_col.find(query)
        all_processes_dict = dict()
        for one in all_processes:
            host_ip = one['HostIP']
            proc_exe = one['proc_exe']
            proc_param = one['proc_param'].strip()
            if len(proc_param) == 0:
                proc_param = '-None'
            proc_name = one['proc_name']
            user_name_set = set()
            user_name = one['user_name']
            user_name_set.add(user_name)
            cpu_percent = one['cpu_percent']
            mem_percent = one['mem_percent']
            disk_read_rate = one['disk_read_rate']
            disk_write_rate = one['disk_write_rate_result']
            connections = one['connections']
            connections_set = set()
            if len(connections) > 0:
                for con in connections:
                    laddr = ''
                    if len(con[3]) > 0:
                        laddr = con[3][0] + ':' + str(con[3][1])
                    raddr = ''
                    if len(con[4]) > 0:
                        raddr = con[4][0] + ':' + str(con[4][1])
                    con = laddr + ',' + raddr
                    if con != ',':
                        connections_set.add(con)
            open_files_set = set()
            open_files = one['open_files']
            if len(open_files) > 0:
                for file in open_files:
                    fi = file[0]
                    open_files_set.add(fi)

            key = (host_ip, proc_exe, proc_param)
            if key not in all_processes_dict:
                all_processes_dict[key] = [host_ip, proc_exe, proc_param, proc_name, user_name_set, cpu_percent, mem_percent,
                                           disk_read_rate, disk_write_rate, connections_set, open_files_set, 1]
            else:
                if user_name not in all_processes_dict[key][4]:
                    all_processes_dict[key][4].add(user_name)
                if cpu_percent > all_processes_dict[key][5]:
                    all_processes_dict[key][5] = cpu_percent
                if mem_percent > all_processes_dict[key][6]:
                    all_processes_dict[key][6] = mem_percent
                if disk_read_rate > all_processes_dict[key][7]:
                    all_processes_dict[key][7] = disk_read_rate
                if disk_write_rate > all_processes_dict[key][8]:
                    all_processes_dict[key][8] = disk_write_rate
                all_processes_dict[key][9] |= connections_set
                all_processes_dict[key][10] |= open_files_set
                all_processes_dict[key][11] += 1
        print(all_processes_dict)
        insert_many = []
        for key in all_processes_dict:
            insert_one = dict()
            insert_one['HostIP'] = all_processes_dict[key][0]
            insert_one['proc_exe'] = all_processes_dict[key][1]
            insert_one['proc_param'] = all_processes_dict[key][2]
            insert_one['proc_name'] = all_processes_dict[key][3]
            insert_one['user_name'] = list(all_processes_dict[key][4])
            insert_one['cpu_percent'] = all_processes_dict[key][5]
            insert_one['mem_percent'] = all_processes_dict[key][6]
            insert_one['disk_read_rate'] = all_processes_dict[key][7]
            insert_one['disk_write_rate_result'] = all_processes_dict[key][8]
            insert_one['connections_set'] = list(all_processes_dict[key][9])
            insert_one['open_files_set'] = list(all_processes_dict[key][10])
            insert_one['activity_num'] = all_processes_dict[key][11]
            insert_many.append(insert_one)
        self.whitelist_col.insert_many(insert_many)

if __name__ == '__main__':
    white = Whitelist()
    white.add_process()