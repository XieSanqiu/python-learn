# 函数式编程允许把函数本身作为参数传入另一个函数，还允许返回一个函数

# map() 接收两个参数，一个是函数，一个是Iterator
# map 将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
def f(x):
    return x * x
r1 = map(f, [1,2,3,4,5,6])
print(list(r1))


#reduce() reduce把一个函数作用在一个序列[x1, x2, x3, ...]上
# 这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
from functools import reduce
def add(x, y):
    return x+y

r2 = reduce(add, [1,2,3,4,5,6])
print(r2)

# map() reduce() 结合的一个demo
def fn(x, y):
    return x * 10 + y

def char2num(s):
    digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    return digits[s]

a = reduce(fn, map(char2num, '13579'))
print(a)
print('-------------------------------------------')


# filter() 过滤序列
# filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素。
def is_odd(n):
    return n % 2 == 1

l1 = list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
print(l1)



# sorted() 排序函数
print(sorted([36, 5, -12, 9, -21]))
print(sorted([36, 5, -12, 9, -21], key=abs))
print(sorted([36, 5, -12, 9, -21], reverse=True))
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower))
# 按照成绩排序
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_score(s):
    return -s[1]
print(sorted(L, key=by_score))
print('-------------------------------------------')



# 返回函数
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum

f = lazy_sum(1,2,3,5)
print(f())

# 闭包
# notice：返回闭包时牢记一点：返回函数不要引用任何循环变量，或者后续会发生变化的变量。
def count():
    fs = []
    for i in range(1, 4):
        def f():
             return i*i
        fs.append(f)
    return fs

f1, f2, f3 = count()
# 跟预想的不一样原因就在于返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9
print(f1(), f2(), f3()) #9 9 9
# 解决方法：再创建一个函数，用该函数的参数绑定循环变量当前的值，无论该循环变量后续如何更改，已绑定到函数参数的值不变
def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1, 4):
        fs.append(f(i)) # f(i)立刻被执行，因此i的当前值被传入f()
    return fs
f1, f2, f3 = count()
print(f1(), f2(), f3()) #1 4 9
print('-------------------------------------------')



# 匿名函数 lambda
L = list(filter(lambda x: x % 2 == 1, range(1, 20)))
print(L)
print('-------------------------------------------')


# 装饰器：在代码运行期间动态增加功能，本质上，decorator就是一个返回函数的高阶函数。
def log(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper

@log
def now():
    print('2020-10-4')

now()

def log2(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log2('execute')
def now2():
    print('2020-10-4')

# 首先执行log('execute')，返回的是decorator函数，再调用返回的函数，参数是now函数，返回值最终是wrapper函数。
now2()
print(now2.__name__) #wrapper

# 更完整的写法
import functools
def log3(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log3('execute')
def now3():
    print('2020-10-4')

now3()
print(now3.__name__) #now3
print('-------------------------------------------')


# 偏函数
# 简单总结functools.partial的作用就是，把一个函数的某些参数给固定住（也就是设置默认值），返回一个新的函数，调用这个新函数会更简单。
# 当函数的参数个数太多，需要简化时，使用functools.partial可以创建一个新的函数，这个新函数可以固定住原函数的部分参数，从而在调用时更简单。
int2 = functools.partial(int, base=2)
print(int2('1000')) #8
print(int2('1000', base=8)) # 512

max2 = functools.partial(max, 10)
print(max2(1,2,4)) #10