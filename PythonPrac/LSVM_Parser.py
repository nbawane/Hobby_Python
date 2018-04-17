import os
import logging
import ntpath
import LSV3

print ('LSVM parser')

name = input("Enter LSVM log with path to parser : ")
#Model script divides huge log in number of pieces
#to parse these pieces this log parser will help
filepath,filename = ntpath.split(name)  #extract filename and filepath

filelist = os.listdir(filepath) #get files from dir

parselog = []
last = 0
lastfile=filename
for files in filelist:
    
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
        for line in fd:
            if 'Cycle count' in line:
                print(line)
                
print ('last file : %s'%last)
fd = open(lastfile)




