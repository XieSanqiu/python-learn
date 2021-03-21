from drain_log_parser import Drain

import matplotlib
from matplotlib import pyplot as plt
font = {
    'family':'SimHei',
    'weight':'bold',
    'size':12
}
matplotlib.rc("font", **font)  #解决中文乱码
matplotlib.rcParams['axes.unicode_minus'] =False  #解决负号显示乱码

#读取解析后的模版文件，获取模版是否异常
def template_result():
    tmpl_normal = dict()
    with open('Drain_result/233-auth.log_templates.csv', 'r') as f:
        for line in f.readlines()[1:]:
            fields = line.strip().split(',')
            temp = fields[1]
            normal = fields[3]
            tmpl_normal[temp] = normal
    return tmpl_normal

def profile(data_x1, data_x2, data_y1, data_y2):
    plt.figure(figsize=(10, 5), dpi=80)  # 设置图形大小，分辨率
    plt.plot(data_x1, data_y1, 'g-', label='匹配正常模版日志数')
    plt.plot(data_x2, data_y2, 'b-', label='匹配异常模版日志数')
    plt.ylabel('数量')
    plt.xlabel('time(hour)')
    # plt.ylim(0, 50)
    plt.legend(loc='upper left')

    plt.vlines(20.95, 0, 350, color='red')
    plt.text(20.95, 290, 'ssh暴力密码破解', fontsize=12)

    plt.vlines(21.38, 0, 350, color='red')
    plt.text(21.38, 270, '攻击结束', fontsize=12)

    plt.show()

if __name__ == '__main__':
    tmpl_normal = template_result()
    normal_hour_count_dict = {}
    abnormal_hour_count_dict = {}
    hour_list = []
    count_list = []
    with open('Drain_result/233-auth.log_structured.csv', 'r') as f:
        for line in f.readlines():
            fields = line.strip().split(',')
            date = fields[1]
            if date != '2021-03-20':
                continue
            time = fields[2]
            tmpl = fields[8]
            time_fields = time.split(':')
            hour = int(time_fields[0]) + (int(time_fields[1]) / 60)
            normal = tmpl_normal[tmpl]
            if normal == '0':
                if hour not in normal_hour_count_dict:
                    normal_hour_count_dict[hour] = 1
                else:
                    normal_hour_count_dict[hour] += 1
            elif normal == '1':
                if hour not in abnormal_hour_count_dict:
                    abnormal_hour_count_dict[hour] = 1
                else:
                    abnormal_hour_count_dict[hour] += 1
    # print(normal_hour_count_dict)
    # print(abnormal_hour_count_dict)
    normal_hour = list(normal_hour_count_dict.keys())
    normal_list = list(normal_hour_count_dict.values())
    abnormal_hour = list(abnormal_hour_count_dict.keys())
    abnormal_list = list(abnormal_hour_count_dict.values())
    print(len(normal_hour), len(normal_list))
    profile(normal_hour, abnormal_hour, normal_list, abnormal_list)