#to test static variable

class name:
    count = 0

    def __init__(self,rot):
        self.rot = rot

a = name(123)
a.count +=10
print a.count
print name.count
name.count += 9
print name.count