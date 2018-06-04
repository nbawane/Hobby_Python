class Button():
	def __init__(self):
		print('square button')	#default button shape

	def function(self):
		print('I click')

	def sound(self):
		print('I thick')

class MyButton(Button):
	def __init__(self):
		print('rect button')
		super().__init__()
		super().function()

	# def sound(self):
	# 	print('I beep')

d=MyButton().sound()