
import random
import logger.logger as logger

log_file = r'C:\Results\regionlog.txt'
log = logger.log(log_file)

cardMaxLba = 995670	#blocks
chunksize = random.randrange(8, 100, 8)  # chunk size in terms of blocks
log.Info("chunk size %s"%chunksize)
regions = random.randint(4, 10)
log.Info("regions : %s"%regions)
allign_to_chunksize = cardMaxLba - (cardMaxLba % chunksize)
allign_to_regions = allign_to_chunksize - (allign_to_chunksize % regions)
Total_blocks = allign_to_regions

#self.__dvtLib.CQEnable(Set_CQ=True, Set_Cache=True, Set_Sequential_mode=True)

#queue_depth = self.__dvtLib.GetCQDepth()
queue_depth = 32
count = 0
blockcount = 0
current_region = 0
regionDiff = Total_blocks/regions
TaskIdList=[x for x in range(queue_depth)]
StartLbalist=[0]*queue_depth
StartLbas = [(Total_blocks * i) / regions for i in range(regions)]
#log.Info('StartLbas %s'%StartLbas)
print regionDiff
while blockcount < Total_blocks:
	log.Info('Queing the task')
	for loop in range(queue_depth):
		current_region = count%regions
		StartLbas[current_region] = StartLbas[current_region]+chunksize
		StartLbalist[count % queue_depth] = StartLbas[current_region]-chunksize
		blockcount = blockcount + chunksize
		count += 1
		log.Info("count : %s"%count)
	log.Info("write at :: TaskID : %s\nStartLba : %s\n" % (TaskIdList, StartLbalist))
	log.Info('Executing the task')
	for task in TaskIdList:
		log.Info('Execting :: task : %s , StartLba : %s'%(TaskIdList[task], StartLbalist[task]))