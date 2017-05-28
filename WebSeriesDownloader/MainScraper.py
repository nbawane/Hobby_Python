from bs4 import BeautifulSoup as bs
import urllib2
search_query = 'index+of+originals'
google_search_url = 'http://www.google.com/search?q'
full_search_url = google_search_url+'='+search_query
webobj = urllib2.urlopen(google_search_url)
soup = bs(webobj,'lxml')
print "type soup %s"%type(soup)
alla = soup.find_all('a')
for linkattributes in alla:
	print linkattributes