import os
path = r"C:\git_folder\SD_CQ\SD\CommonDVT\CQ_Validation\Abort_Tests"

WithoutExtenssion = True
outputlist = False
output = []
dirs = os.listdir(path)
if WithoutExtenssion:
	for file in dirs:
		filename=os.path.splitext(file)[0]
		if outputlist:
			# #if ('Paral' not in filename) and ('32' not in filename) and ('N' not in filename) and ('Random' not in filename):
			# #if ('Paral' not in filename)and ('Random' not in filename) and ('32' not in filename)and ('N' not in filename) and ('Varied' not in filename):
			# if (('CMD44') not in filename) and (('CMD45') not in filename) and ('32' not in filename) and ('Call' not in filename) and ('Discard' not in filename) and ('Invalid' not in filename):
			output.append(filename)
		else:
			print filename

if outputlist:
	print output
	print len(output)
else:
	dirs