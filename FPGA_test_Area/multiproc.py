
	# to test multiprocessing

	import threading
	import time 
	import os

	exitflag = 0

	class Testrun(threading.Thread):
		def __init__(self,threadID,name,delay):
			threading.Thread.__init__(self)
			self.threadID = threadID
			self.name = name
			self.delay = delay
			
		def run(self):
			print 'launching test '+self.name
			launch_test(self.name,self.delay)
			print 'exitiing test '+self.name
			

	def launch_test(threadname,delay):
		os.system('conthello.py')
		if exitflag ==1:
			threadname.exit()
		
	thread = Testrun(1,'test',10)

	thread.start()

		
