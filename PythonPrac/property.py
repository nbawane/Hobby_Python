class boss:
	def __init__(self):
		self.__man = None

	@property
	def man(self):
	    return self.__man

	@man.setter
	def man(self,val):
		self.__man = val

f = boss()
print(f.man)
f.man = 90
print(f.man)