#to give time dependency

import time;

localtime = time.localtime(time.time())

welcome_message = ''
def current_wday():
	return localtime.tm_wday
	
def current_hours():
	return localtime.tm_hour
	
def welcome_message():
	if current_hours() in range(6,13):
		return "Good Morning !!:)"
	elif current_hours() in range(13,17):
		return "Good Afternoon !!:)"
	elif current_hours() in range(17,19):
		return	"Good Evening !!"
	else:
		return "not in office...Enjoy.. !!!;)"