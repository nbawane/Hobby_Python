a = [1,2,3,3,3,4,4,5,6,6,7,7,8,8,8,8,8,8,9,9,9]
	b=[]
	x=None
	for i in a:
		if i==x:
			continue
		else:
			b.append(i)
			x=i

print b
