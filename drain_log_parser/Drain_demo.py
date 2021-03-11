#!/usr/bin/env python
import sys
sys.path.append('../')
from drain_log_parser import Drain

input_dir  = 'logs/'  # The input directory of log file
output_dir = 'Drain_result/'  # The output directory of parsing results
log_file   = 'Linux_test.log'  # The input log file name
log_format = '<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>'  # HDFS log format
# Regular expression list for optional preprocessing (default: [])
regex      = [r'(\d+\.){3}\d+', r'\d{2}:\d{2}:\d{2}']  #匹配IP、时间
st         = 0.66  # Similarity threshold
depth      = 5  # Depth of all leaf nodes

parser = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir,  depth=depth, st=st, rex=regex, keep_para=True)
parser.parse(log_file)

