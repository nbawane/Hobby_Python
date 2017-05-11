#diff module

class Calc(object):
	def __init__(self):
		print"welcome to calculator"
		
	def add(self,num1,num2):
		self.num1 = num1
		self.num2 = num2
		return self.num1+self.num2

	def multiply(self,num1,num2):
		self.num1 = num1
		self.num2 = num2
		return self.num1*self.num2

	def sub(self,num1,num2):
		self.num1 = num1
		self.num2 = num2
		return self.num1-self.num2
		
