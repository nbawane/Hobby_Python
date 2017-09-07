import pandas
filename = r'C:\GoLogicInterpreter\BICS_trace_128Gb.csv'
import time
c=time.time()
df = pandas.read_csv(filename, sep=',')
print list(df.columns.values)
# data = df.values
#
# a = time.time()
# for i in data:
# 	# for j in i:
# 	# 	print j
# 	print i
# b=time.time()
# print 'done',(b-a)
# print 'total',(b-c)
# print data
# print type(data)