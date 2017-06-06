#renaming files in a folder

import os

path = r'C:\Training\file_rnm'
temp1 = 'python_[chapter'
temp2 = ']_log'
file_list =  os.listdir(path)
l = len(file_list)
for i in range(l):
	print file_list[i]
	

def file_name_generator():
	for i in range(l):
		name = temp1+str(i)+temp2
		src = path+'\\'+file_list[i]
		print "%s  %s  %s"%(name,file_list[i],src)
		os.rename(src,name)
file_name_generator()