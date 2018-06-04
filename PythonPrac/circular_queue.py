import urllib3, json, base64
# CONSUMER_KEY = b'NiBKgW5YIu2TKm3kJE4RZKRXz'
# CONSUMER_SECRET = b'8ZPCDCTREa6DF4tm7NpInP1iDq9a7bkPIBQRVyH2Q1cBlLqPHo'
# # Create a HTTP connection pool manager
# manager = urllib3.PoolManager()
#
# # Set the variable to Twitter OAuth 2 endpoint
# oauth_url = 'https://api.twitter.com/oauth2/token'
#
# # Set the HTTP request headers, including consumer key and secret
# http_headers={'Authorization': "Basic %s" % base64.b64encode(b'NiBKgW5YIu2TKm3kJE4RZKRXz',b'8ZPCDCTREa6DF4tm7NpInP1iDq9a7bkPIBQRVyH2Q1cBlLqPHo'), 'Content-Type': 'application/x-www-form-urlencoded'}
#
# # Set the payload to the required OAuth grant type, in this case client credentials
# request_body="grant_type=client_credentials"
#
# # Send the request
# response = manager.urlopen("POST", oauth_url, headers=http_headers, body=request_body)
#
# # Read the response as JSON
# app_token = json.loads(response.data)

consumer_key = b"YOUR_CONSUMER_KEY_STRING"
consumer_secret = b"YOUR_CONSUMER_SECRET_STRING"

### Get the Access Token

bearer_token = "#{consumer_key}:#{consumer_secret}"
bearer_token_64 = base64.b64encode(bearer_token)