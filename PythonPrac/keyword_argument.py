def c():
	print 'c'
	a()


def a():
	print "a"
	c()
c()