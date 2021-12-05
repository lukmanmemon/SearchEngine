from scrapy.spiders import CrawlSpider, Rule
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
    start_urls = ['https://www.ryerson.ca/']
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
                response.text,
                response.url,
                syntaxes=['opengraph', 'json-ld']
            ),
        }
