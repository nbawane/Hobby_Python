 A zero-indexed array A consisting of N integers is given. A pair of indices(P, Q), such that 0<=P<=Q<N, is called a slice of array A.
 A slice is describing as oscillating if:
 every two consecutive elements of the array A  inside the slice are different and no three consecutive elements of the array A inside the slice are monotonic.
 write a function that given an array A consisting of N integers, returns the size of the largest oscillating slice in A. If there is no such slice, the function should return 0.'''

	'''
	def cons_diff_test(array):
		max_len = 0
		dist = 0
		l = len(array)
		for i in range(0,l):
			for j in range(i,l):
				if array[j]==array[j+1]:
		'''