import logger.logger as logger

filepath = r'C:\LSV3\LSV3_ActiveWearLeveling_20180322_172734_2892.log'
parselog = r'C:\LSV3_12D\LSV3_parsedlog.txt'

def parse(filepath,parselog):
	fd = open(filepath)
	hotcountlogflag = False
	logging = logger.log(parselog)
	for line in fd:
		if 'finished subcycle' in line or 'Full cycle write complete' in line or 'Hottest block' in line:
			logging.Info(line)
			hotcountlogflag = True
		if hotcountlogflag and '{' in line:
			logging.Info('####  Hotcount')
			logging.Info(line)
			hotcountlogflag = False
			logging.Info('='*200)
parse(filepath,parselog)