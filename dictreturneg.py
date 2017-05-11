def main():
	print "function : ",retdic()[1]
	if 1 in retlist():
		print "yes"
	else:
		print "no"
def retdic():
	di = {1:"adf",8:"aseww",4:"ppop"}
	return di
def retlist():
	li = [1,2,3,4,5,6]
	return li
main()	