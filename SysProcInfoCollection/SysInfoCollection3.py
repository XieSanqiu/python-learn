# -*- coding: utf-8 -*-
import psutil
import datetime
import time
import socket
import os
import pymongo

def get_host_ip():
    """
    查询本机ip地址
    """
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(('8.8.8.8',80))
        ip=s.getsockname()[0]
    finally:
        s.close()
    return ip

class SysInfoCollect(object):
    def getName(self):
        hostname = socket.gethostname()
        return hostname

    def getStartTime(self):
        dt = datetime.datetime.fromtimestamp(psutil.boot_time())
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def getCPUTime(self):
        cpuTime = psutil.cpu_times()
        cpuUser = cpuTime.user
        cpuSys = cpuTime.system
        cpuIdle = cpuTime.idle
        cpuTotal = cpuUser + cpuSys + cpuIdle
        return cpuTotal, cpuUser, cpuSys, cpuIdle

    def getCPUPercent(self):
        cpuPercent = psutil.cpu_percent(1)
        return cpuPercent

    def getCPUStats(self):
        # cpuStats=psutil.cpu_stats()
        # ctxSwitches=cpuStats.ctx_switches
        # interrupts=cpuStats.interrupts
        # sInterrupts=cpuStats.soft_interrupts
        # syscalls=cpuStats.syscalls
        return 0, 0, 0, 0


    def getVirtualMem(self):
        memInfo = psutil.virtual_memory()
        memTotal = float(memInfo.total) / 1024 / 1024  # M
        memAva = float(memInfo.available) / 1024 / 1024
        memPercent = memInfo.percent
        memUsed = float(memInfo.used) / 1024 / 1024
        memFree = float(memInfo.free) / 1024 / 1024
        memBuffers = float(memInfo.buffers) / 1024 / 1024
        memCaches = float(memInfo.cached) / 1024 / 1024

        return memTotal, memAva, memPercent, memUsed, memFree, memBuffers, memCaches

    def getSwapMem(self):
        sswap = psutil.swap_memory()
        swapTotal = float(sswap.total) / 1024 / 1024
        swapUsed = float(sswap.used) / 1024 / 1024
        swapFree = float(sswap.free) / 1024 / 1024
        swapPercent = sswap.percent
        swapSin = float(sswap.sin) / 1024 / 1024
        swapSout = float(sswap.sout) / 1024 / 1024

        return swapTotal, swapUsed, swapFree, swapPercent, swapSin, swapSout

    def getDiskUsage(self):
        diskInfo = psutil.disk_usage('/')
        diskTotal = float(diskInfo.total) / 1024 / 1024 / 1024  # G
        diskUsed = float(diskInfo.used) / 1024 / 1024 / 1024
        diskFree = float(diskInfo.free) / 1024 / 1024 / 1024
        diskPercent = diskInfo.percent
        return diskTotal, diskUsed, diskFree, diskPercent

    def getDiskIO(self):
        diskIO = psutil.disk_io_counters()
        readCount = diskIO.read_count
        writeCount = diskIO.write_count
        readByte = float(diskIO.read_bytes) / 1024 / 1024  # M
        writeByte = float(diskIO.write_bytes) / 1024 / 1024
        readTime = float(diskIO.read_time) / 1000  # s
        writeTime = float(diskIO.write_time) / 1000
        # readVector = readByte * 1024 / readTime  # Kb/s
        # writeVector = writeByte * 1024 / writeTime
        return readCount, writeCount, readByte, writeByte, readTime, writeTime

    def getNetIO(self):
        netIO = psutil.net_io_counters()
        byteSent = float(netIO.bytes_sent) / 1024 / 1024  # M
        byteRecv = float(netIO.bytes_recv) / 1024 / 1024
        packetSent = float(netIO.packets_sent) / 1000  # k
        packetRecv = float(netIO.packets_recv) / 1000
        errin = float(netIO.errin) / 1000
        errout = float(netIO.errout) / 1000
        dropin = float(netIO.dropin) / 1000
        dropout = float(netIO.dropout) / 1000
        return byteSent, byteRecv, packetSent, packetRecv, errin, errout, dropin, dropout

    def getProcessNum(self):
        pids = []
        for proc in psutil.process_iter():
            pinfo = proc.as_dict()
            pids.append(pinfo['pid'])
        return len(set(pids))

    def getPorts(self):
        ports = []
        for proc in psutil.process_iter():
            pinfo = proc.as_dict()
            conn = pinfo['connections']
            data_listen = [x for x in conn if 'LISTEN' in x]
            pid_port = []
            for port in data_listen:
                pid_port.append(port.laddr[1])
            ports += pid_port
        return list(set(ports))

