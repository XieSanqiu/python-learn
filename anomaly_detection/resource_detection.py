
'''
使用孤立森林检测进程主机资源使用是否异常
需求分析：
1、以应用为对象，key：ip+进程可执行文件+参数，
2、以每个应用找最近运行的、无异常的、100条数据 作为训练数据，检测当前该进程的运行是否异常
3、若没有找到 100 条，则通过 白名单+临界资源使用检测  检测该应用是否异常

每分钟运行一次，检索时间(last_current_time, current_time]，时间检索字段：collect_time(float)
'''

import pymongo, time
from iforest.iForest import IsolationTreeEnsemble
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor


class ResourceDetection:
    def __init__(self):
        self.mongo = pymongo.MongoClient('mongodb://211.65.197.70:27017')
        self.db = self.mongo['pinfo']
        self.activity_col = self.db['activity']
        self.whitelist_col = self.db['whitelist']
        # 类型1：用于 离群点异常检测
        self.fields_type_1 = {'_id': 0, 'start_time': 0, 'collect_time': 0, 'connections': 0, 'open_files': 0,
                              'collect_date': 0, 'start_date': 0, 'user_name': 0}
        # 类型2：用于敏感资源使用检测
        self.fields_type_2 = {'_id': 0, 'start_time': 0, 'collect_time': 0, 'collect_date': 0, 'start_date': 0}
        #类型3：用于 离群点异常检测 训练阶段
        self.fields_type_3 = {'_id': 0, 'start_time': 0, 'collect_time': 0, 'connections': 0, 'open_files': 0,
                              'collect_date': 0, 'start_date': 0, 'user_name': 0, 'proc_exe':0, 'HostIP':0,
                              'proc_param':0, 'proc_name':0}
        self.fields_type_4 = {'_id':0, 'proc_name':0, 'user_name':0, 'cpu_percent':0, 'mem_percent':0, 'disk_read_rate':0,
                              'disk_write_rate':0, 'connections_set':0, 'open_files_set':0}

    #获取所有主机所有应用的活动信息
    def get_processes_activities(self, last_current_time:float, current_time:float, wanted_fields):
        query = {'collect_time':{'$gt':last_current_time, '$lte':current_time}}
        if wanted_fields == 1:
            fields = self.fields_type_1
        elif wanted_fields == 2:
            fields = self.fields_type_2
        res = self.activity_col.find(query, fields)
        all_processes = []
        for one in res:
            all_processes.append(one)
        print(type(all_processes), len(all_processes))
        print(all_processes)
        return all_processes

    def built_iForest_for_all_processes(self, num):
        #step1:从白名单中找哪些进程能够构建孤立森林
        query = {'activity_num':{'$gte':num}}
        white_proc = self.whitelist_col.find(query)
        proc_it = dict()
        for one in white_proc:
            key = (one['HostIP'], one['proc_exe'], one['proc_param'])
            print(key)
            iforest = self.built_iForest_for_one_process(key, num)
            if iforest != None:
                proc_it[key] = iforest

        return proc_it

    def built_iForest_for_one_process(self, key, num):
        #step1：根据进程key从activity库中找到 最近的 100条 正常 的活动信息作为训练信息构建孤立森林
        recent_normal_activities = self.get_recent_normal_activities(key, num)
        recent_normal_activities.append([1, 52.9, 25.313, 0.0, 0.509, 5, 46])
        data_num = len(recent_normal_activities)
        train_data = np.array(recent_normal_activities)
        if data_num >= num:
            it = IsolationTreeEnsemble(100, 1000)
            it.fit(train_data, True)
            scores = it.anomaly_score(train_data)
            print(scores)
            max_score = np.max(scores)
            # train_attr_weight = np.array(it.attr_weight)
            return it, max_score
        else:
            print('数量过少，不足以构建孤立森林')
            return None

    def get_recent_normal_activities(self, key, num):
        query = {'HostIP':key[0], 'proc_exe':key[1], 'proc_param':key[2]}
        res = self.activity_col.find(query, self.fields_type_3).sort([('collect_time', -1)]).limit(num)
        recent_activities = []
        for one in res:
            # print(one)
            activity = [one['proc_num'], round(one['cpu_percent'], 3), round(one['mem_percent'], 3), round(one['disk_read_rate'], 3),
                        round(one['disk_write_rate'], 3), one['connections_num'], one['files_num']]
            recent_activities.append(activity)
            print(activity)
        return recent_activities


if __name__ == '__main__':
    resource = ResourceDetection()
    # resource.get_processes_activities(1615636469, 1615636769, 2)
    # resource.built_iForest_for_all_processes(200)
    key = ('211.65.197.175', '/usr/lib/jvm/jdk1.8.0_131/bin/java', '-XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly -Djava.awt.headless=true -Dfile.encoding=UTF-8 -Djruby.compile.invokedynamic=true -Djruby.jit.threshold=0 -XX:+HeapDumpOnOutOfMemoryError -Djava.security.egd=file:/dev/urandom -Xmx1g -Xms1g -Xss2048k -Djffi.boot.library.path=/usr/local/logstash-6.1.1/vendor/jruby/lib/jni -Xbootclasspath/a:/usr/local/logstash-6.1.1/vendor/jruby/lib/jruby.jar -classpath :.:/usr/lib/jvm/jdk1.8.0_131/jre/lib/rt.jar:/usr/lib/jvm/jdk1.8.0_131/lib/dt.jar:/usr/lib/jvm/jdk1.8.0_131/lib/tools.jar -Djruby.home=/usr/local/logstash-6.1.1/vendor/jruby -Djruby.lib=/usr/local/logstash-6.1.1/vendor/jruby/lib -Djruby.script=jruby -Djruby.shell=/bin/sh org.jruby.Main /usr/local/logstash-6.1.1/lib/bootstrap/environment.rb logstash/runner.rb -f etc/log7.conf')
    # it, max_score = resource.built_iForest_for_one_process(key, 400)
    # print(max_score)
    # print(train_attr_weight)
    # it.clear_attr_weight()
    # det_score = it.anomaly_score(np.array([[1, 62.9, 35.313, 0.0, 0.509, 5, 46]]))
    # detect_attr_weight = np.array(it.attr_weight)
    # print(detect_attr_weight)
    # print(detect_attr_weight / train_attr_weight)
    # print(det_score)

    # X_train = np.array(resource.get_recent_normal_activities(key, 400))
    # rng = np.random.RandomState(42)  # 随机数生成器
    # clf = IsolationForest(max_samples=200, random_state=rng)
    # clf.fit(X_train)
    # y_pred_train = clf.predict(X_train)
    # print(y_pred_train)
    # X_train_scores = clf.decision_function(X_train)
    # print('X_train_scores', X_train_scores)
    # print(np.min(X_train_scores))
    # X_test = np.array([[1, 62.9, 25.313, 0.0, 0.509, 5, 46]])
    # y_pred_test = clf.predict(X_test)
    # print(y_pred_test)
    # X_test_scores = clf.decision_function(X_test)
    # print('X_test_scores', X_test_scores)

    data = resource.get_recent_normal_activities(key, 300)
    clf = LocalOutlierFactor(n_neighbors=20, algorithm='auto', contamination=0, n_jobs=-1)
    res = clf.fit_predict(data)
    print(res)
    print(clf.negative_outlier_factor_)