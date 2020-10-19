from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Repository.schemas import base, Stock


class DataBaseHandler:
    session = None

    def init_database(self):
        engine = create_engine('sqlite:///fipiran.db', echo=True)
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


db_handler = DataBaseHandler()
db_handler.init_database()
