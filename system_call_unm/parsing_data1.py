'''
解析文件：sendmail-CERT目录中的文件
'''
import os
# 将calls中的文件转成dict
def parsing1(file_path):
    calls = []
    with open(file_path) as f:
        for line in f.readlines():
            calls.append(line.strip())
    return calls

# 以进程id为一次系统调用，将.int文件转成一行一次系统调用，第一列为进程id，后面为具体的系统调用序列
def parsing2(src_file, dst_file, calls):
    pid_calls = {}
    with open(src_file) as src:
        for line in src.readlines():
            line_split = line.strip().split(' ')
            pid = line_split[0]
            call_num = int(line_split[1])
            call = calls[call_num]
            if pid not in pid_calls:
                pid_calls[pid] = [call]
            else:
                pid_calls[pid].append(call)
    print(len(pid_calls))
    with open(dst_file, 'w', encoding='utf-8') as dst:
        for pid in pid_calls:
            dst.write(pid+' ')
            call_line = ' '.join(pid_calls[pid])
            dst.write(call_line + '\n')


if __name__ == '__main__':
    calls_path = 'C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\calls.txt'
    calls = parsing1(calls_path)
    # sm565a_path = 'C:\\Users\谢龙龙\Desktop\数据集\sendmail-CERT\cert-sm565a-1.int'
    # sm565a_path2 = 'C:\\Users\谢龙龙\Desktop\数据集\sendmail-CERT\cert-sm565a-1.txt'
    # src_path = 'C:\\Users\谢龙龙\Desktop\数据集\sendmail-CERT\cert-sm5x-1.int'
    # dst_path = 'C:\\Users\谢龙龙\Desktop\数据集\sendmail-CERT\cert-sm5x-1.txt'
    # src_path = 'C:\\Users\谢龙龙\Desktop\数据集\sendmail-CERT\sendmail.int'
    # dst_path = 'C:\\Users\谢龙龙\Desktop\数据集\sendmail-CERT\sendmail.txt'
    dir_path = 'C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM'
    for src_file in os.listdir(dir_path):
        if src_file.endswith('.int'):
            dst_file = dir_path + '\\' + src_file[:-3] + 'txt'
            src_file = dir_path + '\\' + src_file
            print(src_file, dst_file)
            parsing2(src_file, dst_file, calls)