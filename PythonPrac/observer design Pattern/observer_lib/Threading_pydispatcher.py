
from threading import Thread
import  time


class Connection:

	def try_conncet(self):
		try:
			a=3
			b=a/0
		except Exception as a:
			print('zero')
			time.sleep(3)
			dispatcher.send(signal='except')


class getcon:
	def __init__(self):
		dispatcher.connect(self.info,signal='except')
		print('get con')

	def info(self,msg=None):
		print(msg)
		print('event captured')


getcon()

a = Connection()
a.try_conncet()
# getcon()




