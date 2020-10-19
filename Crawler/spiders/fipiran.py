import scrapy
import Crawler.utils as ut
from html_table_extractor.extractor import Extractor
import json
import time


class FipiranSpider(scrapy.Spider):
    name = 'fipiran'
    first_page_url = 'http://www.fipiran.com/Market/LupBourse'
    complex_urls = []

    def start_requests(self):
        yield scrapy.Request(url=self.first_page_url, callback=self.parse)

    def parse(self, response):
        if response.url == self.first_page_url:
            response_string = response.body.decode("utf-8")
            extractor = Extractor(response_string[response_string.index("<table"): response_string.index("</table>")])
            extractor.parse()
            names = [row[0] for row in extractor.return_list()]
            for name in names:
                yield scrapy.Request(url=ut.crawl_url_generator(name, 10000, 1), callback=self.parse)
        else:
            print(json.loads(response.body)['data'])

