import datetime
import os
import schedule
import time
from Crawler.repository.databasehandler import db_handler


class CrawlManager:
    __instance = None

    @staticmethod
    def getInstance():
        if CrawlManager.__instance is None:
            CrawlManager()
        return CrawlManager.__instance

    def __init__(self):
        self.names = []
        self.rows_num = 15000
        self.command = 0
        self.isCrawling = False
        self.is_update = True
        if CrawlManager.__instance is None:
            CrawlManager.__instance = self

    def set_end_crawl(self):
        self.isCrawling = False

    def set_start_crawl(self):
        self.isCrawling = True

    def wait_for_crawl(self):
        while self.isCrawling:
            time.sleep(1)

    def get_command(self):
        if db_handler.is_empty():
            db_handler.init_database()
            print("Database Is Empty, Do You Want To Update Information?" +
                  " This Might Take About 15 Minutes. (Please Type Y or N)")
            if input() == 'Y':
                print("Crawling Information.")
                self.rows_num = 15000
                return 1, None

        command = ""
        print("Please Enter Your Command: ")
        print("Type full-update To Update All Data Until Today.")
        print("Type get-json To Get A Json File From A Specific Date.")
        print("Type start-update To Start Daily Update.")
        print("Type exit To Exit The Program.")
        command = input()
        if command == "exit":
            return -1, None
        elif command == 'get-json':
            print("Please Enter Your Date. (for example: 2020/10/21)")
            date = input()
            date = date.replace('\\', '')
            date = date.replace('/', '')
            date = date.replace('-', '')
            return 2, date
            # get info from db and save to a json file
        elif command == 'start-update':
            return 3, None
