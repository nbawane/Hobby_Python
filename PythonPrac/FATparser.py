import logging
logging.basicConfig(filename='FATParser_12D_issue.log',level=logging.DEBUG)
'''
FAT1 Start : 0x18000 FAT1 End : 0x1FFFF, FAT2 Start : 0x20000, FAT2 end : 0x2016D
'''
path = r'C:\VSCFULLCAPSC18\VSCFULLCAPSC18.txt'
FWFATstart = 94830
FWFATend = 131439
FWDIRstart = FWFATend + 1
FWDIRend = 2097151
fd = open(path)
for line in fd:
	if 'FAT1 address' in line:
		logging.info(line.split(':')[-2:])
		FAT1addr = line.split(':')[-1].strip('\n\r')
		FAT1addrint = int(FAT1addr,16)
		print line
	if 'FAT2 address' in line:
		logging.info(line.split(':')[-2:])
		FAT2addr = line.split(':')[-1].strip('\n\r')
		FAT2addrint = int(FAT2addr, 16)
		print line
	if  'DIR address' in line:
		logging.info(line.split(':')[-2:])
		DIRaddr = line.split(':')[-1].strip('\n\r')
		DIRaddrint = int(DIRaddr, 16)
		print line
print 'done'