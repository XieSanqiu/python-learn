'''
进程分类模块
'''
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
def classification(pci):
    if 2 in pci['proc_ppid']:
        return 1
    if 'None' in pci['terminal']:
        pci['terminal'].remove('None')
    if len(pci['terminal']) >= 1 and 1 not in pci['ppid']:
        return 4

