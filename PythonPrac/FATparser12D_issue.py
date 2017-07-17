import logging
logging.basicConfig(filename='12D_400GB_issue_boundary.txt',level=logging.DEBUG)
'''
FAT1 Start : 0x18000 FAT1 End : 0x1FFFF, FAT2 Start : 0x20000, FAT2 end : 0x2016D
'''
path = r'C:\400GBlog\SameRS400G\SDRBoard_09524\16\VSCFULLCAPSC16_Validation_20170707_204341.log'
FWFATstart = 94830
FWFATend = 131439
FWDIRstart = FWFATend + 1
FWDIRend = 2097151
fd = open(path)
logging.info('400GB issue FAT parser')
for line in fd:

	if 'FAT1 address' in line:
		FAT1addr = line.split(':')[-1].strip('\n\r')
		FAT1addrint = int(FAT1addr,16)
		if FAT1addrint <= FWFATstart-32:
			logging.info('FATstart boundary value %s'%line)
			print line
	if 'FAT2 address' in line:
		logging.info(line.split(':')[-2:])
		FAT2addr = line.split(':')[-1].strip('\n\r')
		FAT2addrint = int(FAT2addr, 16)
		if FAT2addrint >= FWFATend-32:
			logging.info('FATend boundary value %s'%line)
			print line
	if  'DIR address' in line:
		logging.info(line.split(':')[-2:])
		DIRaddr = line.split(':')[-1].strip('\n\r')
		DIRaddrint = int(DIRaddr, 16)
		if (DIRaddrint<=FWDIRstart) or (DIRaddrint >= FWDIRend):
			logging.info('DIR boundary value %s'%line)
			print line
print 'done'