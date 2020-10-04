# 调用函数
print(abs(-100))
print(max(1,4,23,6))
print(int('123'), int(12.3), float('12.34'))
print(str(1.23), str(100))


# 定义函数
def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x

print(my_abs(-100))

# 空函数，什么事也不做
def nop():
    pass #类似于占位符，不写代码也能运行

# 多个返回值，其实返回的是一个tuple
def move(x, y, step):
    return x + step, y - step


#函数的参数
#位置参数 x和n，这两个参数都是位置参数，调用函数时，传入的两个值按照位置顺序依次赋给参数x和n
def power1(x, n):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s

#默认参数power2(x) == power2(x,2)，也可以power2(x, n)
def power2(x, n=2):
    s = 1
    while n > 0:
        n = n - 1
        s = s * x
    return s
print(power2(5, 3))

# 可变参数
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n
    return sum
print(calc(1,2,3,4,5))

# 关键字参数
def person1(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)

person1('Bob', 35, city='Beijing')

# 命名关键字参数
# 命名关键字参数必须传入参数名，这和位置参数不同。如果没有传入参数名，调用将报错
# 和关键字参数**kw不同，命名关键字参数需要一个特殊分隔符*，*后面的参数被视为命名关键字参数。
def person2(name, age, *, city, job):
    print(name, age, city, job)

person2('Jack', 24, city='Beijing', job='Engineer')

# 如果函数定义中已经有了一个可变参数，后面跟着的命名关键字参数就不再需要一个特殊分隔符*了：
def person3(name, age, *args, city, job):
    print(name, age, args, city, job)

person3('harry', 16, 'port', city='Beijing', job='Engineer') #harry 16 ('port',) Beijing Engineer

# 参数组合
# 在Python中定义函数，可以用必选参数、默认参数、可变参数、关键字参数和命名关键字参数，这5种参数都可以组合使用。
# 但是请注意，参数定义的顺序必须是：必选参数、默认参数、可变参数、命名关键字参数和关键字参数。
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)

f1(12, 'we', 5, 6, name='haha', age = '12') #a = 12 b = we c = 5 args = (6,) kw = {'name': 'haha', 'age': '12'}
f2(12, 'ew', d='fd', name='lala')

# 适配所有情况
def all(*args, **kw):
    print(args, kw)


# 递归函数
def fact(n):
    if n==1:
        return 1
    return n * fact(n - 1)
print(fact(3))