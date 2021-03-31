from system_call_unm import anomaly_detection, construct_hmm

def train(files, calls_dict, A_dict, win_len):
    all_calls = construct_hmm.get_all_calls(files)
    threshold = 1
    for calls in all_calls:
        one_res = anomaly_detection.cal_prob(calls, calls_dict, A_dict, win_len)
        threshold = min(min(one_res), threshold)

    # print('threshold:', threshold)

    return threshold

def detection(files, threshold, calls_dict, A_dict, win_len, ratio_threshold):
    for file in files:
        all_calls = construct_hmm.get_calls(file)
        # print('calls_len:', len(all_calls))
        detect_true = 0
        detect_false = 0
        total_detect = len(all_calls)
        for calls in all_calls:
            count = 0
            one_res = anomaly_detection.cal_prob(calls, calls_dict, A_dict, win_len)
            # print(one_res)
            for pro in one_res:
                if pro < threshold:
                    count += 1

            # print(len(one_res), count)
            if (count / len(one_res)) > ratio_threshold:
                detect_true += 1
            else:
                detect_false += 1
        print(file, 'TP:', detect_true / total_detect)
        print(file, 'TN:', detect_false / total_detect)



if __name__ == '__main__':
    files = ['D:\毕业论文相关\数据集\sendmail-UNM\\normal\sendmail.log.txt']
    # files = ['C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\sendmail.log.txt']
    other_threshold = 0.01
    win_len = 6
    old_calls_dict = construct_hmm.get_calls_dict(files)
    new_calls_dict = construct_hmm.get_new_calls_dict(old_calls_dict, other_threshold)
    # print('new_calls_dict', len(new_calls_dict), new_calls_dict)
    A_dict = construct_hmm.get_A_dict(new_calls_dict, files)
    print('A_dict', A_dict)
    for d in A_dict:
        print(d)
        print(dict(sorted(A_dict[d].items(), key=lambda x: x[1], reverse=True)))

    threshold = train(files,new_calls_dict, A_dict, win_len)

    # detection_files = ['C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\\sscp-sm-10763.txt','C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\\sscp-sm-10801.txt', 'C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\\sscp-sm-10814.txt']
    # detection_files = ['C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\\decode-sm-280.txt','C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\\decode-sm-314.txt']
    # detection_files = ['C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\\fwd-loops-1.txt','C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\\fwd-loops-2.txt',
    #                    'C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\\fwd-loops-3.txt','C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\\fwd-loops-4.txt',
    #                    'C:\\Users\谢龙龙\Desktop\数据集\sendmail-UNM\\fwd-loops-5.txt']

    # detection_files = ['C:\\Users\谢龙龙\Desktop\数据集\sendmail-CERT\cert-sm5x-1.txt']
    # detection_files = ['C:\\Users\谢龙龙\Desktop\数据集\sendmail-CERT\cert-sm565a-1.txt']
    # detection_files = ['C:\\Users\谢龙龙\Desktop\数据集\sendmail-CERT\syslog-local-1.txt', 'C:\\Users\谢龙龙\Desktop\数据集\sendmail-CERT\syslog-local-2.txt']
    detection_files = ['D:\毕业论文相关\数据集\sendmail-UNM\\abnormal\decode-sm-280.txt', 'D:\毕业论文相关\数据集\sendmail-UNM\\abnormal\decode-sm-280.txt', 'D:\毕业论文相关\数据集\sendmail-UNM\\abnormal\sscp-sm-10814.txt', 'D:\毕业论文相关\数据集\sendmail-UNM\\normal\\bounce.txt', 'D:\毕业论文相关\数据集\sendmail-UNM\\normal\yanzheng.txt']
    detection(detection_files, threshold, new_calls_dict, A_dict, win_len, 0.1)
