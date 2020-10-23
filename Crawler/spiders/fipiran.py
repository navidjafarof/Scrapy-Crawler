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
        if command == 1:
            manager.set_start_crawl()
            manager.rows_num = 30
            manager.is_update = False
            yield scrapy.Request(url=self.first_page_url, callback=self.parse_stock_names,dont_filter=True)
        elif command == 2:
            date = options
            jsonString = db_handler.get_infos_by_date(date)
            with open("report.json", "w") as data_file:
                data_file.write(jsonString)
        elif command == 3:
            selected_time = options
            manager.rows_num = 1
            manager.is_update = True
            yield scrapy.Request(url=self.first_page_url, callback=self.parse_stock_names,dont_filter=True)


        else:
            print("BYE.")

    def parse_stock_names(self, response):
        response_string = response.body.decode("utf-8")
        extractor = Extractor(response_string[response_string.index("<table"): response_string.index("</table>")])
        extractor.parse()
        names = [row[0] for row in extractor.return_list()]
        for name in names:
            time.sleep(1)
            stock = Stock(name=name)
            added_id = db_handler.add_stock(stock)
            url = ut.crawl_url_generator(name, manager.rows_num, 1)
            yield scrapy.Request(url=url, callback=self.make_stock_info_parser(added_id, manager.is_update,
                                                                               name == names[len(names) - 1]), dont_filter=True)

    def make_stock_info_parser(self, stock_id, is_update, is_last):
        def parse(response):
            infos = json.loads(response.body)['data']
            for info in infos:
                info["stock_id"] = stock_id
                info_object = StocksDailyInfo(info)
                db_handler.add_info_for_stock(stock_id, info_object)
            if is_last:
                if is_update:
                    print("WAITING...")
                    time.sleep(3600 * 24 * 1)
                    print("STARTED UPDATE")
                    yield scrapy.Request(url=self.first_page_url, callback=self.parse_stock_names,dont_filter=True)

        return parse
