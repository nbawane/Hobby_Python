a = [1,2,4,6,0]
c = [2,4,5,7,0]
d = [1,2,3,4,5]
def myfunc(hand):
	return max(hand)
b = max(a,c,d,key=myfunc)
print b


