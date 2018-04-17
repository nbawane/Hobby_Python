import random

def Run():
	maxblockcount = 32
	minblockcount = 4
	maxcardcapacity = 0x3b7
	address = 0
	
	index = 0

	numberofreadstoperform = None
	minreadpercentage = 10
	maxreadpercentage = 20


	minimunnuberofpowercycle = 3
	maximunnuberofpowercycle = 7
	numberofcycle =6
	cycle = 0
	speedmodes = ['LS','HS','SDR12','SDR25','SDR50','SDR104-200mA','SDR104-400mA','DDR200']
	'''
	will contain starting address of LBA, list[1]-list[0] 
	is supposed to give number of blocks to transfer
	this same list is supposed to used fro all randomization
	'''
	while cycle < numberofcycle:
		address = 0
		writeformat = []
		writeaddrssblockcountdict = {}
		readformatdict = {}
		readformat = []
		powercycleaddress = []
		cycle += 1
		print 'cycle count : %s'%cycle
		while address < maxcardcapacity:

			
			blockcount = random.randint(minblockcount, maxblockcount)

			if address+blockcount >= maxcardcapacity:
				blockcount = maxcardcapacity - address
			writeformat.append(address)
			writeaddrssblockcountdict[address] = blockcount
			address += blockcount
		if cycle%2==0:
			print 'Starting random cycle'
			random.shuffle(writeformat)

		print 'writeformat : %s'%writeformat
		print 'writeaddrssblockcountdict : %s'%writeaddrssblockcountdict
		powercyclecount = random.randint(minimunnuberofpowercycle,maximunnuberofpowercycle)
		powercycleaddress = random.sample(writeformat,powercyclecount)
		numberofreadstoperform = random.randint(minreadpercentage*(len(writeformat))/100,maxreadpercentage*(len(writeformat))/100)#to get the number reads to be performed in btween operation
		print 'numberofreadstoperform  : %s'%numberofreadstoperform
		readformat = random.sample(writeformat,numberofreadstoperform)
		print readformat
		for address in writeformat:
			speedmodechangeflag = random.randint(1,4)
			if speedmodechangeflag == 1:
				speedmode = random.choice(speedmodes)
				speedmode_change(speedmode)			
			write(address,writeaddrssblockcountdict[address])
			readaddress = random.choice(writeformat)

			if readaddress in readformat:
				read(readaddress,writeaddrssblockcountdict[readaddress])
				readformat.remove(readaddress)
			if address in powercycleaddress:
				power_cycle(address)

def write(address,numberofblocks):
	print '[write]start address : %s number of blocks : %s'%(address,numberofblocks)

def read(address,numberofblocks):
	print '[read]start address : %s number of blocks : %s' % (address, numberofblocks)

def power_cycle(address):
	print 'power cycle at address : %s'%address

def speedmode_change(speedmode):
	print 'speed mode : %s'%speedmode

Run()