#!/usr/bin/env python
import sys
sys.path.append('../')
from drain_log_parser import Drain

input_dir  = 'logs/'  # The input directory of log file
output_dir = 'Drain_result/'  # The output directory of parsing results
log_file   = '233-log'  # The input log file name
log_format = '<Date> <Time> <Host> <Component>(\[<PID>\])?: <Content>'  # HDFS log format
# Regular expression list for optional preprocessing (default: [])
regex      = [r'(\d+\.){3}\d+', r'\d{2}:\d{2}:\d{2}', r'0x[a-fA-F0-9]{8}']  #匹配IP、时间
st         = 0.36  # Similarity threshold
depth      = 5  # Depth of all leaf nodes

parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex, keep_para=True)
parser.parse(log_file)

# parser.printTree(parser.root, 0)
# file = open('233-log-tree.txt', 'a')
# parser.write_tree(file, parser.root, 0)
str = parser.serialize(parser.root)
print(str)
root = parser.deserialize(str)
print(root.childD[3].childD['+'].childD['<*>'].digitOrtoken)
print(parser.serialize(root))

# parser.parse_log(['2019-10-17 16:06:11 nagios rz[27864]:  [root] aptopo.jar/ZMODEM: 469826 Bytes, 1374133 BPS'])