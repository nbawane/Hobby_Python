import os
path = r"C:\CQ_implementation\SD_CQ\SD\CommonDVT\CQ_Validation\Stress_Tests"

WithoutExtenssion = True
outputlist = True
output = []
dirs = os.listdir(path)
if WithoutExtenssion:
	for file in dirs:
		filename=os.path.splitext(file)[0]
		if outputlist:
			output.append(filename)
		else:
			print filename

if outputlist:
	print output
else:
	dirs