"""Return the difference of another Transaction object, or another 
class object that also has the `val` property."""

class Transaction(object):

    def __init__(self, val):
        self.val = val

    def __sub__(self, other):
        return self.val + other.val




buy = Transaction(10.00)
sell = Transaction(7.00)
print(buy - sell)
c = 'a'+'b'

# 3.0