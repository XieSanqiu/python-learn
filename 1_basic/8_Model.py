#!/usr/bin/env python3   #可以在Unix/Linux/Mac上运行
# -*- coding: utf-8 -*-  #.py文件使用的是utf-8编码

' a test module '  #模块的文档注释

__author__ = 'Xie Sanqiu'  #作者信息，特殊变量

def test():
    print('编写一个模块')

_private_variable = '私有变量'  #不希望被直接使用
def _private_method():
    print(_private_variable)
    print('私有函数，不希望直接被调用')

# 其他地方使用该模块，if 判断失败
if __name__ == '__main__':
    test()

# 安装第三方模块
# 在python命令行界面 pip install xxx