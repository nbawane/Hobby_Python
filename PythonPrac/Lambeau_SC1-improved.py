import random as randomObj

def Run():
	maxblockcount = 32
	minblockcount = 4
	powercyclesize = 65000
	maxcardcapacity = 250000
	chunksize = 1000	#10MB size of each chunk write pattern
	address = 0
	cycle = 0
	chunknumber = 1
	pattern = 0
	changepattern = 0
	chunkpattern = {}
	numberofpattern = 9
	patternlist  = [0,1,2,3,4,5,6,7,8]
	while cycle<1:
		print 'cycle count : %s'%cycle
		cycle+=1
		while address < maxcardcapacity:
			#address = 1000
			numberofblocks = randomObj.randint(minblockcount,maxblockcount)
			if (address + numberofblocks) >= (chunksize*chunknumber):
				#print 'chunksize reached'
				chunkpattern[(chunknumber-1)%numberofpattern] = pattern
				numberofblocks = chunksize*chunknumber-(address)
				chunknumber +=1
				
				changepattern = 1

			if (chunknumber*chunksize)>powercyclesize:
				powercyclesize+=powercyclesize
				if cycle%2:
					power_cycle()
			write(address, numberofblocks,pattern)
			
			address=address+numberofblocks+1		
			if changepattern == 1:
				
				
				pattern = patternlist[chunknumber%len(patternlist)-1]
				if len(chunkpattern.keys())==numberofpattern:
					randomObj.shuffle(patternlist)
					performreadverify(chunkpattern,chunknumber-1)
					chunkpattern = {}
				changepattern = 0
				
		if any(chunkpattern):
			performreadverify(chunkpattern,chunknumber-1,endaddress=address)
		address = 0		
			
def performreadverify(chunkpattern,chunknumber,endaddress = None):
	print 'Patern %s'%chunkpattern
	chunksize = 1000
	maxcardcapacity = 250000
	for key in chunkpattern.keys():
		startaddress = (chunknumber-(len(chunkpattern.keys())-key))*chunksize
		#print 'startaddress : %s, Pattern to verify : %s'%(startaddress,chunkpattern[key])
		if maxcardcapacity-startaddress	< chunksize:
			chunksize = maxcardcapacity-startaddress
		read(startaddress, chunksize,chunkpattern[key])
	
	
def write(address,numberofblocks,pattern):
	print '[write]start address : %s number of blocks : %s pattern : %s'%(address,numberofblocks,pattern)

def read(address,numberofblocks,pattern):
	print '[read]start address : %s number of blocks : %s ,pattern : %s' % (address, numberofblocks,pattern)

def power_cycle():
	print "#################### power cycle"

def speedmode_change(speedmode):
	print 'speed mode : %s'%speedmode

Run()