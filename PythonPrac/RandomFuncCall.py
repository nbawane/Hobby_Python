'''
randomly call a function
'''
import random
def a():
	print 'I am a()'


def b():
	print 'I am b()'


def c():
	print 'I am c()'
for i in range(10):
	random.choice([a,b,c])()
