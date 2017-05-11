class Foo:
	def __init__(self,inval):
		print"initial value : ",inval

	def setval(self,value):
		print 'in setval()'
		self.value=value
	
	def getval(self):
		return self.value
		
ob = Foo(6)
ob.setval(8)
print"updated value : ",ob.getval()

class Bar(Foo):
	def increment(self,va):
		self.va=va
		self.va+=1
		return self.va

oopp = Bar(101010)
oopp.setval(34)
print"inherit:",oopp.getval()