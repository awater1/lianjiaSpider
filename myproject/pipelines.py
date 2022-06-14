# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from openpyxl import Workbook
from myproject.items import HouseItem


class MyprojectPipeline:

    def open_spider(self, spider):
        self.wb = Workbook()
        self.ws = self.wb.create_sheet("lianjia")
        self.ws.append(["小区名称", "户型", "房屋面积", "房价"])

    def process_item(self, item, spider):
        if isinstance(item, HouseItem):
            self.ws.append([item["house_name"], item["house_type"], item["house_size"], item["house_price"]])
        return item

    def close_spider(self, spider):  # 当爬虫结束时自动调用
        self.wb.save("house.xlsx")
