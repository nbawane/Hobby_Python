#private attribute

class A:
	def __init__(self,name):
		self.__name = name
		
class B(A):
	def __init__(self):
		print "name assigned ",self.name
		
ii = B('madsfn')
		
	