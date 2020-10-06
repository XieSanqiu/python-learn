# Python允许在定义class的时候，定义一个特殊的__slots__变量，来限制该class实例能添加的属性
class Student(object):
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称

s1 = Student()
s1.name = 'Mary'
print(s1.name)
# s1.score = 12 #AttributeError: 'Student' object has no attribute 'score'

# 使用__slots__要注意，__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的
class GraduateStudent(Student):
    pass
gs1 = GraduateStudent()
gs1.score = 89
print(gs1.score) #89

