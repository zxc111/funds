# coding: utf8

from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.schema import UniqueConstraint

from .config import Base


class Fund(Base):

    __tablename__ = "funds"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    fundcode = Column(String(32), unique=True)
    manager = Column(String(32))

    @classmethod
    def get_exist_fundcode_list(cls, fundcode_list, session):
        if not fundcode_list:
            return fundcode_list
        fc_set = set(fundcode_list)
        res = session.query(cls.fundcode).filter(
            cls.fundcode.in_(fundcode_list)
        ).all()
        result = []
        for fundcode in res:
            result.append(fundcode[0])
        return result

    @classmethod
    def get_fundcode_list(cls, session):
        res = session.query(cls.fundcode).all()
        return [i[0] for i in res]


class FundStatistics(Base):

    __tablename__ = "fund_statistics"

    id = Column(Integer, primary_key=True)
    fundcode = Column(String(32))
    net_asset_value = Column(Integer)  # 单位净值
    cumulative_net_value = Column(Integer)  # 累计净值
    grown_rate = Column(Float)
    date = Column(Date)

    __table_args__ = (
        UniqueConstraint('fundcode', 'date', name='unique'),
    )

    @classmethod
    def get_exists_date_list(cls, session, fundcode):
        res = session.query(cls.date).filter(
            cls.fundcode==fundcode,
        ).all()
        return [i[0] for i in res]
