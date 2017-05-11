"""
********************************************************************************
* MODULE      : xlsxwt.py
* FUNCTION    : contains the function to write data to .xlsx file in predefined pattern
* PROGRAMMER  : Nitesh Bawane
* DATE(ORG)   : 01/03/2017
* REMARKS     : NA
* COPYRIGHT   : Copyright (C) 2015 SanDisk Corporation
*------------------------------------------------------------------------------*
* Revision History : 1.0
********************************************************************************
"""
import os
import time

Root_dir = r"C:\VCD_Data"
Input_Files = r"C:\VCD_Data\Input_Files"
Output_Files = r"C:\VCD_Data\Output_Files"
default_op_path = r"C:\VCD_Data\Codes"
class DirOperation:
	def __init__(self):
		self.files 		= []
		self.folders 	= []

	def CheckDefaultFolder(self):
		folders = Root_dir,Input_Files,Output_Files
		for folder in folders:
			if not os.path.exists(folder):
				os.mkdir(folder)
				print "%s created"%folder

	def GetInputFiles(self):
		self.files = [dumps for dumps in os.listdir(Input_Files) if dumps.endswith('.txt')]
		print self.files
		return self.files

	def MoveInputFilesToFolder(self):
		"""
		Moves all Input files to timestamped folder in inputfiles folders
		:return: nan
		"""
		folder_name = time.strftime("%Y%m%d")
		file_name = time.strftime('_%Y%m%d_%H%M%S')
		folders = [dumps for dumps in os.listdir(Input_Files) if os.path.isdir(os.path.join(Input_Files,dumps))]


		if folder_name not in folders:
			os.mkdir(os.path.join(Input_Files,folder_name))
		for file in self.files:
			src = os.path.join(Input_Files,file)
			file = file.split('.txt')[0]
			file = file+file_name+'.txt'
			dest = os.path.join(Input_Files,folder_name,file)
			os.rename(src,dest)

	def MoveOutputFiles(self):
		folder_name = time.strftime("%Y%m%d")

		folders = [folder for folder in os.listdir(Output_Files) if os.path.isdir(os.path.join(Output_Files,folder))]
		if folder_name not in folders:
			os.mkdir(os.path.join(Output_Files, folder_name))

		xlsx_files = [xls for xls in os.listdir(default_op_path) if xls.endswith(".xlsx")]

		for filename in xlsx_files:
			src = os.path.join(default_op_path,filename)
			dest = os.path.join(Output_Files,folder_name,filename)
			os.rename(src,dest)
#inst = DirOperation()
# inst.CheckDefaultFolder()
# inst.GetInputFiles()
# inst.MoveInputFilesToFolder()
#inst.MoveOutputFiles()