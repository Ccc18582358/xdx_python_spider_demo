import time
import urllib

from shlex import join

import scrapy
from ..items import SpiderdemoItem

class EastbaySpider(scrapy.Spider):
    name = 'eastbay'
    allowed_domains = ['eastbay.com']
    start_urls = ['https://www.eastbay.com/category/sale.html']

    def parse(self, response):
        li_list = response.xpath('//div[@class="SearchResults"]//li')
        for li in li_list:
            item = SpiderdemoItem()
            item["href"] = li.xpath('div/a/@href').extract_first()


            if item["href"] is not None:
                item["href"] = urllib.parse.urljoin("https://www.eastbay.com",item["href"])
                # print(item["href"])

                yield scrapy.Request(
                    item["href"],
                    callback=self.parse_detail,
                    meta={"item": item},
                    dont_filter=True)
                time.sleep(1)


        next_url = response.xpath('//*[@id="main"]/div/div[2]/div/section/div/div[2]/nav/ul/li[9]/a/@href').extract_first()
        next_url = urllib.parse.urljoin(response.url,next_url)
        page = next_url.partition("=")[2]
        page = str(int(page) - 71)

        next_url = next_url.partition("=")[0]+next_url.partition("=")[1]+page




        yield scrapy.Request(
            next_url,
            callback=self.parse
        )


    def parse_detail(self,response):

        item = response.meta["item"]
        # print(item["href"])
        item["title"] = response.xpath('//*[@id="main"]/div/div[1]/nav/ol/li[2]/text()').extract_first()
        item["price_final"] = response.xpath('//*[@id="ProductDetails"]/div[4]/div[2]/span/span/span/span[2]/text()').extract_first()
        item["price_original"] = response.xpath('//*[@id="ProductDetails"]/div[4]/div[2]/span/span/span/span[3]/text()').extract_first()
        item["color"] = response.xpath('//*[@id="ProductDetails"]/div[4]/p[1]/text()').extract()
        item["size_product"] = response.xpath('//*[@id="ProductDetails"]/div[4]/fieldset/div/div[@class="c-form-field c-form-field--radio ProductSize"]/input/@aria-label').extract()
        item["size_unavailable"] = response.xpath('//*[@id="ProductDetails"]/div[4]/fieldset/div/div[@class="c-form-field c-form-field--radio c-form-field--disabled c-form-field--unavailable ProductSize"]/input/@aria-label').extract()
        item["sku"] = response.xpath('//*[@id="ProductDetails-tabs-details-panel"]/text()').extract()
        item["sku"] = join(item["sku"]).partition(":")[2]
        item["details"] = response.xpath('//*[@id="ProductDetails-tabs-details-panel"]/div/p/text()').extract()
        div_list = response.xpath('//*[@id="ProductDetails"]/div[2]/fieldset/div')
        for div in div_list:

            item["img_urls"] = []
            item["img_urls"] = item["img_urls"].append(div.xpath('label/span/span/span/img/@src').extract())

        print(item)
        yield item




