
dummylist = []

class a:
	def flater(self,inputlist):
		for i in inputlist:
			if type(i) == int:
				dummylist.append(i)
			elif type(i) == list:
				self.flater(i)


if __name__ == '__main__':
	int = a()
	listtoflat = [5, 7, range(16, 257), range(23, 31), [1, 2, [111, 222, [321, 432]]]]
	int.flater(listtoflat)
	print dummylist