Supportbits = True
Readybits = True
StatusReg = 0x53
PDMSbit = 0x80
PSUSbit = 0x20
POFSbit = 0x10
PDMRbit = 0x04
PSURbit = 0x02
POFRbit = 0x01
PMFSupport = {}
PMFReady = {}
if Supportbits:
	SupportStatus = {1: "Supported", 0: "Not Supported"}
	PMFSupport['PDMS'] = SupportStatus[(StatusReg & PDMSbit) >> 6]
	PMFSupport['PSUS'] = SupportStatus[(StatusReg & PSUSbit) >> 5]
	PMFSupport['POFS'] = SupportStatus[(StatusReg & POFSbit) >> 4]
if Readybits:
	ReadyStatus = {1: 'Ready', 0: 'Not Ready'}
	PMFReady['PDMR'] = ReadyStatus[(StatusReg & PDMRbit) >> 2]
	PMFReady['PSUR'] = ReadyStatus[(StatusReg & PSURbit) >> 1]
	PMFReady['POFR'] = ReadyStatus[(StatusReg & POFRbit)]

print PMFSupport.update(PMFReady)
print PMFSupport
print PMFReady