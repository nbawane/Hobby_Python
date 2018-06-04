def gen_square(lowerlim , higherlim):
	index = lowerlim
	while index<=higherlim:
		yield index*3
		index+=1


for i in gen_square(2,9):
	print (i)
