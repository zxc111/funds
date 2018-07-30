# -*- coding: utf-8 -*-

import logging

from scrapy import Spider
from funds.models.db import InitDB
from funds.models.funds import Fund, FundStatistics


class BaseSpider(Spider):

    def __init__(self, env="dev"):
        self.db = InitDB(env)

    def save(self, obj):
        session = self.session
        session.add(obj)
        try:
            session.commit()
        except Exception as e:
            logging.error(e, exc_info=True)
            session.rollback()
        session.close()

    def multi_save(self, obj_list):
        if not obj_list:
            return
        session = self.session
        try:
            session.bulk_save_objects(obj_list)
            session.commit()
        except Exception as e:
            logging.error(e)
            session.rollback()
        session.close()
        

    @property
    def session(self):
        return self.db.Session()

    def get_exist_fundcode_list(self, fund_list):
        session = self.session
        res = Fund.get_exist_fundcode_list(
            fund_list,
            session
        )
        session.close()
        return res

    def get_fundcode_list(self):
        session = self.session
        res = Fund.get_fundcode_list(session)
        session.close()
        return res

    def get_exist_fundcode_date_list(self, fundcode):
        session = self.session
        res = FundStatistics.get_exists_date_list(session, fundcode)
        session.close()
        return res
