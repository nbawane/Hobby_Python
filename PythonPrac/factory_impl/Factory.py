#to read from txt,csv, xlsx -> input family
#output to xlsx,txt,csv -> output family
from openpyxl import load_workbook
import csv

class Inputs:
	@staticmethod
	def create_input(file_name):
		ext = file_name.split('.')[-1]
		if ext.lower() in['txt','log'] :
			return text_input(file_name)
		elif ext.lower() =='csv':
			return csv_input()
		elif ext.lower() == 'xlsx':
			return xlsx_input()

class text_input:
	'''
	instantiate with file descripter
	'''
	def __init__(self,file_name):
		self.fd = open(file_name)

class csv_input:
	def __init__(self,file_name):
		fd = open(file_name)

class xlsx_input:
	def __init__(self,file_name):
		fd = load_workbook(file_name)

file = 'C:\Lambaeu_Validation\lsv.log'

input_instance =  Inputs.create_input(file)
print(input_instance.fd)

