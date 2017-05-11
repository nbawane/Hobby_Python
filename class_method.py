# #calling with class

# class Nycro:
	# @staticmethod
	# def halo(self):
		# self.traceface = traceface
		# return "thats it "+self.traceface
		
# print Nycro.halo()

class A(object):

	def f(self,x):
		print self.x
		self.foo(7878)
		
    def foo(self,x):
        print "executing foo(%s,%s)"%(self,x)

    @classmethod
    def class_foo(cls,x):
        print "executing class_foo(%s,%s)"%(cls,x)
		

    @staticmethod
    def static_foo(x):
        print "executing static_foo(%s)"%x    
	
	

a=A()
a.foo(2)
a.class_foo(4)
A.class_foo(6)

