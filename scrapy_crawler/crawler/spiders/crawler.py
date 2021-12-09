from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner
import extruct

# Remove query strings from URLs to limit number of requests
def process_links(links):
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link

class WebSpider(CrawlSpider):
    name = 'web_spider'
    start_urls = ['https://www.ryerson.ca/', 'https://www.yorku.ca/', 'https://www.utoronto.ca/']
    custom_settings = {
        'ROBOTSTXT_OBEY': 'True',
        'CLOSESPIDER_PAGECOUNT': '20',
        'HTTPCACHE_ENABLED': 'False',
        'COOKIES_ENABLED': 'False',
        'LOG_ENABLED': 'True',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html',
            'Accept-Language': 'en',
        },
    }
    rules = (
        Rule(LinkExtractor(), 
        process_links=process_links,
        callback='parse_item',
        follow=True
        ),
    )
    
    # Get specified data for each web page
    def parse_item(self, response):
        return {
            'url': response.url,
            'metadata': extruct.extract(
                response.url,
                response.text,
                syntaxes=['opengraph']
            ),
            'text': response.css("::text").extract(),
        }

process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

process.crawl(WebSpider)
process.start() # the script will block here until the crawling is finished



