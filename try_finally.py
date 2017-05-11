#try except finally

a = 0
b = 9

c = 0

try:
	b/a
except ZeroDivisionError:
	print "oh no"
else:
	print "oh yes"	
finally:
	print "ill work always"