'''
异常检测
'''
# 计算一次系统调用各个窗口内的概率
def cal_prob(calls, calls_dict, A_dict, win_len):
    res = []
    for i in range(len(calls)-win_len+1):
        one = 1.0
        pre_call = None
        for j in range(win_len):
            call = calls[i+j]
            if call not in calls_dict:
                call = 'others'
            if j == 0:
                one *= calls_dict[call]
                pre_call = call
            else:
                if pre_call in A_dict and call in A_dict[pre_call]:
                    one *= A_dict[pre_call][call]
                else:
                    one *= 0
                pre_call = call
        res.append(one)
    return res


