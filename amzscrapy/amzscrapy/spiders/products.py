import scrapy
from scrapy.loader import ItemLoader
from ..items import Product


class ProductsSpider(scrapy.Spider):
    name = 'products'
    allowed_domains = ['amazon.co.uk']

    def start_requests(self):
        baseurl = "https://www.amazon.co.uk/dp/"
        with open('asins.csv') as f:
            for line in f:
                if not line.strip():
                    continue
                yield scrapy.Request(baseurl + line)

    def parse(self, response):
        loader = ItemLoader(item=Product(), response=response)
        loader.add_css('name', 'span#productTitle')
        loader.add_css('price', 'span.a-price span')
        yield loader.load_item()
