import scrapy
import Crawler.utils as ut
import schedule
import time
from html_table_extractor.extractor import Extractor
import json
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from Crawler.repository.databasehandler import db_handler
from Crawler.model.schemas import Stock, StocksDailyInfo
from Crawler.crawlmanager.manager import CrawlManager

manager = CrawlManager.getInstance()


class FipiranSpider(scrapy.Spider):
    name = 'fipiran'
    first_page_url = 'http://www.fipiran.com/Market/LupBourse'
    complex_urls = []

    def start_requests(self):
        command, options = manager.get_command()
        # manager.rows_num = 1
        if command == 1:
            manager.set_start_crawl()
            manager.rows_num = 15000
            yield scrapy.Request(url=self.first_page_url, callback=self.parse_stock_names)
        elif command == 2:
            date = options
            jsonString = db_handler.get_infos_by_date(date)
            print('JSON: ', jsonString)
        elif command == 3:
            selected_time = options
            manager.rows_num = 1
            manager.is_update = True
            yield scrapy.Request(url=self.first_page_url, callback=self.parse_stock_names)
            # schedule.every().day.at(selected_time).do(self.request_infos_daily)
            # self.request_infos_daily()


        else:
            print("BYE.")



    def parse_stock_names(self, response):
        response_string = response.body.decode("utf-8")
        extractor = Extractor(response_string[response_string.index("<table"): response_string.index("</table>")])
        extractor.parse()
        names = [row[0] for row in extractor.return_list()]
        print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
        self.request_infos_by_names(names, True)

    def make_stock_info_parser(self, stock_id, is_last, is_update=False):
        print("AAAAAAAAAAAAAaaa")
        def parse(response):
            infos = json.loads(response.body)['data']
            for info in infos:
                info["stock_id"] = stock_id
                info_object = StocksDailyInfo(info)
                db_handler.add_info_for_stock(stock_id, info_object)
        if is_update:
            # time.sleep(24 * 3600 * 1)
            time.sleep(10)
            yield scrapy.Request(url=self.first_page_url, callback=self.parse_stock_names)
        return parse

    def request_infos_daily(self):
        names =[]
        for stock in db_handler.get_stocks():
            names.append(stock.name)
        print("HEREE 1 ", len(names))
        self.request_infos_by_names(names, False,)

    def request_infos_by_names(self, names, is_adding):

        print("HEREE 1.5 ", len(names),"   ", manager.rows_num)
        for name in names:
            stock = Stock(name=name)
            if is_adding:
                db_handler.add_stock(stock)

            print("HEREE 2 ", len(names))
            url = ut.crawl_url_generator(name, manager.rows_num, 1)
            yield scrapy.Request(url=url, callback=self.make_stock_info_parser(stock.id, name == names[len(names) - 1], manager.is_update))

