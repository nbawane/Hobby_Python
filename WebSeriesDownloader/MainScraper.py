from bs4 import BeautifulSoup as bs
import urllib2
search_query = 'index+of+originals'
google_search_url = 'http://www.google.co.in/search?q='
full_search_url = google_search_url+search_query
# print full_search_url
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(full_search_url,headers=hdr)
webobj = urllib2.urlopen(req)
soup = bs(webobj,'lxml')
print "type soup %s"%type(soup)
alla = soup.find_all('a')
for linkattributes in alla:
	print linkattributes