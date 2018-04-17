adict = {'a':100,'b':33,'c':898,'d':43}
bdict = {'a':105,'b':30,'c':808,'d':48}
cdict = {'a':125,'b':31,'c':848,'d':41}
edict = None
ddict = {'b':23,'p':32}
allvariable = ['adict','bdict','cdict','edict','ddict']

'''
opdict = {'a':{'adict':100,'bdict':105,'cdict':125}....}
'''
findict = {}
def getvardata(var):
	for curdict in allvariable:
		try:
			findict[curdict] = eval(str(curdict))[var]
		except:
			pass

	print ({var:findict})
getvardata('b')