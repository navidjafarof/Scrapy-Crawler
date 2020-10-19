from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

base = declarative_base()


class Stock(base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class StocksDailyInfo(base):
    __tablename__ = 'stock_daily_infos'

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey('stocks.id'))

    def __init__(self, info_dict):
        for key in info_dict:
            setattr(self, key, info_dict[key])

    gDate = Column(String)
    DEven = Column(String)
    ZTotTran = Column(Float)
    QTotTran5J = Column(Float)
    QTotCap = Column(Float)
    PClosing = Column(Float)
    PcCh = Column(Float)
    PcChPercent = Column(Float)
    PDrCotVal = Column(Float)
    LTPCh = Column(Float)
    LTPChPercent = Column(Float)
    PriceYesterday = Column(Float)
    PriceMin = Column(Float)
    PriceMax = Column(Float)
    PriceFirst = Column(Float)

    stock = relationship("Stock", back_populates="stock_daily_infos")


Stock.stock_daily_infos = relationship("StocksDailyInfo", order_by=StocksDailyInfo.id, back_populates="stock")


