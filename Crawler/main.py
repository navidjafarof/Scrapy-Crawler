
from Crawler.spiders.fipiran import FipiranSpider
from Crawler.crawlmanager.manager import CrawlManager
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner

manager = CrawlManager.getInstance()
names = []
row_num = 0
process = CrawlerProcess()



# def start_crawler(spider_name):
#     process = CrawlerProcess(get_project_settings())
#     process.crawl()
#     process.start(stop_after_crawl=True)
# def run_spider(spider_name):
#     crawler = CrawlerRunner(get_project_settings())
#     crawler.crawl(spider_name, domain='fipiran.com')


def auto_update():
    print("")
    # main.row_num = (todays date - last update date)
    # run_spider('price_history')


def main():
    print("Welcome To Fipiran Website Crawler.")
    process.crawl(FipiranSpider)
    process.start()



if __name__ == "__main__":
    main()