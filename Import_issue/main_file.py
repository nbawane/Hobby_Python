"""
.pyc file is also executable file so whether it imports py or pyc
code works fine
"""

print "main_file started"
importFile = "sub_file"
obj = __import__(importFile)
obj.getdata()