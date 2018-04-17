import logging
from os import path,remove

class log:
	def __init__(self,log_file_name):
		"""

		:param log_file_name: this must be the path of log file
		"""
		self.Log_file = log_file_name
		self.init_logger()

	def init_logger(self):
		# print 'logger initiated'
		if path.exists(self.Log_file):
			remove(self.Log_file)
		logging.basicConfig(format='%(message)s',filename=self.Log_file,level=logging.DEBUG)

	def Info(self,stri):
		logging.info(stri)
		print (stri)



