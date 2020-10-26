# 计算每个进程的权重
import math

# 获取所有主机的进程集合
def get_process_set(file):
    process_set = set()
    with open(file, 'r') as f:
        for process in f.readlines():
            process_set.add(process.strip())
    return process_set

def get_weight(set1, set2, r):
    if len(set1) == 1 and len(set2) == 1:
        val1 = 0
    else:
        val1 = len(set1 & set2) / len(set1 | set2)
    val2 = 1 + math.e ** (r - min(len(set1), len(set2)))
    return val1 / val2

def calculate():
    # 从process.txt获得所有进程
    all_process = []
    with open('all_process.txt', 'r') as f:
        for process in f.readlines():
            all_process.append(process.strip())
    # print(all_process)

    # 得到每个进程所属主机的集合，使用dict存储
    process_host = dict()
    # hosts = ['23', '233', '175']
    set_23 = get_process_set('211.65.193.23-process.txt')
    set_233 = get_process_set('211.65.197.233-process.txt')
    set_175 = get_process_set('211.65.197.175-process.txt')
    for process in all_process:
        process_host[process] = set()
        if process in set_23:
            process_host[process].add('211.65.193.23')
        if process in set_233:
            process_host[process].add('211.65.197.233')
        if process in set_175:
            process_host[process].add('211.65.197.175')
        # print(process, process_host[process])

    # 计算p1-p2边的weight
    weight = dict()
    with open('process_weight.txt', 'w') as f:
        for i in range(len(all_process)):
            for j in range(i + 1, len(all_process)):
                p1 = all_process[i]
                p2 = all_process[j]
                # print(p1, p2)
                set1 = process_host[p1]
                set2 = process_host[p2]
                weight[p1+'->'+p2] = get_weight(set1, set2, 3)
                f.write(p1+'->'+p2 + ':' + str(weight[p1+'->'+p2]) + '\n')

    # 计算每个进程的权重
    process_weight = dict()
    for k, v in weight.items():
        pp = k.split('->')
        p1 = pp[0]
        p2 = pp[1]
        process_weight[p1] = process_weight.get(p1, 0) + v
        process_weight[p2] = process_weight.get(p2, 0) + v
    print(process_weight)
    result = sorted(process_weight.items(), key=lambda x: x[1], reverse=True)
    print(result)
    with open('weight_result.txt', 'w') as f:
        for kv in result:
            f.write(kv[0] + ':' + str(kv[1]) + '\n')

if __name__ == '__main__':
    calculate()