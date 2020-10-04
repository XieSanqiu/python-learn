# 切片
L1 = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
print(L1[0:3])
print(L1[:2])
print(L1[2:3])
print(L1[-2:]) #['Bob', 'Jack']

L2 = list(range(10))
print(L2)
print(L2[2:9:3])
print(L2[::2])
print('------------------------------------------------')



# 迭代
# 迭代list, tuple, str, dict, set 用 for in
for c in 'abc':
    print(c)

d = {'a': 1, 'b': 2, 'c': 3}
for k, v in d.items():
    print(k, v, sep=':')
for k in d:
    print(k, end=', ')
print()
for v in d.values():
    print(v, end=', ')
print()
# 下表循环
for i, value in enumerate(['A', 'B', 'C']):
    print(i, value)

for x, y in [(1, 1), (2, 4), (3, 9)]:
    print(x, y)

print('------------------------------------------------')



# 列表生成式
lg1 = list(range(1, 11))
print(lg1)
lg2 = [x * x for x in range(1, 11)]
print(lg2)
lg3 = [x * x for x in range(1, 11) if x % 2 == 0]
print(lg3)
lg4 = [m + n for m in 'ABC' for n in 'XYZ']
print(lg4)
lg5 = [k + '=' + str(v) for k, v in d.items()]
print(lg5)

L3 = ['Hello', 'World', 'IBM', 'Apple']
lg6 = [s.lower() for s in L3]
print(lg6)

# if else
lg7 = [x if x % 2 == 0 else -x for x in range(1, 11)]
print(lg7)
print('------------------------------------------------')



# 生成器 一边循环一边计算的机制
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'
for n in fib(6):
    print(n)

def odd():
    print('step 1')
    yield 1
    print('step 2')
    yield(3)
    print('step 3')
    yield(5)
o = odd();
print(next(o))
print(next(o))
print(next(o))
# print(next(o)) #运行出错 StopIteration



# 迭代器
'''
凡是可作用于for循环的对象都是Iterable类型；
凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列；
集合数据类型如list、dict、str等是Iterable但不是Iterator，不过可以通过iter()函数获得一个Iterator对象。
'''
# Python的for循环本质上就是通过不断调用next()函数实现的
for x in [1, 2, 3, 4, 5]:
    pass
# 完全等价于
# 首先获得Iterator对象:
it = iter([1, 2, 3, 4, 5])
# 循环:
while True:
    try:
        # 获得下一个值:
        x = next(it)
    except StopIteration:
        # 遇到StopIteration就退出循环
        break