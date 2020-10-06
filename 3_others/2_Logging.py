# debug，info，warning，error等几个级别，当我们指定level=INFO时，logging.debug就不起作用了
# logging的另一个好处是通过简单的配置，一条语句可以同时输出到不同的地方，比如console和文件。

import logging
#
# def foo(s):
#     return 10 / int(s)
#
# def bar(s):
#     return foo(s) * 2
#
# def main():
#     try:
#         bar('0')
#     except Exception as e:
#         # logging.error(e)
#         logging.exception(e)
#
# main()
# print('END')

logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='logging.log',
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )
logging.info('info...')
logging.debug(('debug...'))
logging.warning('warning...')
logging.error('error...')