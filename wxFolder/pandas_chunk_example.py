import pandas
import time
filename = r'C:\GoLogicInterpreter\Write Traces\1Z_Trace.CSV'
chunk=10*1000
df = pandas.read_csv(filename,chunksize=chunk)
index=0

for chunks in df:
	# print 'chunk'
	for i in enumerate(chunks.values):
		index +=1
		if index%21000 == 0:
			print time.time()

