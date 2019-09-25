# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import datetime

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

import re


def remove_unicode(value):
    return (value.encode('ascii', 'ignore')).decode("utf-8")


def remove_spaces(value):
    return value.replace("\r\n", "")

def remove_tab(value):
    return value.replace("\t", "")


def format_date(value):
    return datetime.datetime.strptime(value, '%d/%m/%Y').strftime('%Y/%m/%d')


def format(value):
    return re.sub('\s+', ' ', value).strip()


def remove_last_comma(value):
    return value.rstrip(',')


def remove_various_author(value):
    return value.replace("AA.VV.", "")


class ComicsITAItem(scrapy.Item):
    serie_title = scrapy.Field()
    link_albo = scrapy.Field()
    serie_year = scrapy.Field()
    serie_numbers = scrapy.Field()
    publisher = scrapy.Field()
    dettagliEdizione = scrapy.Field()
    issue_title = scrapy.Field(input_processor=MapCompose(remove_tab), output_processor=TakeFirst())
    issue_originalstories = scrapy.Field()
    issue_subtitle = scrapy.Field()
    issue_date = scrapy.Field()
    issue_link_image = scrapy.Field()
    issue_description = scrapy.Field()


class PaniniItem(scrapy.Item):
    title = scrapy.Field(input_processor=MapCompose(remove_spaces, format), output_processor=TakeFirst())
    link = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(remove_spaces, format), output_processor=TakeFirst())
    publication_date = scrapy.Field(input_processor=MapCompose(format_date),output_processor=TakeFirst())
    series = scrapy.Field(input_processor=MapCompose(remove_spaces, format), output_processor=TakeFirst())
    subtitle = scrapy.Field(input_processor=MapCompose(remove_spaces, format), output_processor=TakeFirst())
    authors = scrapy.Field(input_processor=MapCompose(remove_various_author, remove_spaces, format, remove_last_comma), output_processor=TakeFirst())
    include = scrapy.Field(input_processor=MapCompose(remove_spaces, format, remove_last_comma), output_processor=TakeFirst())
    image_url = scrapy.Field()
    description = scrapy.Field(input_processor=MapCompose(remove_spaces, format), output_processor=TakeFirst())
    pages = scrapy.Field(input_processor=MapCompose(remove_spaces, format), output_processor=TakeFirst())

class ComicsBoxWeeklyItem(scrapy.Item):
    date = scrapy.Field()
    serie_title = scrapy.Field()
    action = scrapy.Field()
    link_albo = scrapy.Field()
    serie_year = scrapy.Field()
    serie_numbers = scrapy.Field()
    publisher = scrapy.Field()
    dettagliEdizione = scrapy.Field()
    issue_title = scrapy.Field(input_processor=MapCompose(remove_tab), output_processor=TakeFirst())
    issue_originalstories = scrapy.Field()
    issue_subtitle = scrapy.Field()
    issue_date = scrapy.Field()
    issue_link_image = scrapy.Field()
    issue_description = scrapy.Field()