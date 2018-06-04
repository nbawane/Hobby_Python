'''
steps:
1.pass a class to singleton method
2.singleton method will return function address
3.that function will get called and add the instance in dictionary
4. and return the instance
'''

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class Counter:
    def __init__(self):
        self.count = 0
    def inc(self):
        self.count += 1
        return self.count

print (type(Counter))    # <type 'classobj'>
Counter = singleton(Counter)
print (type(Counter))

a = Counter()
print( a.inc())
b = Counter()
print (b.inc())

