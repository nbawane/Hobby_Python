
class arg:
	def fun(self,*args):
		print 'abcd',args
		print type(args)
		for i in args:
			print"arg ",i
			
a = arg()
a.fun('a','b','3',4,5,'fga')