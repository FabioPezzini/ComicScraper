# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import datetime as DT
import scrapy

from datetime import datetime
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from .items import ComicsITAItem
from .items import ComicsImage


class CustomImageNamePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if isinstance(item, ComicsImage):
            for (image_url, image_name) in zip(item[self.IMAGES_URLS_FIELD], item["image_names"]):
                yield scrapy.Request(url=image_url, meta={"image_name": image_name})

    def file_path(self, request, response=None, info=None):
        image_name = request.meta["image_name"]
        return image_name


class ComicscraperPipeline(object):
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['thecomics']
        self.collection = db['comics']

    def process_item(self, item, spider):
        if isinstance(item, ComicsITAItem):
            valid = True
            for data in item:
                if not data:
                    valid = False
                    raise DropItem("Missing {0}!".format(data))
            if valid:
                itemSerieTitle = item.get('serie_title')
                item['serie_title'] = itemSerieTitle.strip()

                itemPublisher = item.get('publisher')
                item['publisher'] = itemPublisher.strip()

                itemTitle = item.get('issue_title')
                item['issue_title'] = itemTitle.strip()

                itemStory = item.get('issue_originalstories')
                if itemStory is not None:
                    words = [w.replace('# ', '#') for w in itemStory]
                    item['issue_originalstories'] = ','.join(words)
                if itemStory is not None and len(itemStory) == 0:
                    del item['issue_originalstories']
                itemSub = item.get('issue_subtitle')
                if itemSub is not None:
                    item['issue_subtitle'] = itemSub.replace('| ', '')

                self.collection.insert(dict(item))
            pass
        return item

    def close_spider(self):
        self.conn.close()


class ComicscraperWeeklyPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['thecomics']
        self.collection = db['comics']

    def process_item(self, item):
        if isinstance(item, ComicsITAItem):
            itemSerieTitle = item.get('serie_title')
            item['serie_title'] = itemSerieTitle.strip()

            itemPublisher = item.get('publisher')
            item['publisher'] = itemPublisher.strip()

            itemTitle = item.get('issue_title')
            item['issue_title'] = itemTitle.strip()

            today = DT.date.today()
            week_before = today - DT.timedelta(days=7)
            weekFormatted = week_before.strftime('%d/%m/%Y')
            if datetime.strptime(item.get('date'), '%d/%m/%Y') > datetime.strptime(weekFormatted, '%d/%m/%Y'):
                itemStory = item.get('issue_originalstories')
                if itemStory is not None:
                    words = [w.replace('# ', '#') for w in itemStory]
                    item['issue_originalstories'] = ','.join(words)
                if itemStory is not None and len(itemStory) == 0:
                    del item['issue_originalstories']
                itemSub = item.get('issue_subtitle')
                if itemSub is not None:
                    item['issue_subtitle'] = itemSub.replace('| ', '')

                self.store_in_db(item)
                return item
            else:
                raise DropItem("before Week")
        pass

    def store_in_db(self, item):
        # If the comics is already in the DB i must upgrade its content
        if self.collection.count_documents({'link_albo': item.get('link_albo')}, limit=1):
            self.collection.find_one_and_update({'link_albo': item.get('link_albo')}, {'$set': item})
        else:
            self.collection.insert(dict(item))

    def close_spider(self, spider):
        self.conn.close()
