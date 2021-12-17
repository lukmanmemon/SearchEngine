from scrapy.linkextractors import LinkExtractor
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from w3lib.url import url_query_cleaner
import extruct
import os.path


def process_links(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link

class WebSpider(CrawlSpider):
    name = 'web_spider'
    allowed_domains = ['ryerson.ca', 'utoronto.ca', 'utm.utoronto.ca', 'utsc.utoronto.ca/home', 'yorku.ca', 'yorku.ca/glendon', 'ocadu.ca']
    start_urls = ['https://www.utoronto.ca/', 'https://www.yorku.ca/', 'https://www.ryerson.ca/', 'https://www.ocadu.ca/', 'https://www.utsc.utoronto.ca/home/', 'https://www.utm.utoronto.ca/', 'https://www.yorku.ca/glendon/']
    BASE_URL = 'https://ryerson.ca' 
    custom_settings = {
        'ROBOTSTXT_OBEY': 'True',
        'CLOSESPIDER_PAGECOUNT': '1000',
        'HTTPCACHE_ENABLED': 'False',
        'COOKIES_ENABLED': 'False',
        'LOG_ENABLED': 'False',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html',
            'Accept-Language': 'en',
        },
    }
    rules = (
        Rule(
            LinkExtractor(),
            process_links=process_links,
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        return {
            'url': response.url,
            'text': response.css("::text").extract(),
            'title': response.css('title::text').extract(),
            'metadata': extruct.extract(
                response.text,
                response.url,
                syntaxes=['opengraph', 'json-ld']
            ),
        }

# Erase file content if file exists
if os.path.exists('items.json'):
    file = open('items.json', "r+")
    contents = file.read().split("\n")
    file.seek(0)                        
    file.truncate()

process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

process.crawl(WebSpider)
process.start() # the script will block here until the crawling is finished



