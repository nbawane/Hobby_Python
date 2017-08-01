import xlwt


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
		self.logpath    = "C:\Results\CA11_CQVolParallelism_CallAll_20170725_141758_5052.log"
		self.fd         = open(self.logpath)
		self.glob_dict  = {'Start Block Address':None, 'Priority':None, 'Direction':None, 'TaskID':None, 'NumBlocks':None}
		self.excelopt   = XlsOpt()
		self.rownum     = 0
		self.write_header()

	def parser(self):
		for line in self.fd:
			if 'ITERATION' in line:
				self.rownum += 1
				self.excelopt.sheet.write_merge(self.rownum,self.rownum,0,4,line)
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
		self.excelopt.write_at_location(row,0,int(task_id))

	def write_addr(self, row, addr):
		self.excelopt.write_at_location(row, 1, addr)

	def write_length(self, row, length):
		self.excelopt.write_at_location(row, 2, int(length))

	def write_direction(self, row, direction):
		self.excelopt.write_at_location(row, 3, int(direction))

	def write_priority(self,row, priority):
		self.excelopt.write_at_location(row, 4, int(priority))

	def write_header(self):
		header = ['TaskID','Start Block Address','NumBlocks', 'Direction','Priority']
		for column,key in enumerate(header):
			self.excelopt.write_at_location(0,column,key)


if __name__ == '__main__':
	fileobj = FileOpt()
	fileobj.parser()

