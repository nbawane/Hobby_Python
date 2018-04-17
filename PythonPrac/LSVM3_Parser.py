import os
import logger.logger as logger
import ntpath


#script should be in the log folder
print ('LSVM parser')
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

name = input("Enter LSVM log with path to parser : ")
#Model script divides huge log in number of pieces
#to parse these pieces this log parser will help
filepath,filename = ntpath.split(name)  #extract filename and filepath

filelist = os.listdir(filepath) #get files from dir
alist = filelist
alist.sort(key=natural_keys)


parselog = []
last = 0
lastfile=filename

parselogresult = r'C:\LSV3\LSV3_hotcountlog1.txt'
logging = logger.log(parselogresult)
alist.reverse()
for files in alist:
    
    if filename in files:
        #filenames are named as
        #LSVM3_ActiiveWearLeveling_20180205_115431_11876.log.1
        #LSVM3_ActiiveWearLeveling_20180205_115431_11876.log.10
        #LSVM3_ActiiveWearLeveling_20180205_115431_11876.log.11
        #LSVM3_ActiiveWearLeveling_20180205_115431_11876.log.12
        #so we search filename in filelist
        print(files)
        try:
            fileseq = int(files.split('.')[-1])
        except ValueError:
            last = 0
        else:
            if fileseq>last:
                last=fileseq
                lastfile = os.path.join(filepath,files)
            
        parsepath  = os.path.join(filepath,files)
        fd = open(parsepath)
        hotcountlogflag = False
        for line in fd:
            if 'finished subcycle' in line or 'Full cycle write complete' in line or 'Hottest block' in line:
                logging.Info(line)
                hotcountlogflag = True
            if hotcountlogflag and '{' in line:
                logging.Info('####  Hotcount')
                logging.Info(line)
                hotcountlogflag = False
                logging.Info('=' * 200)
        for line in fd:
            if 'Cycle count' in line:
                print(line)
                
print ('last file : %s'%last)
fd = open(lastfile)




