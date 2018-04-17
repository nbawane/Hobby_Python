import ConfigParser
config = ConfigParser.ConfigParser()
config.read('memorytypes.ini')
dict0 = {}
sectionlist= config.sections()	#get all the sections
optionlist = config.options(sectionlist[0])	#get all the fields in sections

while True:
	for option in optionlist:
		dict0[option] = config.get(sectionlist[0],option)
	print dict0


