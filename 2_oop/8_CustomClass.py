class Student(object):
    def __init__(self, name):
        self.name = name

    # 作用于 print()时，返回用户看到的字符串
    def __str__(self):
        return 'Student object (name: %s)' % self.name

    # __repr__() 返回程序开发者看到的字符串
    __repr__ = __str__

s1 = Student('Harry')
print(s1) #Student object (name: Harry)


class Fib1(object):
    def __init__(self, n):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b
        self.n = n

    def __iter__(self):
        return self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b # 计算下一个值
        if self.a > self.n: # 退出循环的条件
            raise StopIteration()
        return self.a # 返回下一个值

for n in Fib1(10):
    print(n)


class Fib2(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a
f = Fib2()
print(f[3])