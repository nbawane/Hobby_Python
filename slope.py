L = [[0,0],[1,1],[2,2],[3,3],[3,2],[4,2],[5,1]]
inf=999999999999

def solution(A):
	count = 0
	for i in range(len(A)):
		for j in range(i+1,len(A)):
			for k in range(j+1,len(A)):
				slope_1 = slope(A[i],A[j])
				slope_2 = slope(A[i],A[k])
				if slope_1 == slope_2 and j!=k:
					count +=1
					print "points are colinear %r %r %r"%(A[i],A[j],A[k])
	return count

def slope(a,b):
	x1 = a[0]
	y1 = a[1]
	x2 = b[0]
	y2 = b[1]
	try:
		slp = float(x2-x1)/(y2-y1)
		print slp
	except ZeroDivisionError:
		slp = inf
	print 'data is x1 %r y1 %r x2 %r y2 %r'%(x1,y1,x2,y2)
	return slp
print solution(L)

