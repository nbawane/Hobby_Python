#===========string search and ccount=============#
# s = 'abcniteshabcmiterabc'
# sst = 'abc'
# count  = 0
# l = len(s)
# lsst = len(sst)
# for i in range(l):
	# if sst == s[i:(lsst+i)]:
		# count +=1
# print'abc count ',count


#===========flatening of list=============#
# l = []
# s = [1,2,3,[2,3,4,[1,564,4],[1,2222,3333,4444]]]
# def fun(s):
	# for i in s:
		# if isinstance(i,list):
			# fun(i)
		# else:
			# l.append(i)
# fun(s)	
# print l

#=============dictionary making===============#

# s = 'abcniteshabcmiterabc'
# sst = 'abc'
# count  = 0
# d = {}
# l = len(s)
# lsst = len(sst)
# for i in range(l):
	# if sst == s[i:(lsst+i)]:
		# count +=1
# print'abc count ',count
# d[sst] = count	#make dictionary
# print d

#=============return list================#
# def p():
	# t= [x for x in range(10)]
	# return t
	
# print p()

#================generator example=============#

# def gen(n):
	# a=0
	# while a<n:
		# a+=1
		# yield a
# for x in gen(10):
	# print x
	
#================mapping ======================#

# def cub(a):
	# return a*a*a
# l = [1,2,3,4,5,6,7,8]
# p = map(cub,l)
# print p

# def mo(x):
	# return x%2
# l = [1,2,3,4,5,6,7,8]
# p = filter(mo == 0,l)
#==================fibo===================#

class a:
	def __init__(self,an):
		self.an = an
		print self.an
		
	def nm(self,x):
		self.x = x
		print self.x
ad = a(2333)
ad.nm(23)
