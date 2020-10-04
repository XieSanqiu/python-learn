# 输入
# 直接输入
name = input()
# 输入提示
age = input('请输入您的年龄：')


# 输出
print('hello, world')

# 多个字符串可以用逗号隔开，逗号 "," 会输出一个空格，不使用逗号隔开也行
print("hello", name)
print("hello""李华")

# 定义分割符
print("www", "google", "com", sep=".")

# end 设置以什么为结尾
print('不换行', end=' ')
print('。。。分号+换行结尾', end=';\n')

# 格式化输出
print('姓名：{0}， 年龄：{1}'.format(name, age))
print('{1} and {0}'.format('google', 'baidu'))
print('姓名：{name}， 年龄：{age}'.format(name = name, age = age))
print('PI的值为:{0:6.2f}, 小明身高:{1:6}'.format(3.1415926, 182))