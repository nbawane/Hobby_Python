from os import path

filepath = r'C:\Users\34806\Desktop\LSV71\VSCFULLCAPSC61.txtLSV71_Seq_Rand_ReadWrites_CQLegacy_20180119_185347.log'
fd = open(filepath)

dividelogpath = r'C:\DivideLog'


index = 0
for line in fd:
	destlog = 'file'+str(index)
	dividefd = open(dividelogpath)
