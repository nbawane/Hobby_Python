#This is a Script to run the test suit sequentially for particular amount of time or till they pass or fail

import os

class automate:
	
	def Run(self,home):
		self.home = home
		os.chdir(self.home)
		print "current dir is %s"%os.getcwd()
		os.system('setenv.bat')
		os.system('testrunner.py')
		
	def Main(self):
		
		SDDVT_home = "C:\Program Files (x86)\SanDisk\SDDVT_Python_Package\SDDVT_Python_Package\SDDVT"
		EnvVar = 'C:\Program Files (x86)\SanDisk\SDDVT_Python_Package\SDDVT_Python_Package\SDDVT\setenv.bat'
		
		self.Run(SDDVT_home)

obj = automate()
obj.Main()

