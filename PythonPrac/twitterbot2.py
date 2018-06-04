import requests
import base64

Consumer_Key = 'NiBKgW5YIu2TKm3kJE4RZKRXz'
Consumer_Secret = '8ZPCDCTREa6DF4tm7NpInP1iDq9a7bkPIBQRVyH2Q1cBlLqPHo'
base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

key = '{}:{}'.format(Consumer_Key, Consumer_Secret).encode('ascii')
b64_encoded_key = base64.b64encode(key)
b64_encoded_key = b64_encoded_key.decode('ascii')

header = {'Authorization': 'Basic {}'.format(b64_encoded_key),'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

data = {'grant_type': 'client_credentials'}

auth_resp = requests.post(auth_url, headers=header, data=data)
print(auth_resp)