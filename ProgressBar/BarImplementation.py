import math

class showbar:
	def __init__(self,max_val):
		self.__maxval = max_val

	def displayprogress(self,currentval=0):
		PercentComplete = float(currentval)/self.__maxval
		print '|'*(math.floor(PercentComplete))

