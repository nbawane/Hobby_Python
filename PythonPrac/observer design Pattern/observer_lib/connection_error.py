POCKETBITS = 'https://pocketbits.in/api/ticker'

import requests
try:
	d = requests.get(POCKETBITS)
except requests.exceptions.ConnectionError:
	print('cconnection error')
# print(d)