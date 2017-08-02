import xlwt
import re


class XlsOpt:
	def __init__(self):
		self.wb 	= xlwt.Workbook()
		self.sheet 	= self.wb.add_sheet("Sheet1")

	def write_at_location(self, row, column, data):
		self.sheet.write(row, column, data)

	def save_file(self):
		'''To do : need to provide name flexibility'''
		self.wb.save("test111.xls")


class FileOpt:
	def __init__(self):
		self.logpath    = "C:\Results\CA11_CQVolParallelism_CallAll_20170801_174508_8476.log"
		self.fd         = open(self.logpath)
		self.glob_dict  = {'Start Block Address':None, 'Priority':None, 'Direction':None, 'TaskID':None, 'NumBlocks':None}
		self.excelopt   = XlsOpt()
		self.rownum     = 0
		self.write_header()
		self.scriptnamecolumn = 0
		self.iterationnumcol  = 1
		self.taskidcol		  = 2
		self.addrcol		  = 3
		self.lengthcol		  = 4
		self.directioncol	  = 5
		self.prioritycol      = 6
		self.scriptname       = None
		self.scriptnamestartrow = 0
		self.scriptnameendrow = 0
		self.scriptnameflag = 0
		self.iterationnumstartrow = 0
		self.intrationnumendrow = 0
		self.iterationnumflag = 0

	def parser(self):
		self.rownum += 1
		for line in self.fd:
			if 'Started' in line:
				self.write_script_name_merge_rows(line)

			if 'ITERATION' in line:
				self.write_iteration_name_merge_rows(line)

			if ('CQTaskInformation' in line) or ('CQStartBlockAddr' in line):
				taskInformation = line[line.rfind('[')+1:line.rfind(']')]
				tasksplit = taskInformation.split(',')
				self.info_dict = {(i.split(':')[0]).strip(' '):(i.split(':')[1]) for i in tasksplit}
				self.glob_dict.update(self.info_dict)
				if 'CQStartBlockAddr' in line:
					print self.glob_dict
					self.rownum += 1
					self.log_data(self.rownum)

					# print self.glob_dict['TaskID'],self.glob_dict['Start Block Address']

	def log_data(self,row):
		self.write_task_id(row, self.glob_dict['TaskID'])
		self.write_addr(row, self.glob_dict['Start Block Address'])
		self.write_length(row,self.glob_dict['NumBlocks'])
		self.write_direction(row, self.glob_dict['Direction'])
		self.write_priority(row, self.glob_dict['Priority'])
		self.excelopt.save_file()

	def write_task_id(self, row ,task_id):
		self.excelopt.write_at_location(row,self.taskidcol,int(task_id))

	def write_addr(self, row, addr):
		self.excelopt.write_at_location(row, self.addrcol, addr)

	def write_length(self, row, length):
		self.excelopt.write_at_location(row, self.lengthcol, int(length))

	def write_direction(self, row, direction):
		self.excelopt.write_at_location(row, self.directioncol, int(direction))

	def write_priority(self,row, priority):
		self.excelopt.write_at_location(row, self.prioritycol, int(priority))

	def write_header(self):
		header = ['Script_Name','ITERATION','TaskID','Start Block Address','NumBlocks', 'Direction','Priority']
		for column,key in enumerate(header):
			self.excelopt.write_at_location(0,column,key)

	def write_script_name_merge_rows(self, line):

		if self.scriptnameflag == 0:
			self.scriptnamestartrow = self.rownum
		if self.scriptnameflag == 1:
			self.scriptnameendrow = self.rownum-1
			self.excelopt.sheet.write_merge(self.scriptnamestartrow,self.scriptnameendrow,self.scriptnamecolumn,self.scriptnamecolumn,self.scriptname)
			self.scriptnamestartrow = self.scriptnameendrow+1
		self.scriptnameflag = 1
		self.scriptname = (line.rstrip()).split(' ')[-1]

	def write_iteration_name_merge_rows(self,line):
		self.iterationnum = re.search('(?<=ITERATION )[0-9]', line)
		self.iterationnum = self.iterationnum.group()
		self.excelopt.write_at_location(self.rownum, self.iterationnumcol, int(self.iterationnum))


if __name__ == '__main__':
	fileobj = FileOpt()
	fileobj.parser()

