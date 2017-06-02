import random
cardMaxLba = 995670	#blocks
chunksize = random.randrange(8, 100, 8)  # chunk size in terms of blocks
print "chunk size %s"%chunksize
regions = random.randint(4, 10)
print "regions : %s"%regions
allign_to_chunksize = cardMaxLba - (cardMaxLba % chunksize)
allign_to_regions = allign_to_chunksize - (allign_to_chunksize % regions)
Total_blocks = allign_to_regions

#self.__dvtLib.CQEnable(Set_CQ=True, Set_Cache=True, Set_Sequential_mode=True)

#queue_depth = self.__dvtLib.GetCQDepth()
queue_depth = 32
count = 0
blockcount = 0
current_region = 0
StartLbalist = [(Total_blocks * i) / regions for i in range(regions)]
while blockcount < Total_blocks:

	TaskId = count%queue_depth
	current_region = count%regions
	StartLba = StartLbalist[current_region]
	print "write at :: TaskID : %s , current_reg : %s , StartLba : %s"%(TaskId,current_region,StartLba)
	StartLbalist[current_region] = StartLbalist[current_region]+chunksize
	blockcount = blockcount + chunksize
	count += 1
	print"count : %s"%count
