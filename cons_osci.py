

#print len(array)


def given_fun():
	max_len = 0
	dist = 0
	array = [5,0,-2,6,3,4,4,-3,5]
	l=len(array)
	for i in range(0,l):
		for j in range(i,l):
			if (cons_diff_test(array,i,j) == True) and monotonic(array,i,j) == False:
				dist = (j+1)-i
				#print "dist is ",dist
				if max_len < dist:
					max_len = dist
					lower_lim = i
					upper_lim = j
					#print "cons and mono",i,j,array[i:j+1]
				
			'''#else:
				#print "false"
			if monotonic(array,i,j) == False:
				print "non mono",i,j,array[i:j+1]
			#else:
				#print "Monotonic"
				'''
	return max_len,lower_lim,upper_lim,array
def cons_diff_test(a,i,j):
	for k in range(j):
		if a[k]==a[k+1]:
			return False
	return True
	
def monotonic(a,i,j):
	if j-i > 2:
		for k in range(i,j):
			if a[k]>a[k+1]>a[k+2] or a[k]<a[k+1]<a[k+2]:
				return True
			else:
				return False
	
	
ans,low_lim,up_lim,arr = given_fun()	
print " max slice len ",ans
print "slice is ",arr[low_lim:up_lim+1]
	
		
						