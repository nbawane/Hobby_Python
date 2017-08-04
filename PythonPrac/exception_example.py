'experiment to see behaviour for multiple raise'
'result: only last rasie message will be printed'
a = 10
b = 0
def zerodef():
	try:

		c = a/b
	except ZeroDivisionError:
		raise Exception('division by zero happened')

def mathop():
	try:
		zerodef()
	except:
		raise Exception('Program could have failed')
mathop()