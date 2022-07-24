# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags


def remove_whitespace(value):
    return value.strip()


class Product(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(remove_tags, remove_whitespace),
                        output_processor=TakeFirst(), )
    price = scrapy.Field(input_processor=MapCompose(remove_tags, remove_whitespace),
                         output_processor=TakeFirst(), )
