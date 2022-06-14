import random
import scrapy
import time
from myproject.items import HouseItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['https://xa.lianjia.com/ershoufang/pg1/']

    def parse(self, response):
        url_list = response.xpath('//div[@class="info clear"]/div[@class="title"]/a/@href').extract()

        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_detail)
            i = random.random()
            time.sleep(i)

        page = eval(response.xpath('//div[@class="contentBottom clear"]/div[@class="page-box fr"]/div['
                                   '@class="page-box house-lst-page-box"]/@page-data').get())
        total_page = int(page.get('totalPage'))
        cur_page = int(page.get('curPage'))
        next_page = cur_page + 1

        if cur_page < total_page:
            next_url = 'https://xa.lianjia.com/ershoufang/pg' + str(next_page)
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        name = response.xpath("//div[@class='communityName']/a[1]/text()").get()
        price = response.xpath("//div[@class='price ']/span[@class='total']/text()").get()
        base = response.xpath("//div[@class='base']/div[@class='content']/ul")
        types = base.xpath("./li[1]/text()").get()
        size = base.xpath("./li[3]/text()").get()
        item = HouseItem()
        item["house_name"] = name
        item["house_price"] = price
        item["house_type"] = types
        item["house_size"] = size
        yield item

