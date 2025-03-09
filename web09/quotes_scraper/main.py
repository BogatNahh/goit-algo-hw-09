from scrapy.crawler import CrawlerProcess
from quotes_scraper.spiders.quotes_spider import QuotesSpider

process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()
