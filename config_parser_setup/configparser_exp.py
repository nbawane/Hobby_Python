import ConfigParser
import os
configpath = r'C:\Hobby_codes\Hobby_codes\config_parser_setup\configfile.txt'

config = ConfigParser.ConfigParser()
config.read(configpath)
sectionlist = config.sections()	#to get section headings in config file
for sectionname in sectionlist:	#parsing through the sections
	print "section : %s"%sectionname
	optionlist = config.options(sectionname)	#get the options under the section specified
	print optionlist
	items = config.items(sectionname)			#get the the options with value un der the section
	for name,value in items:
		print "%s : %s"%(name,int(value))
print __file__									#get he current file name
print os.path.basename(__file__)				#get the current filename with out path