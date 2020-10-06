# try:
#     print('try...')
#     r = 10 / 0
#     print('result:', r)
# except ZeroDivisionError as e:
#     print('except:', e)
# finally:
#     print('finally...')
# print('END')

# 使用try...except捕获错误有一个巨大的好处，就是可以跨越多层调用
def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        print('Error:', e)
    finally:
        print('finally...')

main()
print('END')

# 自定义错误并抛出
class FooError(ValueError):
    pass

def foo(s):
    n = int(s)
    if n==0:
        raise FooError('invalid value: %s' % s)
    return 10 / n

# foo('0')

# 向上抛出异常，交给上层处理
def bar():
    try:
        foo('0')
    except ValueError as e:
        print('ValueError!')
        raise

bar()