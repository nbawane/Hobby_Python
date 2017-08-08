import xlwt
import re
from os import listdir, path

'''
To Do 	  : handle If script is failed in log
'''


class XlsOpt:
	def __init__(self):
		self.wb = xlwt.Workbook()
		self.sheet = self.wb.add_sheet("Sheet1")

	def write_at_location(self, row, column, data):
		self.sheet.write(row, column, data)

	def save_file(self, xlsname):
		#op xls name will be same as input text file name
		xlsname = xlsname + '.xls'
		self.wb.save(xlsname)


class FileOpt:
	def __init__(self):
		self.logfolder = "C:\Results\cq_test"	#log folder with the desired logs to be parsed
		self.log = listdir(self.logfolder)
		self.glob_dict = {'Start Block Address': None, 'Priority': None, 'Direction': None, 'TaskID': None,
						  'NumBlocks': None}
		self.excelopt = XlsOpt()
		self.write_header()
		self.rownum = 0
		self.scriptnamecolumn = 0
		self.iterationnumcol = 1
		self.taskidcol = 2
		self.addrcol = 3
		self.lengthcol = 4
		self.directioncol = 5
		self.prioritycol = 6
		self.scriptnamestartrow = 0
		self.scriptnameendrow = 0
		self.scriptnamelist = []
		self.scriptnameflag = 0
		self.iterationnumlist = []
		self.iterationnumstartrow = 0
		self.iterationnumendrow = 0
		self.iterationnumflag = 0

	def parser(self):

		for file in self.log:
			self.__init__()  # reinitialize all the variables
			self.rownum += 1  # incremented because of header
			print "processing file : %s" % file
			self.xlsname = str(file.split('.')[0])
			file = path.join(self.logfolder, file)
			with open(file) as fd:
				for line in fd:
					print line
					if 'Started' in line:
						self.write_script_name_merge_rows(line)
					'''add all the failure strings here to log in xls sheet'''

					if 'Failed Running script' in line or "Failed to Import" in line :
						self.excelopt.sheet.write_merge(self.rownum,self.rownum,self.taskidcol,self.prioritycol,"****TEST FAILED****")
						self.rownum+=1
						continue
					if 'ITERATION' in line:
						self.write_iteration_name_merge_rows(line)

					if ('CQTaskInformation' in line) or ('CQStartBlockAddr' in line):
						taskInformation = line[line.rfind('[') + 1:line.rfind(']')]
						tasksplit = taskInformation.split(',')
						self.info_dict = {(i.split(':')[0]).strip(' '): (i.split(':')[1]) for i in tasksplit}
						self.glob_dict.update(self.info_dict)
						if 'CQStartBlockAddr' in line:
							# print self.glob_dict
							self.log_data(self.rownum)
							self.rownum += 1
				else:
					# this else is for loop, to handle endof file corner case
					self.write_script_name_merge_rows('EOF')
					self.write_iteration_name_merge_rows('EOF')
					self.excelopt.save_file(self.xlsname)

				# print self.glob_dict['TaskID'],self.glob_dict['Start Block Address']
			print "Done with : %s" % file
			self.rownum = 0

	def log_data(self, row):
		self.write_task_id(row, self.glob_dict['TaskID'])
		self.write_addr(row, self.glob_dict['Start Block Address'])
		self.write_length(row, self.glob_dict['NumBlocks'])
		self.write_direction(row, self.glob_dict['Direction'])
		self.write_priority(row, self.glob_dict['Priority'])
		self.excelopt.save_file(self.xlsname)

	def write_task_id(self, row, task_id):
		print 'in writetask %s'%row
		self.excelopt.write_at_location(row, self.taskidcol, int(task_id))

	def write_addr(self, row, addr):

		self.excelopt.write_at_location(row, self.addrcol, addr)

	def write_length(self, row, length):
		self.excelopt.write_at_location(row, self.lengthcol, int(length))

	def write_direction(self, row, direction):
		if int(direction):
			dirc = 'Read'
		else:
			dirc = 'Write'
		self.excelopt.write_at_location(row, self.directioncol, dirc)

	def write_priority(self, row, priority):
		if int(priority):
			pri = 'High'
		else:
			pri = 'Low'
		self.excelopt.write_at_location(row, self.prioritycol, pri)

	def write_header(self):
		header = ['Script_Name', 'ITERATION', 'TaskID', 'Start Block Address', 'NumBlocks', 'Direction', 'Priority']
		for column, key in enumerate(header):
			self.excelopt.write_at_location(0, column, key)

	def write_script_name_merge_rows(self, line):
		if line is 'EOF':
			pass
		else:
			self.scriptnamelist.append((line.rstrip()).split(' ')[-1])
		if self.scriptnameflag == 0:
			self.scriptnamestartrow = self.rownum
		if self.scriptnameflag == 1:
			self.scriptnameendrow = self.rownum - 1
			print "startrow : %s,endrow : %s"%(self.scriptnamestartrow,self.scriptnameendrow)
			self.excelopt.sheet.write_merge(self.scriptnamestartrow, self.scriptnameendrow, self.scriptnamecolumn,
											self.scriptnamecolumn, self.scriptnamelist[0])
			del self.scriptnamelist[0]
			self.scriptnamestartrow = self.scriptnameendrow + 1
		self.scriptnameflag = 1

	def write_iteration_name_merge_rows(self, line):
		if line is 'EOF':
			pass
		else:
			self.iterationnum = re.search('(?<=ITERATION )[0-9]', line)
			self.iterationnumlist.append(self.iterationnum.group())
		if self.iterationnumflag == 0:
			self.iterationnumstartrow = self.rownum
		if self.iterationnumflag == 1:
			self.iterationnumendrow = self.rownum - 1
			print 'startitercol : %s, endrowiter : %s'%(self.iterationnumstartrow,self.iterationnumendrow)
			self.excelopt.sheet.write_merge(self.iterationnumstartrow, self.iterationnumendrow, self.iterationnumcol,
											self.iterationnumcol, int(self.iterationnumlist[0]))
			del self.iterationnumlist[0]
			self.iterationnumstartrow = self.iterationnumendrow + 1
		self.iterationnumflag = 1


if __name__ == '__main__':
	fileobj = FileOpt()
	fileobj.parser()
