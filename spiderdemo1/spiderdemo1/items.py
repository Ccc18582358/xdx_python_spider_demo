# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Spiderdemo1Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    header = scrapy.Field()
    vertical = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    price_final = scrapy.Field()
    price_original = scrapy.Field()
    color = scrapy.Field()
    size_product = scrapy.Field()
    size_unavailable = scrapy.Field()
    sku = scrapy.Field()
    details = scrapy.Field()
    img_urls = scrapy.Field()
    price = scrapy.Field()
    size = scrapy.Field()
