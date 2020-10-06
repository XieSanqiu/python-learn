from enum import Enum, unique

# @unique装饰器可以帮助我们检查保证没有重复值。
@unique
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

day1 = Weekday.Mon
print(day1) #Weekday.Mon
print(Weekday.Tue) #Weekday.Tue
print(Weekday['Tue']) # Weekday.Tue
print(Weekday.Tue.value) #2

print(day1 == Weekday.Mon) #True
print(Weekday(1)) #Weekday.Mon