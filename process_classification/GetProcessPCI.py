'''
获取进程活动信息
'''
import pymongo
from process_classification import GetAllProcess

my_client = pymongo.MongoClient("mongodb://211.65.197.70:27017/")
my_collection = my_client['pinfo']['activity']

hosts_collection = my_client['pinfo']['hosts']


def get_process_pci(host_ip, proc_name, proc_param):
    pci = dict()
    my_query = {'host_ip': host_ip, 'proc_name':proc_name, 'proc_param':proc_param}
    results = my_collection.find(my_query)

    proc_ppid = set() #进程父进程 ppid 集合
    proc_user = set() # 进程所属用户

    max_cpu = 0 # 进程最大cpu使用率
    max_memory = 0 # 进程最大内存使用率
    total_cpu = 0
    total_memory = 0

    read_count = 0
    read_byte = 0
    write_count = 0
    write_byte = 0

    sockets = set()
    files = set()

    threads_num = 0

    terminal = set()

    record_count = 0 # 被记录次数
    activity_count = 0 # 活动次数

    for res in results:
        proc_ppid.add(res['proc_ppid'])
        proc_user.add(res['user_name'])

        max_cpu = max(max_cpu, res['max_cpu'])
        total_cpu += res['avg_cpu']
        total_memory += res['avg_memory']
        max_memory = max(max_memory, res['max_memory'])

        read_count = max(read_count, res['read_count'])
        read_byte = max(read_byte, res['read_byte'])
        write_count = max(write_count, res['write_count'])
        write_byte = max(write_byte, res['write_byte'])

        # "(fd=8, family=10, type=1, laddr=('::ffff:211.65.197.175', 52340), raddr=('::ffff:211.65.197.175', 3306), status='ESTABLISHED'), ",
        for socket in res['sockets']:
            ss = socket.split(', ')
            family = ss[1]
            type = ss[2]
            laddr = ss[3] + ':' + ss[4]
            if ss[5] == 'raddr=()':
                raddr = ss[5]
            else:
                raddr = ss[5] + ':' + ss[6]
            new_socket = (family, type, laddr, raddr)
            sockets.add(new_socket)

        # (path='/var/log/apache2/other_vhosts_access.log', fd=7),
        # (path='/var/log/httpd/error_log', fd=2, position=344, mode='a', flags=558081),
        for file in res['files']:
            file_path = file.split(',')[0]
            files.add(file_path)

        threads_num = max(threads_num, res['threads_num'])

        terminal.add(res['terminal'])

        record_count += res['count']
        activity_count += 1
    avg_cpu = total_cpu / activity_count # 进程平均cpu使用率
    avg_memory = total_memory / activity_count # 进程平均内存使用率

    pci['proc_ppid'] = proc_ppid
    pci['proc_user'] = convert_user_2_int(host_ip, proc_user.pop())
    pci['max_cpu'] = max_cpu
    pci['avg_cpu'] = avg_cpu
    pci['max_memory'] = max_memory
    pci['avg_memory'] = avg_memory
    pci['read_count'] = read_count
    pci['read_byte'] = read_byte
    pci['write_count'] = write_count
    pci['write_byte'] = write_byte
    pci['sockets_num'] = len(sockets)
    pci['files_num'] = len(files)
    pci['threads_num'] = threads_num
    pci['terminal'] = terminal
    pci['collect_rate'] = record_count / (5 * 24 * 12)  # 收集率
    pci['activity_rate'] = activity_count / record_count # 活动比
    return pci

def convert_user_2_int(host_ip, user):
    query = {'host_ip':host_ip, 'user':user}
    result = hosts_collection.find_one(query)
    if result['type'] == 'super':
        return 0
    elif result['type'] == 'normal':
        return 1000
    elif result['type'] == 'system':
        return 100
    else:
        return -1

if __name__ == '__main__':
    # host_ip = '211.65.197.175'
    # host_ip = '211.65.193.23'
    host_ip = '211.65.197.233'
    processes = GetAllProcess.get_all_process(host_ip)

    num = 0
    file = host_ip + '-pdt.txt'
    with open(file, 'w') as f:
        for proc in processes:
            pci = get_process_pci(host_ip, proc[0], proc[1])
            if 'None' in pci['terminal']:
                pci['terminal'].remove('None')
            if len(pci['terminal']) >= 1:  # 有终端的都为交互进程
                continue
            if 2 not in pci['proc_ppid'] and proc[0] not in ['init', 'kthreadd']:  # 父进程id为2的都为内核进程
                num += 1
                print(num, proc[0], proc[1])
                line = str([pci['proc_user'], pci['max_cpu'], pci['avg_cpu'], pci['max_memory'], pci['avg_memory'], pci['read_count'],
                            pci['read_byte'], pci['write_count'], pci['write_byte'], pci['sockets_num'], pci['files_num'], pci['threads_num'],
                            pci['collect_rate'], pci['activity_rate']])[1:-1] + '\n'
                f.write(line)
