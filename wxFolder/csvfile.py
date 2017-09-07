import csv
import time
filename = r'C:\GoLogicInterpreter\Write Traces\1Z_Trace.CSV'
fd = csv.reader(open(filename))
a=time.time()
for i in fd:
	print i
b=time.time()
print'done ',(b-a)
