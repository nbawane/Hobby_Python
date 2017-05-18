"""
.pyc file is also executable file so whether it imports py or pyc
code works fine
"""
import sys
print "main_file started"
importFile = "sub_file"
obj = __import__(importFile)
obj.getdata()
del sys.modules['sub_file']#this is to remove the subfile module which was chached in sys.module
# print i
# del i['sub_file']
# # print type(i)
# # for t in i:
# # 	print t
i = sys.modules
for t in i:
	print t