class A:
	def a(self):
		print('a')

class B(A):
	def a(self):
		print('b')

class C(B):
	def a(self):
		print('c')

class D(C):
	def a(self):
		print('d')


for cls in D.mro()[:-1]:
	clll = cls()
	clll.a()