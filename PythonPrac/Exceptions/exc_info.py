import sys

try:
	raise ZeroDivisionError('Baaam')
except ZeroDivisionError as x:
	print x.args
	print x.message
try:
	try:



import pys