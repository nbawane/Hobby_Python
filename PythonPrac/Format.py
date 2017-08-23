'''
format functionality cheat code
'''

print '{} {}'.format('one','two')	#one two
print '{1} ** {0}'.format('abra','dabra')	#dabra ** abra,can be printed by index
print '{:10}:{:>10}'.format('key','value')	#key       :     value

d = {
	'function one':'Special function one',
	 'function two':'Special function two',
	 'function three':'Special function three',
	 'function thrree':'Special function thrree',
	 'function ofour':'Special function four',
	 'function fice':'Special function fice',
	'1':1
	 }
print d
for key,values in d.items():
	# vallen = str(len(values)+10)
	print '{:20}:{:>40}'.format(key, values)
