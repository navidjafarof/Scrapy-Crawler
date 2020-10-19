import scrapy
import Crawler.utils as ut
from html_table_extractor.extractor import Extractor
import json
import time
from collections import namedtuple
from Repository.databasehandler import db_handler
from Repository.schemas import Stock, StocksDailyInfo


class FipiranSpider(scrapy.Spider):
    name = 'fipiran'
    first_page_url = 'http://www.fipiran.com/Market/LupBourse'
    complex_urls = []

    def start_requests(self):
        yield scrapy.Request(url=self.first_page_url, callback=self.parser_maker())

    def parser_maker(self, stock_id=0):

        def parse(response):
            if response.url == self.first_page_url:
                response_string = response.body.decode("utf-8")
                extractor = Extractor(
                    response_string[response_string.index("<table"): response_string.index("</table>")])
                extractor.parse()
                names = [row[0] for row in extractor.return_list()]
                for name in names:
                    stock = Stock(name=name)
                    db_handler.add(stock)
                    yield scrapy.Request(url=ut.crawl_url_generator(names[2], 100, 1), callback=self.parser_maker(stock.id))
            else:
                infos = json.loads(response.body)['data']
                for info in infos:
                    info["stock_id"] = stock_id
                    info_object = StocksDailyInfo(info)
                    print("AAAAAAAAAAAAAAAa" , info_object)
                    db_handler.add_info_for_stock(stock_id, info_object)

        return parse
