"""
Description : This file implements the Drain algorithm for log parsing
Author      : LogPAI team
License     : MIT
"""

import re
import os
import numpy as np
import pandas as pd
import hashlib
from datetime import datetime


class Logcluster:
    def __init__(self, logTemplate='', logIDL=None):
        self.logTemplate = logTemplate
        if logIDL is None:
            logIDL = []
        self.logIDL = logIDL


class Node:
    def __init__(self, childD=None, depth=0, digitOrtoken=None):
        if childD is None:
            childD = dict()
        self.childD = childD
        self.depth = depth
        self.digitOrtoken = digitOrtoken


class LogParser:
    def __init__(self, log_format, indir='./', outdir='./result/', depth=4, st=0.4, 
                 maxChild=100, rex=[], keep_para=True):
        """
        Attributes
        ----------
            rex : regular expressions used in preprocessing (step1)
            path : the input path stores the input log file name
            depth : depth of all leaf nodes
            st : similarity threshold
            maxChild : max number of children of an internal node
            logName : the name of the input file containing raw log messages
            savePath : the output path stores the file containing structured logs
        """
        self.path = indir
        self.depth = depth - 2
        self.st = st
        self.maxChild = maxChild
        self.logName = None
        self.savePath = outdir
        self.df_log = None
        self.log_format = log_format
        self.rex = rex
        self.keep_para = keep_para

        self.root = None

    def hasNumbers(self, s):
        return any(char.isdigit() for char in s)

    def treeSearch(self, rn, seq): #p1:root node, p2:解析后的日志列表 从root node开始找匹配seq的叶节点（log cluster list）
        retLogClust = None  #return log cluster

        seqLen = len(seq)
        if seqLen not in rn.childD:
            return retLogClust #返回 None

        parentn = rn.childD[seqLen]

        currentDepth = 1
        for token in seq:
            if currentDepth >= self.depth or currentDepth > seqLen:
                break

            if token in parentn.childD:
                parentn = parentn.childD[token]
            elif '<*>' in parentn.childD:
                parentn = parentn.childD['<*>']
            else:
                return retLogClust #返回None
            currentDepth += 1

        logClustL = parentn.childD

        retLogClust = self.fastMatch(logClustL, seq)  #如果最高的相似度不够，返回的也是 None

        return retLogClust

    def addSeqToPrefixTree(self, rn, logClust):  #p1:root node, p2:日志模版对象，一个，是字段列表
        seqLen = len(logClust.logTemplate)
        if seqLen not in rn.childD:
            firtLayerNode = Node(depth=1, digitOrtoken=seqLen)  #解析树 二层是 digit 往下是 token
            rn.childD[seqLen] = firtLayerNode
        else:
            firtLayerNode = rn.childD[seqLen]

        parentn = firtLayerNode  #该长度下的节点

        currentDepth = 1
        for token in logClust.logTemplate:

            #Add current log cluster to the leaf node
            if currentDepth >= self.depth or currentDepth > seqLen: #达到预设的深度就将logClust加入，然后退出，当当前深度大于模版长度，也没有继续下去的必要了
                if len(parentn.childD) == 0:
                    parentn.childD = [logClust]
                else:
                    parentn.childD.append(logClust)
                break

            #If token not matched in this layer of existing tree. 
            if token not in parentn.childD:
                if not self.hasNumbers(token):
                    if '<*>' in parentn.childD:
                        if len(parentn.childD) < self.maxChild:
                            newNode = Node(depth=currentDepth + 1, digitOrtoken=token)
                            parentn.childD[token] = newNode
                            parentn = newNode
                        else:
                            parentn = parentn.childD['<*>']
                    else:
                        if len(parentn.childD)+1 < self.maxChild:
                            newNode = Node(depth=currentDepth+1, digitOrtoken=token)
                            parentn.childD[token] = newNode
                            parentn = newNode
                        elif len(parentn.childD)+1 == self.maxChild:
                            newNode = Node(depth=currentDepth+1, digitOrtoken='<*>')
                            parentn.childD['<*>'] = newNode
                            parentn = newNode
                        else:
                            parentn = parentn.childD['<*>']
            
                else:
                    if '<*>' not in parentn.childD:
                        newNode = Node(depth=currentDepth+1, digitOrtoken='<*>')
                        parentn.childD['<*>'] = newNode
                        parentn = newNode
                    else:
                        parentn = parentn.childD['<*>']

            #If the token is matched
            else:
                parentn = parentn.childD[token]

            currentDepth += 1

    #seq1 is template
    def seqDist(self, seq1, seq2): #计算日志与模版的相似度 seq1：模版，seq2：日志
        assert len(seq1) == len(seq2)
        simTokens = 0
        numOfPar = 0

        for token1, token2 in zip(seq1, seq2):
            if token1 == '<*>':
                numOfPar += 1
                continue
            if token1 == token2:
                simTokens += 1 

        retVal = float(simTokens) / len(seq1)

        return retVal, numOfPar


    def fastMatch(self, logClustL, seq):  #从 logClustL 中返回与 seq 最相似的 logClust
        retLogClust = None

        maxSim = -1
        maxNumOfPara = -1
        maxClust = None

        for logClust in logClustL:
            curSim, curNumOfPara = self.seqDist(logClust.logTemplate, seq)
            if curSim>maxSim or (curSim==maxSim and curNumOfPara>maxNumOfPara): #相似度相同时，返回'<*>' 多的logClust
                maxSim = curSim
                maxNumOfPara = curNumOfPara
                maxClust = logClust

        if maxSim >= self.st:
            retLogClust = maxClust  

        return retLogClust

    def getTemplate(self, seq1, seq2): #seq1：日志， seq2：模版  更新模版
        assert len(seq1) == len(seq2)
        retVal = []

        i = 0
        for word in seq1:
            if word == seq2[i]:
                retVal.append(word)
            else:
                retVal.append('<*>')

            i += 1

        return retVal

    def outputResult(self, logClustL):
        log_templates = [0] * self.df_log.shape[0]
        log_templateids = [0] * self.df_log.shape[0]
        df_events = []
        for logClust in logClustL:
            template_str = ' '.join(logClust.logTemplate)
            occurrence = len(logClust.logIDL)
            template_id = hashlib.md5(template_str.encode('utf-8')).hexdigest()[0:8]
            for logID in logClust.logIDL:
                logID -= 1
                log_templates[logID] = template_str
                log_templateids[logID] = template_id
            df_events.append([template_id, template_str, occurrence])

        df_event = pd.DataFrame(df_events, columns=['EventId', 'EventTemplate', 'Occurrences'])
        self.df_log['EventId'] = log_templateids
        self.df_log['EventTemplate'] = log_templates

        if self.keep_para:
            self.df_log["ParameterList"] = self.df_log.apply(self.get_parameter_list, axis=1) 
        self.df_log.to_csv(os.path.join(self.savePath, self.logName + '_structured.csv'), index=False)


        occ_dict = dict(self.df_log['EventTemplate'].value_counts())
        df_event = pd.DataFrame()
        df_event['EventTemplate'] = self.df_log['EventTemplate'].unique()
        df_event['EventId'] = df_event['EventTemplate'].map(lambda x: hashlib.md5(x.encode('utf-8')).hexdigest()[0:8])
        df_event['Occurrences'] = df_event['EventTemplate'].map(occ_dict)
        df_event.to_csv(os.path.join(self.savePath, self.logName + '_templates.csv'), index=False, columns=["EventId", "EventTemplate", "Occurrences"])


    def printTree(self, node, dep):
        pStr = ''   
        for i in range(dep):
            pStr += '\t'

        if node.depth == 0:
            pStr += 'Root'
        elif node.depth == 1:
            pStr += '<' + str(node.digitOrtoken) + '>'
        else:
            pStr += node.digitOrtoken

        print(pStr)

        if node.depth == self.depth:
            pStr2 = ''
            for i in range(dep+1):
                pStr2 += '\t'
            for tmp in node.childD:
                print(pStr2 + ' '.join(tmp.logTemplate))
            return 1
        for child in node.childD:
            self.printTree(node.childD[child], dep+1)

    def write_tree(self, file, node, dep):
        pStr = ''
        for i in range(dep):
            pStr += '\t'

        if node.depth == 0:
            pStr += 'Root'
        elif node.depth == 1:
            pStr += '<' + str(node.digitOrtoken) + '>'
        else:
            pStr += node.digitOrtoken

        file.write(pStr+'\n')

        if node.depth == self.depth:
            pStr2 = ''
            for i in range(dep + 1):
                pStr2 += '\t'
            for tmp in node.childD:
                pStr2 += ' '.join(tmp.logTemplate) + '\n'
                file.write(pStr2)
            return 1
        for child in node.childD:
            self.write_tree(file, node.childD[child], dep + 1)

    def serialize(self, root):
        ls = list()
        self.serialize_helper(root, ls, 0)
        return ','.join(ls)

    def serialize_helper(self, root, ls, depth):
        if root == None:
            return
        if depth == 0:
            ls.append('root')
        elif depth == 1:
            ls.append(str(root.digitOrtoken))
        else:
            ls.append(root.digitOrtoken)
        ls.append(str(len(root.childD)))
        if root.depth == self.depth:
            return 1

        for child in root.childD:
            self.serialize_helper(root.childD[child], ls, depth+1)

    def deserialize(self, data):
        if data == None or len(data) == 0:
            return None
        que = data.split(',')
        print(que)
        return self.deserialize_helper(que, 0)

    def deserialize_helper(self, que, dep):
        val = que.pop(0)
        size = int(que.pop(0))
        # print(val, size)
        if dep == 0:
            node = Node()
        elif dep == 1:
            node = Node(depth=1, digitOrtoken=int(val))
        else:
            node = Node(depth=dep, digitOrtoken=val)
        if size == 1 and dep == self.depth:
            return node
        for i in range(size):
            re_node = self.deserialize_helper(que, dep+1)
            node.childD[re_node.digitOrtoken] = re_node
        return node

    def read_tree(self, file):
        lines = []
        with open(file) as f:
            for line in f.readlines():
                lines.append(line)
        root = Node()
        self.read_tree_helper(root, lines, 1, 1)

    def read_tree_helper(self, parent_node, lines,  current_depth, current_line):
        t_count = lines[current_line].count('\t')
        if current_depth == 1:
            digit = int(lines[current_line].strip()[1:-1])
            node = Node(depth=1, digitOrtoken=digit)
            parent_node.childD[digit] = node

    def parse(self, logName):
        print('Parsing file: ' + os.path.join(self.path, logName))
        start_time = datetime.now()
        self.logName = logName
        rootNode = Node()
        self.root = rootNode
        logCluL = []

        self.load_data()  #根据log_format将原始日志文件解析成 字段 并写入 self.df_log

        count = 0
        for idx, line in self.df_log.iterrows(): #遍历行数据
            logID = line['LineId']
            logmessageL = self.preprocess(line['Content']).strip().split() #预处理日志内容，根据self.reg将部分字段替换为 '<*>'
            # print(logmessageL)
            # logmessageL = filter(lambda x: x != '', re.split('[\s=:,]', self.preprocess(line['Content'])))
            matchCluster = self.treeSearch(rootNode, logmessageL)

            #Match no existing log cluster
            if matchCluster is None:
                newCluster = Logcluster(logTemplate=logmessageL, logIDL=[logID])
                # print('newCluster', newCluster.logTemplate, newCluster.logIDL)
                logCluL.append(newCluster)
                self.addSeqToPrefixTree(rootNode, newCluster)

            #Add the new log message to the existing cluster
            else:  #能够找到匹配的日志模版
                newTemplate = self.getTemplate(logmessageL, matchCluster.logTemplate)
                matchCluster.logIDL.append(logID)
                if ' '.join(newTemplate) != ' '.join(matchCluster.logTemplate):  #更新找到的模版
                    matchCluster.logTemplate = newTemplate

            count += 1
            if count % 1000 == 0 or count == len(self.df_log):
                print('Processed {0:.1f}% of log lines.'.format(count * 100.0 / len(self.df_log)))


        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)

        # self.printTree(rootNode, 6)
        self.outputResult(logCluL)

        print('Parsing done. [Time taken: {!s}]'.format(datetime.now() - start_time))

    def parse_log(self, logs):
        log_messages = []
        headers, regex = self.generate_logformat_regex(self.log_format)
        for line in logs:
            try:
                match = regex.search(line.strip())
                # print('match', match)
                message = [match.group(header) for header in headers]
                # print('message', message)
                log_messages.append(message)
            except Exception as e:
                pass
        logdf = pd.DataFrame(log_messages, columns=headers)
        print(logdf)
        for idx, line in logdf.iterrows(): #遍历行数据
            logmessageL = self.preprocess(line['Content']).strip().split() #预处理日志内容，根据self.reg将部分字段替换为 '<*>'
            # print(logmessageL)
            # logmessageL = filter(lambda x: x != '', re.split('[\s=:,]', self.preprocess(line['Content'])))
            matchCluster = self.treeSearch(self.root, logmessageL)
            print(matchCluster.logTemplate)

    def load_data(self):
        headers, regex = self.generate_logformat_regex(self.log_format)
        self.df_log = self.log_to_dataframe(os.path.join(self.path, self.logName), regex, headers, self.log_format)

    def preprocess(self, line):
        for currentRex in self.rex:
            line = re.sub(currentRex, '<*>', line)  #根据预设的规则，先将能匹配的改为 '<*>'
        return line

    def log_to_dataframe(self, log_file, regex, headers, logformat):
        """ Function to transform log file to dataframe 
        """
        log_messages = []
        linecount = 0
        with open(log_file, 'r') as fin:
            for line in fin.readlines():
                try:
                    match = regex.search(line.strip())
                    # print('match', match)
                    message = [match.group(header) for header in headers]
                    # print('message', message)
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
        logdf = pd.DataFrame(log_messages, columns=headers)
        logdf.insert(0, 'LineId', None)
        logdf['LineId'] = [i + 1 for i in range(linecount)]
        return logdf


    def generate_logformat_regex(self, logformat):
        """ Function to generate regular expression to split log messages
        """
        headers = []
        splitters = re.split(r'(<[^<>]+>)', logformat)  #(<>)匹配<>并获取这一匹配，[^<>]+：除 '<' '>' 以外的所有字符 + 一次或多次
        # print(logformat)
        # print(splitters)
        regex = ''
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(' +', '\\\s+', splitters[k])  #将连续的空格替换为 '\s+'
                # print(splitter)
                regex += splitter
            else:
                header = splitters[k].strip('<').strip('>')
                regex += '(?P<%s>.*?)' % header  #header 替换 %s
                headers.append(header)
            # print(k, regex)
        # print(regex)
        regex = re.compile('^' + regex + '$')
        # print(regex)
        # print(headers)
        return headers, regex

    def get_parameter_list(self, row):
        template_regex = re.sub(r"<.{1,5}>", "<*>", row["EventTemplate"])
        # print('row', row["EventTemplate"])
        # print('template_regex', template_regex)
        if "<*>" not in template_regex: return []
        template_regex = re.sub(r'([^A-Za-z0-9])', r'\\\1', template_regex)
        template_regex = re.sub(r'\\ +', r'\\s+', template_regex)
        template_regex = "^" + template_regex.replace("\<\*\>", "(.*?)") + "$"
        # print('template_regex2', template_regex)
        parameter_list = re.findall(template_regex, row["Content"])
        parameter_list = parameter_list[0] if parameter_list else ()
        parameter_list = list(parameter_list) if isinstance(parameter_list, tuple) else [parameter_list]
        return parameter_list