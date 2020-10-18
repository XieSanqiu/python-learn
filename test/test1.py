'''
测试
try...except...finally...
'''

for i in range(2)[::-1]:
    try:
        print('try...')
        r = 10 / i
        a = 'dfg'
        print('result:', r)
    except ZeroDivisionError as e:
        print('except:', e)
        a = 'fdfdg'
    finally:
        print('finally...')

    t = ('evd', a, 'df')
    print(t)
''' 结果
try...
except: division by zero
finally...
END
'''