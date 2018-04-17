"""
If main instance is deleted then child instances are deleted
if __del__ is not defined it shows default behaviour ie. do nothing

"""

class Main:
	def __init__(self):
		print('in main class')

	def __del__(self):
		print('deleting main')

	def operation(self):
		print('perfroming main operation')

class Interface:
	def __init__(self):
		print('In Interface')
		self.mainobj=Main()

	def __del__(self):
		print('deleting Interface')

	def	operation(self):
		print('performing interface operation')
		self.mainobj.operation()

if __name__ == "__main__":
	interfaceobj= Interface()
	interfaceobj.operation()
	print('did that..........1111111')
	print('''''''')
	# del interfaceobj



