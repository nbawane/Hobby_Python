import sys
import traceback
def exception_function(etype, value, trace):
	print(etype)
	print(value)
	print(trace)
	print(traceback.format_exception(etype,value,trace))
sys.excepthook = exception_function
a = 9/0


