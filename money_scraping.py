#Money_scraping

from urllib2 import * 
u = urllib2.urlopen("http://docs.python.org/3.0/library/urllib.request.html")
data = u.read()
print data