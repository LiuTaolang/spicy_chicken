from scrapy.selector import Selector
from scrapy import Spider
from web_scrapy.items import WebScrapyItem


class FundListSpider(Spider):
    name = 'fund_list'
    allowed_domains = ['eastmoney.com']
    start_urls = ['http://fund.eastmoney.com/allfund.html']

    def parse(self, response):
        item = WebScrapyItem()
        fund_code = response.xpath('//li[@class="b"]/div/a[1]/text()').extract()
        print('fund codes:\n', fund_code)
        input('fund totality:\n' + str(len(fund_code)))
        item['fund_code'] = fund_code
        return item
