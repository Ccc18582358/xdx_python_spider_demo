# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import codecs
import json
import os

from itemadapter import ItemAdapter
from scrapy import item

from .items import SpiderdemoItem


class SpiderdemoPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    def __init__(self):

        self.df = codecs.open("./eastbaysave.json", "w", encoding="utf-8")
        self.df.write("[")

    def open_spider(self, spider):
        print("json存储开始")

    def process_item(self, item, spider):


        try:
            value = dict(item)
            json_str = json.dumps(value, ensure_ascii=False)
            self.df.write(json_str)
            self.df.write(",\n")
        except Exception as e:
            print("存储失败", e)
        return item

    def close_spider(self, spider):

        self.df.truncate()
        self.df.write("]")
        self.df.close()
