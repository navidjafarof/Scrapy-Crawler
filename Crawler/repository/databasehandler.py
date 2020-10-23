from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Crawler.model.schemas import Stock, StocksDailyInfo, base
import json
from Crawler.model.utils import build_alchemy_encoder


def is_date_after(date1, date2):
    a = int(date1)
    b = int(date2)
    return date1 >= date2


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

    def add_stock(self, stock):
        if self.session.query(Stock).filter_by(name=stock.name).scalar() is not None:
            return self.session.query(Stock).filter_by(name=stock.name).first().id
        else:
            self.session.add(stock)
            self.session.commit()
            return stock.id

    def add_info_for_stock(self, stock_id, info):
        stock = self.session.query(Stock).get(stock_id)
        if len(list(filter(lambda inf: inf.gDate == info.gDate, stock.stock_daily_infos))) == 0:
            stock.stock_daily_infos.append(info)
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

    def get_infos_by_date(self, date):

        data = self.session.query(StocksDailyInfo).filter(StocksDailyInfo.gDate == date).all()
        json_string = json.dumps(data, cls=build_alchemy_encoder(), check_circular=False, ensure_ascii=False).encode(
            'utf8').decode()
        return json_string

    def is_empty(self):
        return len(self.get_stocks()) == 0


db_handler = DataBaseHandler()
db_handler.init_database()
