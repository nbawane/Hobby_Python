f = lambda x,y: x+y		#lambda args,operation
print(f(1,9))

def square(l):
	return l*l


b = [1,2,3,4,5,6,7,8,9,9,8,7,6,5,4,3,2]
a = list(map(square,b))
print(a)


fil = filter(lambda x:x%3,b)

print(list(fil))


