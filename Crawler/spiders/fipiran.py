import scrapy
import Crawler.utils as ut
from html_table_extractor.extractor import Extractor
import json
from Crawler.repository.databasehandler import db_handler
from Crawler.model.schemas import Stock, StocksDailyInfo


class FipiranSpider(scrapy.Spider):
    name = 'fipiran'
    first_page_url = 'http://www.fipiran.com/Market/LupBourse'
    complex_urls = []

    def start_requests(self):
        yield scrapy.Request(url=self.first_page_url, callback=self.parse_stock_names)

    def parse_stock_names(self, response):
        response_string = response.body.decode("utf-8")
        extractor = Extractor(response_string[response_string.index("<table"): response_string.index("</table>")])
        extractor.parse()
        names = [row[0] for row in extractor.return_list()]
        for name in names:
            stock = Stock(name=name)
            db_handler.add(stock)
            url = ut.crawl_url_generator(name, 1, 1)
            yield scrapy.Request(url=url, callback=self.make_stock_info_parser(stock.id))

    @staticmethod
    def make_stock_info_parser(stock_id):
        def parse(response):
            infos = json.loads(response.body)['data']
            for info in infos:
                info["stock_id"] = stock_id
                info_object = StocksDailyInfo(info)
                db_handler.add_info_for_stock(stock_id, info_object)

        return parse
