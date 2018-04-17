import ConfigParser

config = ConfigParser.ConfigParser()
filepath = r'C:\Hobby_codes\Hobby_codes\Cryptospace\QAWR_SD_PC2H_1Znm_64Gb_eX2.ini'
config.read(filepath)
options = config.sections()
print options
