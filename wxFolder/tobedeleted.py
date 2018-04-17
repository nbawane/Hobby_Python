import time
import timeit

a = range(18000)
b=[]

def test():
	global b
	b=a[:]
print timeit.timeit('test()',setup="from __main__ import test")

