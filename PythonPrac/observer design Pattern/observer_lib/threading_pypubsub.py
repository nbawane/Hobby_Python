from pubsub import pub
from threading import Thread
import time


class CallerThread:

	def senderthread(self):
		# while(1):
			time.sleep(10)
			pub.sendMessage('sM')

class ReceiverThread:
	def __init__(self):
		pub.subscribe(self.getmsg,'sM')

	def getmsg(self):
		print('get msg')

a = CallerThread()
at =  Thread(target=a.senderthread)
at.start()

r = ReceiverThread()


