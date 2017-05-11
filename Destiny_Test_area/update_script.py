#script to update the program 
'''
1. delete all files from folder 1 
2. move files from folder 2 to folder 1
'''

import shutil
import os
import stat

dir1 = r"C:\San_py\f1"	#folder1
dir2 = r"C:\San_py\f2"	#folder2 with files

perm = os.stat(dir1)
print "perm ",perm

dir1_files = os.listdir( dir1 )	#listing files in source(folder1)
dir2_files = os.listdir( dir2 ) #listing files in dest(folder2)
print dir2_files
sq= '\\'
'''
for i in dir2_files:
	os.remove(dir1+sq+i)
	print "removed ",i	#to remove the files present in dst 
'''
for i in dir2_files:
	print "copying %s from folder1 to folder2"%i
	print dir1
	file_path = os.path.join(dir2,i)
	shutil.copyfile(file_path,dir1)

