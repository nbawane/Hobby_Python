import GoogleSearch


class scraper:
	def __init__(self):
		self.search = GoogleSearch.google()
		self.download_links = ''
	def link_selector(self):
		#self.series_name = raw_input("Enter the series you want to download : ")
		self.series_name = 'Friends'	#need to improve case sensetivity
		self.download_links =  self.search.search(self.series_name)
		self.search.Crawler(self.download_links[0])
if __name__ == '__main__':
	scraperObj = scraper()
	web_link = scraperObj.link_selector()
