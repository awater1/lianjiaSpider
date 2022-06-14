import scrapy
import random
import time
from lianjia_img.items import LianjiaImgItem


class LianjiaImgsSpider(scrapy.Spider):
    name = 'lianjia_imgs'
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
        imgs = response.xpath('//div[@class="img"]/div[@class="thumbnail"]/ul/li')
        category = response.xpath('/html/body/div[3]/div/div/div[1]/h1/@title').get()

        for img in imgs:
            img_name = img.xpath('./@data-desc').get()
            img_src = img.xpath('./@data-pic').get()
            item = LianjiaImgItem()
            if img_name and img_src:
                item["category"] = category
                item["img_name"] = img_name
                item["img_src"] = img_src
                yield item
