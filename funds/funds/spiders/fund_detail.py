# -*- coding: utf-8 -*-

import json
import datetime

from scrapy import Request

from base import BaseSpider
from funds.models.funds import Fund, FundStatistics


class Detail(BaseSpider):
    name = 'detail'

    base_url = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?callback=&symbol={}&datefrom=&dateto=&page={}"
    # allowed_domains = ['xincai.xom']
    def start_requests(self):
        fundcode_list = self.get_fundcode_list()
        for fundcode in fundcode_list:
            yield Request(
                url=self.base_url.format(fundcode, 1),
                meta=dict(
                    page=1,
                    fundcode=fundcode,
                )
            )


    def __init__(self, env="dev"):
        super().__init__(env)

    def parse(self, response):
        meta = response.meta
        fundcode = meta["fundcode"]
        self.parse_statistics(response)
        body = json.loads(response.body)
        total = int(body["result"]["data"]["total_num"])
        # import ipdb; ipdb.set_trace()
        for i in range(2, int(total/21)+2):
            yield Request(
                url=self.base_url.format(fundcode, i),
                dont_filter=True,
                meta=dict(
                    fundcode=fundcode,
                ),
                callback=self.parse_statistics,
            )

    def parse_statistics(self, response):

        meta = response.meta
        fundcode = meta["fundcode"]
        body = json.loads(response.body)
        data_list = body["result"]["data"]["data"]
        obj_list = []
        exists_date_list = set(self.get_exist_fundcode_date_list(fundcode))

        for info in data_list:
            date = datetime.datetime.strptime(info["fbrq"], "%Y-%m-%d %H:%M:%S").date()
            if date in exists_date_list:
                continue
            data = dict(
                fundcode=fundcode,
                date=date,
                net_asset_value=info["jjjz"],
                cumulative_net_value=info["ljjz"],
            )
            new_obj = FundStatistics(**data)
            obj_list.append(new_obj)

        if obj_list:
            self.multi_save(obj_list)