class ProcInfoCollect(object):
    #获取当前时间主机中所有进程的运行信息，返回进程运行信息集合，主键：进程执行路径+进程执行参数+进程启动时间+进程id
    def getProcessInfo(self):
        processes_dict = {}  #进程集合
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(
                    attrs=['exe', 'name', 'username', 'pid', 'cpu_percent', 'ppid', 'memory_percent', 'memory_info',
                           'terminal', 'status', 'create_time', 'cpu_times', 'cmdline', 'uids', 'gids', 'nice',
                           'num_ctx_switches', 'num_fds', 'num_threads', 'io_counters', 'open_files', 'connections'])
            except psutil.NoSuchProcess:
                pass
            else:
                procExe = pinfo['exe']
                procName = pinfo['name']
                procUser = pinfo['username']
                procPID = pinfo['pid']
                procPPID = pinfo['ppid']

                procCPU = pinfo['cpu_percent']
                procCPUUTime = pinfo['cpu_times'].user
                procCPUSTime = pinfo['cpu_times'].system

                procMEM = '{:.3f}'.format(pinfo['memory_percent'])
                procRSS = pinfo['memory_info'].rss
                procVMS = pinfo['memory_info'].vms

                procTTY = pinfo['terminal']
                procSTAT = pinfo['status']
                procSTART = pinfo['create_time']

                if len(pinfo['cmdline']) > 0:
                    procCMD = pinfo['cmdline'][0]
                    if len(pinfo['cmdline']) > 1:
                        procParam = ' '.join(pinfo['cmdline'][1:])
                    else:
                        procParam = '-None'
                else:
                    procCMD = 'None'
                    procParam = '-None'

                procRUID = pinfo['uids'].real
                procEUID = pinfo['uids'].effective
                procSUID = pinfo['uids'].saved

                procRGID = pinfo['gids'].real
                procEGID = pinfo['gids'].effective
                procSGID = pinfo['gids'].saved

                procNice = pinfo['nice']
                procCTXSWV = pinfo['num_ctx_switches'].voluntary
                procCTXSWINV = pinfo['num_ctx_switches'].involuntary
                procFDS = pinfo['num_fds']
                procThreads = pinfo['num_threads']

                procRCount = pinfo['io_counters'].read_count
                procWCount = pinfo['io_counters'].write_count
                procRBytes = pinfo['io_counters'].read_bytes
                procWBytes = pinfo['io_counters'].write_bytes

                procEnv = {}
                procFile = pinfo['open_files']
                procFileNum = len(procFile)
                procConnection = pinfo['connections']
                procConnNum = len(procConnection)
            stopTime = -1
            procDiskRRate , procDiskWRate = 0, 0
            key = (procExe, procParam, procSTART, procPID)
            dataValue = [procExe, procName, procUser, procPID, procPPID, procCPU, procCPUUTime, procCPUSTime,
                         procMEM, procRSS, procVMS, procTTY, procSTAT, procCMD, procParam, procRUID, procEUID,
                         procSUID, procRGID, procEGID, procSGID, procNice, procCTXSWV, procCTXSWINV, procFDS,
                         procThreads, procRCount, procWCount, procRBytes, procWBytes,procDiskRRate , procDiskWRate,
                         procEnv, procFile, procFileNum, procConnection, procConnNum, procSTART, stopTime]
            processes_dict[key] = dataValue
        return processes_dict


