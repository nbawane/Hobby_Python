#private meethods and variables

class Mojo:

	__jo = 5
	__name = "mordor"
	def __init__(self):
		print "hello__!!"
		
	def __hello(self,name):
		self.__name = name
		print "name is ",self.__name
		
butter = Mojo()
butter.___jo = 45	#not accessable will give error as no attributes
print "no __j0",butter.__jo #not accessable
butter.hello("jojo")