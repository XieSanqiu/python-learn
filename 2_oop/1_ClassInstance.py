# 定义一个类Student，继承自 object
class Student(object):

    # __init__() 方法第一个参数永远是self，表示创建的实例本身
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def print_stu(self):
        print('%s : %s' %(self.name, self.age))

if __name__ == '__main__':
    s1 = Student('Marry', '12') #参数必须要跟类里的__init__() 方法一样，不用传self
    print(s1) #<__main__.Student object at 0x000002D006C20C88>

    # s2 = Student(13); #TypeError: __init__() missing 1 required positional argument: 'age'

    s1.score = 88; #可以自由的给一个实例绑定属性

    s1.print_stu(); #调用类的方法