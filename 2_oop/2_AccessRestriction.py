class Student():
    # 属性加上双下划线表示私有，不能通过实例直接访问
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def print_stu(self):
        print('%s : %s' % (self.__name, self.__age))

    def _private_method1(self):
        print('私有方法1，能被实例访问')

    def __private_method2(self):
        print('私有方法2，不能被实例访问')

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age


if __name__ == '__main__':
    s1 = Student('mary', 12)
    s1.print_stu() #mary : 12

    # print(s1.__name) #'Student' object has no attribute '__name'
    # print(s1._Student__name) #mary  可以访问的到，但是不建议使用

    s1.set_age(16)
    s1.print_stu() #mary : 16

    s1._private_method1() #能访问，不建议访问
    # s1.__private_method2() #AttributeError: 'Student' object has no attribute '__private_method2'