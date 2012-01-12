import re
from math import sqrt

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector

from hnconf.items import HNItem

def strip_tags(value):
	"""Returns given HTML with all tags stripped."""
	return re.sub(r'<[^>]*?>', '', value)

def confidence(ups, downs):
	"""Lower bound of Wilson score confidence interval for a Bernoulli parameter
	Here we assume num comments = negative signal
	"""
	n = ups + downs

	if n == 0:
	    return 0

	z = 1.6 #1.0 = 85%, 1.6 = 95%
	phat = float(ups) / n
	return sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)

class HNSpider(CrawlSpider):
	"""Spider class, used by Scrapy
	"""
	name = "hnconf"
	allowed_domains = ["news.ycombinator.com"]
	start_urls = [
		"http://news.ycombinator.com/",
	]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)

		# returns <a> tags
		titles = hxs.select("/html/body/center[1]/table[1]/tr[3]/td[1]/table[1]/tr/td[contains(concat(' ',@class,' '),' title ')]/a[1]").extract()
		links = hxs.select("/html/body/center[1]/table[1]/tr[3]/td[1]/table[1]/tr/td[contains(concat(' ',@class,' '),' title ')]/a/@href").extract()
		# returns spans
		votes = hxs.select("/html/body/center[1]/table[1]/tr[3]/td[1]/table[1]/tr/td[contains(concat(' ',@class,' '),' subtext ')]/span[1]").extract()
		# returns <a> tags
		comments = hxs.select("/html/body/center[1]/table[1]/tr[3]/td[1]/table[1]/tr/td[contains(concat(' ',@class,' '),' subtext ')]/a[2]").extract()

		selfpost = re.compile('^item\?id=\d+')
		items = []
		averages = []
		x = 0
		for vote in votes:
			if selfpost.match(links[x]):
				linky = u"http://news.ycombinator.com/%s" % links[x]
				title = u'<a href="%s">%s<a>' % (linky, strip_tags(titles[x]))
			else:
				title = titles[x]

			comm = strip_tags(comments[x]).split(' ')[0]
			down = int(comm) if comm != "discuss" else 0
			up = int(strip_tags(vote).split(' ')[0])

			item = HNItem()
			item['title'] = title
			item['site'] = links[x]
			item['vote'] = up
			item['comment'] = down
			item['score'] = confidence(up, down)
			items.append(item)
			x = x+1

		sorted_items = sorted(items, key=lambda item: item['score'])
		sorted_items.reverse()
		return sorted_items


