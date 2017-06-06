#script to update the program 
'''
1. delete all files from folder 1 
2. move files from folder 2 to folder 1
'''

import shutil
import os
import stat

dir1 = r"C:\Python27\San_py\test_folder1"	#folder1
dir2 = r"C:\Python27\San_py\test_folder2"	#folder2

perm = os.stat(dir1)
print "perm ",perm

dir1_files = os.listdir( dir1 )	#listing files in source(folder1)
dir2_files = os.listdir( dir2 ) #listing files in dest(folder2)

sq= '\\'

for i in dir1_files:
	os.remove(dir1+sq+i)
	print "removed ",i	#to remove the files present in dst 

for i in dir2_files:
	print "copying %s from folder1 to folder2"%i
	shutil.copyfile(dir1,dir2+sq+i)

