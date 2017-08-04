#script for launching applications
#import time
from time_dep import *
import os
'''list of tasks to open'''
apps = [
	'start chrome https://mail.google.com/mail/u/0/#inbox',
	'start outlook',
	'start notepad++'
	]
	
print "welcome Mr Nitesh\n%s"%(welcome_message())
if current_wday() not in [6,7] and current_hours() in range(8,19): #condition for weekday operation
	for i in apps:
		print "opening %s"%((i.split()[1]))
		os.system(i)
		time.sleep(8)