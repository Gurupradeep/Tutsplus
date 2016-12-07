from scrapy.spiders import Spider
from tutsplus.items import TutsplusItem
from scrapy.http    import Request
import re

class MySpider(Spider) :
	#setting the inital parameters
	name = "tutsplus"
	allowed_domains = ["code.tutsplus.com"]
	start_urls = ["https://code.tutsplus.com/tutorials"]

	def parse(self, response) :
		links = response.xpath('//a/@href').extract()

		#to store all the crawled links
		crawledLinks = []

		#to get only post pages
		linkPattern = re.compile("^\/tutorials\?page=\d+")

		for link in links :
			if linkPattern.match(link) and not link in crawledLinks :
				link = "http://code.tutsplus.com" + link
				crawledLinks.append(link)
				yield Request(link,self.parse)

		### getting the titles
		titles = response.xpath('//a[contains(@class, "posts__post-title")]/h1/text()').extract()
		for title in titles :
			item = TutsplusItem()
			item["title"] = title
			yield item 	
		