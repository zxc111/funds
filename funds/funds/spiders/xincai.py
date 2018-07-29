# -*- coding: utf-8 -*-

from scrapy import Request

from base import BaseSpider

from funds.models.funds import Fund


class XincaiSpider(BaseSpider):
    name = 'xincai'

    base_url = "https://trade.xincai.com"
    # allowed_domains = ['xincai.xom']
    start_urls = ['https://trade.xincai.com/web/goodsFund?status=&order=month_incratio&order_type=desc&tab=1&page=1']

    def url(self, page):
        return "{}/web/goodsFund?status=&order=month_incratio&order_type=desc&tab=1&page={}".format(
            self.base_url,
            page,
        )

    def __init__(self, env="dev"):
        super().__init__(env)

    def parse_fund_list(self, response):
        fundcode_dict = {}

        for fund in response.xpath("//tbody/tr"):
            name, fundcode = fund.xpath("./td/a/text()").extract()[:2]
            fundcode_dict[fundcode] = dict(
                name=name,
                fundcode=fundcode,
            )
        exist_fundcode_list = self.get_exist_fundcode_list(fundcode_dict.keys())
        for fundcode in exist_fundcode_list:
            del fundcode_dict[fundcode]

        if fundcode_dict:
            obj_list = [Fund(**fundcode_dict[k]) for k in fundcode_dict]
            self.multi_save(obj_list)


    def parse(self, response):
        self.parse_fund_list(response)
        max_page = max(
            map(
                int,
                response.xpath("//div[@class='pages']/ul/li/a/@data-page").extract()
            )
        )
        # return

        for page in range(2, max_page+1):
            # import ipdb; ipdb.set_trace()
            yield Request(
                url=self.url(page),
                callback=self.parse_fund_list,
                headers={"Referer": self.url(page-1)}
            )
