# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def remove_tab(value):
    return value.replace("\t", "")


class ComicsImage(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_names = scrapy.Field()


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
    protagonists = scrapy.Field()
    authors = scrapy.Field()


class ComicsBoxWeeklyItem(scrapy.Item):
    action = scrapy.Field()
    date = scrapy.Field()
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
    protagonists = scrapy.Field()
    authors = scrapy.Field()
