class Student(object):
    teacher = 'Marry'
    def __init__(self, name):
        self.name = name

print(Student.teacher) #Marry

s1 = Student('Harry')
print(s1.teacher) #Marry
s1.teacher = 'Jane'
print(s1.teacher) #Jane

print(Student.teacher) #Marry