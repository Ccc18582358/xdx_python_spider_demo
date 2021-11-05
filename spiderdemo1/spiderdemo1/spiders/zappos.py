import time
import urllib

import scrapy

from ..items import Spiderdemo1Item


class ZapposSpider(scrapy.Spider):
    name = 'zappos'
    allowed_domains = ['zappos.com']
    start_urls = ['https://www.zappos.com/null/.zso']

    def parse(self, response):
        article_list = response.xpath('//*[@id="products"]//article')

        for article in article_list:
            item = Spiderdemo1Item()
            item["href"] = article.xpath('a/@href').extract_first()

            if item["href"] is not None:
                item["href"] = urllib.parse.urljoin(response.url, item["href"])
                time.sleep(2)
                yield scrapy.Request(
                    item["href"],
                    callback=self.parse_detail,
                    meta={"item": item},
                    dont_filter=True)

        next_url = response.xpath('//*[@id="searchPagination"]/div[2]/a[2]/@href').extract_first()
        next_url = urllib.parse.urljoin('https://www.zappos.com', next_url)

        yield scrapy.Request(
            next_url,
            callback=self.parse
        )

    def parse_detail(self, response):
        item = response.meta["item"]
        item["title"] = response.xpath('//*[@id="breadcrumbs"]/div[1]/a[4]/span/text()').extract_first()
        item["price"] = response.xpath(
            '//*[@id="productRecap"]/div[1]/div[2]/div/div[1]/div[1]/div/span/span/text()').extract()

        item["color"] = response.xpath('//*[@id="buyBoxForm"]/div[1]/div/span[2]/text()').extract()

        # item["size_product"] = response.xpath(
        #     '//*[@id="buyBoxForm"]/div[2]/fieldset[1]/div/div[@class="pq-z"]/label/text()').extract()
        # item["size_unavailable"] = response.xpath(
        #     '//*[@id="buyBoxForm"]/div[2]/fieldset[1]/div/div[@class="pq-z qq-z"]/label/text()').extract()
        item["sku"] = response.xpath('//*[@id="breadcrumbs"]/div[2]/span/text()').extract_first()
        item["size"] = response.xpath('//*[@id="pdp-size-select"]/option/text()').extract()

        li_list = response.xpath('//div[@class="px-z qx-z nx-z"]/ul/li')
        for li in li_list:
            item["detail"] = li.xpath("font/font/text()").extract()
        item["img_urls"] = response.xpath('//div[@class="tl-z/label/span/img/@src"]').extract()
        for img in item["img_urls"]:
            img_manage = img.partition("AC_")
            postfix = "SR920, 736_.jpg"
            img = img_manage[0] + img_manage[1] + postfix
            del item["img_urls"]
            item["img_urls"].append(img)
        print(item)
        yield item
