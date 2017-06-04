import GoogleSearch


class scraper:
	def __init__(self):
		self.search = GoogleSearch.google()

	def link_selector(self):
		#self.series_name = raw_input("Enter the series you want to download : ")
		self.series_name = 'originals'
		getLinks =  self.search.search(self.series_name)
		#self.search.print_links(getLinks)
		for link in getLinks:
			#self.search.Crawler(link)
			pass


if __name__ == '__main__':
	scraperObj = scraper()
	web_link = scraperObj.link_selector()