def writeIntofile(filePath,fileName,captureTime,dataName,dataValue,name,bootTime):

    logFile=filePath+fileName
    if os.path.exists(logFile):
        t=os.path.getctime(logFile)
        cDate=time.strftime("%Y-%m-%d",time.localtime(t))
        captureDate = datetime.datetime.strptime(captureTime, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        if cDate==captureDate:
            f = open(logFile, 'a')
            f.write("\n")
            f.write(captureTime+" "+name+" "+str(bootTime)+" ")
            for i in range(0,len(dataName)):
                content=dataName[i]+":"+str(dataValue[i])+" "
                f.write(content)
            f.close()
        else:
            f = open(logFile, 'w')
            f.write(captureTime+" "+name+" "+str(bootTime)+" ")
            for i in range(0, len(dataName)):
                content = dataName[i] + ":" + str(dataValue[i]) + " "
                f.write(content)
            f.close()
    else:
        f = open(logFile, 'w')
        f.write(captureTime+" "+name+" "+str(bootTime)+" ")
        for i in range(0, len(dataName)):
            content = dataName[i] + ":" + str(dataValue[i]) + " "
            f.write(content)
        f.close()

def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

def updatemongo(dataName,dataValue,captureTime):
    mongo=pymongo.MongoClient("mongodb://211.65.197.70:27017")
    db=mongo["anomaly"]
    col=db['sysinfo']
    d=dict()
    d['time']=captureTime
    d['host']='211.65.197.175'
    for i in range(len(dataName)):
        d[dataName[i]]=dataValue[i]
    col.insert_one(d)

def update_proc_activity(host_ip, all_process):
    mongo=pymongo.MongoClient("mongodb://211.65.197.70:27017")
    db = mongo['pinfo']
    col = db['activity']
    res = {}
    for proc in all_process:
        proc_exe = proc[0]
        #print(proc_exe)
        if proc_exe is None or proc_exe == "":
            proc[0] = 'kernel'
        key = (proc[0], proc[14])
        if key in res:
            if proc[37] < res[key]['start_time']:
                res[key]['start_time'] = proc[37]
                res[key]['start_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(proc[37]))
                res[key]['user_name'] = proc[2]
            res[key]['cpu_percent'] += proc[5]
            res[key]['mem_percent'] += proc[8]
            res[key]['disk_read_rate'] += proc[30]
            res[key]['disk_write_rate_result'] += proc[31]
            res[key]['open_files'] |= set(proc[33])
            res[key]['connections'] |= set(proc[35])
            res[key]['threads'] += proc[25]
            res[key]['proc_num'] += 1
        else:
            res[key] = {'HostIP':host_ip, 'start_time':proc[37], 'proc_name':proc[1], 'user_name':proc[2], 'proc_param':proc[14],
                        'proc_exe':proc[0], 'cpu_percent':proc[5], 'mem_percent':proc[8], 'disk_read_rate':proc[30], 'disk_write_rate_result':proc[31],
                        'open_files':set(proc[33]), 'connections':set(proc[35]), 'threads':proc[25]}
            res[key]['start_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(proc[37]))
            res[key]['proc_num'] = 1

    current_time = time.time()
    current_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time))
    for app_key in res:
        res[app_key]['open_files'] = list(res[app_key]['open_files'])
        res[app_key]['files_num'] = len(res[app_key]['open_files'])
        res[app_key]['connections'] = list(res[app_key]['connections'])
        res[app_key]['connections_num'] = len(res[app_key]['connections'])
        res[app_key]['collect_time'] = current_time
        res[app_key]['collect_date'] = current_date
    # 插入到mongodb
    count = len(res.values())
    if count != 0:
        col.insert_many(list(res.values()))
    return count


if __name__=="__main__":
    sysInfo = SysInfoCollect()
    procInfo = ProcInfoCollect()
    host_ip = get_host_ip()

    name = sysInfo.getName().strip()
    bootTime = sysInfo.getStartTime()

    cycle_start_time = time.time()  #该周期开始时间
    cycle_time = 300  #一个周期默认300秒
    processes_A = {}

    while(True):
        try:
            current_time = time.time()
            current_date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current_time))
            one_cycle_continued_time = current_time - cycle_start_time
            # 从mongodb中获取收集周期
            try:
                mongo = pymongo.MongoClient("mongodb://211.65.197.70:27017")
                record_time_col = mongo['pinfo']['record_time']
                query1 = {'type': 'collect_rate', 'host': host_ip}
                x = record_time_col.find_one(query1, {'_id': 0, 'rate': 1})['rate']  # 收集周期（秒）
                if x:
                    cycle_time = x
            except IOError:
                print(current_date_time + ' : 从mongodb中获取数据收集周期错误')

            processes_B = procInfo.getProcessInfo()
            #将当前时刻出现的进程添加的进程集合A
            for proc_key in processes_B:
                if proc_key not in processes_A:
                    processes_A[proc_key] = processes_B[proc_key]

            #将此前时刻出现在集合A，当前时刻没出现在集合B的进程更新其结束时间，磁盘读写速度已经无法计算
            for proc_key in processes_A:
                if proc_key not in processes_B:
                    processes_A[proc_key][-1] = current_time

            if one_cycle_continued_time >= cycle_time:
                # 1、写系统运行数据到文件
                # 获取系统运行信息
                cpuTotal, cpuUser, cpuSys, cpuIdle = sysInfo.getCPUTime()
                cpuPercent = sysInfo.getCPUPercent()
                ctxSwitches, interrupts, sInterrupts, syscalls = sysInfo.getCPUStats()
                memTotal, memAva, memPercent, memUsed, memFree, memBuffers, memCaches = sysInfo.getVirtualMem()
                swapTotal, swapUsed, swapFree, swapPercent, swapSin, swapSout = sysInfo.getSwapMem()
                diskTotal, diskUsed, diskFree, diskPercent = sysInfo.getDiskUsage()
                readCount, writeCount, readByte, writeByte, readTime, writeTime = sysInfo.getDiskIO()
                byteSent, byteRecv, packetSent, packetRecv, errin, errout, dropin, dropout = sysInfo.getNetIO()
                processNum = sysInfo.getProcessNum()
                ports = sysInfo.getPorts()
                dataName = ["cpuTotal", "cpuUser", "cpuSys", "cpuIdle", "cpuPercent", "ctxSwitches", "interrupts",
                            "sInterrupts", "syscalls", "memTotal", "memAva", "memPercent", "memUsed", "memFree",
                            "memBuffers", "memCaches", "swapTotal", "swapUsed", "swapFree", "swapPercent", "swapSin",
                            "swapSout", "diskTotal", "diskUsed", "diskFree", "diskPercent", "readCount", "writeCount",
                            "readByte", "writeByte", "readTime", "writeTime", "byteSent", "byteRecv", "packetSent",
                            "packetRecv", "errin", "errout", "dropin", "dropout", "processNum", "ports"]
                dataValue = [cpuTotal, cpuUser, cpuSys, cpuIdle, cpuPercent, ctxSwitches, interrupts, sInterrupts, syscalls,
                             memTotal, memAva, memPercent, memUsed, memFree, memBuffers, memCaches, swapTotal, swapUsed,
                             swapFree, swapPercent, swapSin, swapSout, diskTotal, diskUsed, diskFree, diskPercent,
                             readCount, writeCount, readByte, writeByte, readTime, writeTime, byteSent, byteRecv,
                             packetSent, packetRecv, errin, errout, dropin, dropout, processNum, ports]
                updatemongo(dataName, dataValue, current_date_time)
                sysInfoPath = "/usr/local/systemInfoMonitor/"
                sysInfoName = "sysInfo.log"
                writeIntofile(sysInfoPath, sysInfoName, current_date_time, dataName, dataValue, name, bootTime)

                #2、写进程运行信息
                #B集合中有的可以用来计算磁盘读写速度
                for proc_key in processes_B:
                    if processes_A[proc_key][-2] > cycle_start_time:
                        time_diff = current_time - processes_A[proc_key][-2]
                    else:
                        time_diff = one_cycle_continued_time
                    processes_A[proc_key][30] = ((processes_B[proc_key][28] - processes_A[proc_key][28]) / time_diff) / 1024
                    processes_A[proc_key][31] = ((processes_B[proc_key][29] - processes_A[proc_key][29]) / time_diff) / 1024

                dataName = ["procExe", "procName", "procUser", "procPID", "procPPID", "procCPU", "procCPUUTime",
                            "procCPUSTime", "procMEM", "procRSS", "procVMS", "procTTY", "procSTAT", "procCMD",
                            "procParam", "procRUID", "procEUID", "procSUID", "procRGID", "procEGID", "procSGID",
                            "procNice", "procCTXSWV", "procCTXSWINV", "procFDS", "procThreads", "procRCount",
                            "procWCount", "procRBytes", "procWBytes", "procDiskRRate", "procDiskWRate", "procEnv",
                            "procFile", "procFileNum", "procConnection", "procConnNum", "procSTART", "stopTime"]

                pInfoPath = "/usr/local/systemInfoMonitor/"
                pInfoName = "pInfo.log"

                for proc_key in processes_A:
                    dataValue = processes_A[proc_key]
                    writeIntofile(pInfoPath, pInfoName, current_date_time, dataName, dataValue, name, processes_A[proc_key][-2])

                #3、将进程活动信息写入mongodb
                insert_count = update_proc_activity(host_ip, processes_A.values())
                # print(current_date_time, host_ip, insert_count, 'application activities')

                #4、更新周期数据
                cycle_start_time = current_time
                processes_A = processes_B
            time.sleep(10)
        except Exception as e:
            current_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            print(current_date, e)
            time.sleep(10)