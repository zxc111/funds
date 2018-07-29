# coding: utf8

from sqlalchemy import Column, Integer, String

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


