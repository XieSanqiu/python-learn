# 读文件
# 一次读取完文件内容
with open('logging.log') as f:
    print(f.read())

# 一行行读取
with open('logging.log') as f:
    for line in f.readlines():
        print(line)

# 读取一行
with open('logging.log') as f:
    print(f.readline())


# 写文件
# 默认是gbk编码
with open('write.txt', 'a', encoding='utf8') as f:
    f.write('写一行\n')