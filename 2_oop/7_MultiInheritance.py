class Animal(object):
    pass

# 大类:
class Mammal(Animal):
    pass

class Bird(Animal):
    pass

class Runnable(object):
    def run(self):
        print('Running...')

class Flyable(object):
    def fly(self):
        print('Flying...')

# 通过多重继承，一个子类就可以同时获得多个父类的所有功能。
class Dog(Mammal, Runnable):
    pass

class Bat(Mammal, Flyable):
    pass


# 为了更好地看出继承关系，我们把Runnable和Flyable改为RunnableMixIn和FlyableMixIn
# MixIn的目的就是给一个类增加多个功能，这样，在设计类的时候，我们优先考虑通过多重继承来组合多个MixIn的功能，而不是设计多层次的复杂的继承关系。
class RunnableMixIn(object):
    def run(self):
        print('Running...')

class FlyableMixIn(object):
    def fly(self):
        print('Flying...')

class CarnivorousMixIn(object):
    def eat(self):
        print('meat...')

class Dog(Mammal, RunnableMixIn, CarnivorousMixIn):
    pass