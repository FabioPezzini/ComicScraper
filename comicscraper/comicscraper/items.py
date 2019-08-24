# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

import re


def remove_unicode(value):
    return (value.encode('ascii', 'ignore')).decode("utf-8")


def remove_spaces(value):
    return value.replace("\r\n", "")


def format(value):
    return re.sub('\s+', ' ', value).strip()

def remove_last_comma(value):
    return value.rstrip(',')
def remove_various_author(value):
    return value.replace("AA.VV.", "")


class ComicscraperItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(
        input_processor=MapCompose(remove_unicode, remove_spaces, format), output_processor=TakeFirst()
    )
    link = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(remove_unicode, remove_spaces, format), output_processor=TakeFirst())
    publication_date = scrapy.Field()
    series = scrapy.Field(input_processor=MapCompose(remove_unicode, remove_spaces, format), output_processor=TakeFirst())
    subtitle = scrapy.Field(input_processor=MapCompose(remove_unicode, remove_spaces, format), output_processor=TakeFirst())
    authors = scrapy.Field(input_processor=MapCompose(remove_unicode, remove_various_author, remove_spaces, format, remove_last_comma), output_processor=TakeFirst())
    include = scrapy.Field(input_processor=MapCompose(remove_unicode, remove_spaces, format, remove_last_comma), output_processor=TakeFirst())
    image_url = scrapy.Field()
