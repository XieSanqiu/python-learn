class Animal(object):
    def run(self):
        print('Animal is running...')

# 继承可以把父类的所有功能都直接拿过来，这样就不必重零做起，子类只需要新增自己特有的方法，也可以把父类不适合的方法覆盖重写。
class Dog(Animal):

    def run(self):
        print('Dog is running...')

    def eat(self):
        print('Eating meat...')


class Cat(Animal):
    pass

def run_twice(animal):
    animal.run()
    animal.run()

class Timer(object):
    def run(self):
        print('Start...')

if __name__ == '__main__':
    animal = Animal()
    dog = Dog()
    cat = Cat()

    animal.run()
    dog.run()
    cat.run()

    print(isinstance(animal, Animal)) #True
    print(isinstance(dog, Dog)) #True
    print(isinstance(cat, Cat)) #True
    print(isinstance(cat, Animal)) #True

    # 多态的好处，只要是Animal类型或者其子类型，就会调用实际类型的方法
    run_twice(animal)
    run_twice(dog)
    run_twice(cat)

    # 动态语言的鸭子属性 file-like object
    run_twice(Timer())