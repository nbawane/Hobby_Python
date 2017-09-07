import time

def mem1(temp):
	'''2LC by A2h command'''
	addmap = {}
	addmap['col_addr']='0-13'
	addmap['page_addr']='17-24'
	addmap['plane']=25
	addmap['block_addr']='25-36'
	print decode(addmap,temp)


def decode(addmap,temp):
	'''
	returns a dictionary with field value
	:param addmap:
	:param temp:
	:return:
	'''
	for key in addmap.keys():
		offsets = addmap[key]
		mask = getmask(offsets)
		fielddata = mask & int(temp,16)#converting hexstring to integer
		addmap[key] = hex(fielddata)
	return addmap

def getmask(offsets):
	"""
	creates mask to extract the fields from address map
	"""
	if isinstance(offsets,int):
		temp_data = 1<<offsets
	else:
		temp_data = 0
		lsbbit = int(offsets.split('-')[0])
		temp_lsbbit = lsbbit
		msbbit = int(offsets.split('-')[1])
		totalbit = msbbit-lsbbit
		for i in range(totalbit+1):
			temp_data = 1<<(temp_lsbbit)|temp_data
			temp_lsbbit = temp_lsbbit+1

	return temp_data

def merge_address(addrlist):
	a = time.time()
	temp = ''
	for byte in addrlist:
		hexnum = (int(byte, 16))
		if hexnum < 10:
			byte = '0' + byte
		temp = byte + temp
	b = time.time()
	print b,a
	print 'time for pro',(b-a)
	print temp
	print type(temp)
	mem1(temp)
if __name__ == '__main__':
	addrlist = ['40', '11', '6', '0', '40']
	merge_address(addrlist)
	# decode_mem1(temp)
	# getmask()


