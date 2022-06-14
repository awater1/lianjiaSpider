# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from lianjia_img.settings import IMAGES_STORE as IMGS
from scrapy import Request


class LianjiaImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        return Request(item.get('img_src'), meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        print('########', item)
        filePath = '/' + item['category'] + '/' + item['img_name']+'.jpg'
        return filePath

    def item_completed(self, results, item, info):
        return item