# list 有序集合
classmates = ['Michael', 'Bob', 'Tracy']
print(classmates)
print(len(classmates))
print(classmates[0], classmates[-1]) #索引访问元素
classmates.append('Adam') #添加元素
print(classmates)
classmates.insert(1, 'Jack') #插入元素
print(classmates)
classmates[1] = 'Sarah' #替换元素
print(classmates)

#list里面元素数据类型可以不同
s = ['python', 'java', ['asp', 'php'], 'scheme', 123, True]
print(s, len(s), s[2][1])
L = [] #定义一个lsit变量


#tuple 有序元组，一旦初始化不能修改，每有append()、insert()之类的方法
classmates2 = ('Michael', 'Bob', 'Tracy')
print(classmates2)
t1 = ()
t2 = (1,) #只有一个元素时要加个逗号
t = ('a', 'b', ['A', 'B'])
t[2][0] = 'C'
print(t)


# dict 字典
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
print(d)
print(d['Bob'], 'Michael' in d)
d['Bob'] = 60 #设置值
print(d['Bob'])
print(d.get('Harry', -1)) # 获取不到取默认值
d.pop('Tracy') #删除一个元素
print(d)


# set key的集合
s = set([1, 2, 2, 2, 3]) #创建一个set，需要提供一个list作为输入集合
print(s)
s.add(6) #添加元素
s.remove(2) #删除元素
print(s)

# 集合操作
s1 = set([1, 2, 3])
s2 = set([2, 3, 4])
print(s1 & s2)
print(s1 | s2)
print(s1 - (s1 & s2))