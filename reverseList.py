#reverse list

l = [1,2,3,4,5,6,7,8,9,0,'a']
print l
ll = len(l)

for i in range(0,ll/2):
	l[ll-i-1],l[i] = l[i],l[ll-1-i]
		
print l