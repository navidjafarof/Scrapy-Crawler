from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Crawler.model.schemas import Stock, StocksDailyInfo, base
import json
from Crawler.model.utils import build_alchemy_encoder


class DataBaseHandler:
    session = None

    def init_database(self):
        engine = create_engine('sqlite:///fipiran.db')
        session_class = sessionmaker(bind=engine)
        self.session = session_class()
        base.metadata.create_all(engine)

    def add_all(self, items):
        self.session.add_all(items)
        self.session.commit()

    def add(self, item):
        self.session.add(item)
        self.session.commit()

    def add_info_for_stock(self, stock_id, info):
        x = self.session.query(Stock).get(stock_id)
        x.stock_daily_infos.append(info)
        self.session.commit()

    def get_infos(self):
        return self.session.query(StocksDailyInfo).all()

    def get_stocks(self):
        return self.session.query(Stock).all()

    def get_database_json(self):
        stock_list = []
        for stock in self.get_stocks():
            stock_list.append(stock)
        data = {"stocks": stock_list}
        json_string = json.dumps(data, cls=build_alchemy_encoder(), check_circular=False, ensure_ascii=False).encode(
            'utf8').decode()
        return json_string


db_handler = DataBaseHandler()
db_handler.init_database()
