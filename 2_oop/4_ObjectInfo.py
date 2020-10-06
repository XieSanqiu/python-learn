# 获取对象信息

# 使用type()
import types
print(type(123)) #<class 'int'>
print(type('apple')) #<class 'str'>
print(type(None)) #<class 'NoneType'>
print(type(abs)) #<class 'builtin_function_or_method'>

print(type('abc')==type('123'))
print(type(123)==int)
print(type(abs)==types.BuiltinFunctionType)

# 使用isinstance()
print(isinstance(123, int))

# 获得一个对象的所有属性和方法
print(dir('abc'))

print(hasattr('abc', '__len__')) #True

# 我们希望从文件流fp中读取图像，我们首先要判断该fp对象是否存在read方法，如果存在，
# 则该对象是一个流，如果不存在，则无法读取。hasattr()就派上了用场。
def readData():
    pass
def readImage(fp):
    if hasattr(fp, 'read'):
        return readData(fp)
    return None