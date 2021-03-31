'''
获取初始概率π，状态转移矩阵A
'''

def get_all_calls(files):
    all_calls = []
    for file in files:
        with open(file) as f:
            for line in f.readlines():
                calls = line.strip().split(' ')[1:]
                all_calls.append(calls)
    return all_calls

def get_calls(file):
    all_calls = []
    with open(file) as f:
        for line in f.readlines():
            calls = line.strip().split(' ')[1:]
            all_calls.append(calls)
    return all_calls

# 获取所有系统调用以及他们出现的频率并返回
def get_calls_dict(files):
    calls_dict = {}
    count = 0
    for file in files:
        with open(file) as f:
            for line in f.readlines():
                calls = line.strip().split(' ')[1:]
                for call in calls:
                    count += 1
                    if call not in calls_dict:
                        calls_dict[call] = 1
                    else:
                        calls_dict[call] += 1
    for key in calls_dict:
        calls_dict[key] = calls_dict[key] / count

    return calls_dict

# 将概率低于阈值 other_thread 的系统调用合为 other
def get_new_calls_dict(old_calls_dict, other_thread):
    other = 0.0
    tmp_dict = old_calls_dict.copy()
    for key in tmp_dict:
        if old_calls_dict[key] <= other_thread:
            other += old_calls_dict[key]
            del old_calls_dict[key]
    old_calls_dict['others'] = other
    return old_calls_dict

# 获取状态转移矩阵A
def get_A_dict(calls_dict, files):
    A_dict = {}
    for file in files:
        with open(file) as f:
            for line in f.readlines():
                calls = line.strip().split(' ')[1:]
                for call, next_call in zip(calls[:-1], calls[1:]):
                    if call not in calls_dict:
                        call = 'others'
                    if next_call not in calls_dict:
                        next_call = 'others'
                    if call not in A_dict:
                        A_dict[call] = {}
                    if next_call not in A_dict[call]:
                        A_dict[call][next_call] = 1
                    else:
                        A_dict[call][next_call] += 1
    for key in A_dict:
        sum = 0
        for key_key in A_dict[key]:
            sum += A_dict[key][key_key]
        for key_key in A_dict[key]:
            A_dict[key][key_key] = A_dict[key][key_key] / sum
    return A_dict


if __name__ == '__main__':
    files = ['D:\毕业论文相关\数据集\sendmail-UNM\\normal\sendmail.log.txt']
    old_calls_dict = get_calls_dict(files)
    print(len(old_calls_dict), old_calls_dict)
    new_calls_dict = get_new_calls_dict(old_calls_dict, 0.001)
    print(len(new_calls_dict), new_calls_dict)

    get_A_dict(new_calls_dict, files)
