import os
import ConfigParser

configpath = r'C:\Hobby_codes\Hobby_codes\config_parser_setup\configfile.txt'
currentfilename = os.path.basename(__file__)
currentfilename,currentfileext = os.path.splitext(currentfilename)
executescript = []
print currentfilename
CallAllObj = ConfigParser.ConfigParser()
CallAllObj.read(configpath)
Sectionlist = CallAllObj.sections()
for section in Sectionlist:
	print section
	if currentfilename == section:
		items = CallAllObj.items(section)
		for scriptname,flag in items:
			print "%s : %d"%(scriptname,int(flag))
			if int(flag)==1:
				executescript.append(scriptname)
print executescript
