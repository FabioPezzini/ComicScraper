# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import datetime as DT
import scrapy

from datetime import datetime
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from .items import ComicsITAItem, ComicsBoxWeeklyItem
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

                itemAuthors = item.get('authors')
                if itemAuthors is not None:
                    temp = list(dict.fromkeys(itemAuthors))
                    item['authors'] = ', '.join(temp)

                itemProtagonists = item.get('protagonists')
                if itemProtagonists is not None:
                    temp = list(dict.fromkeys(itemProtagonists))
                    item['protagonists'] = ', '.join(temp)

                itemPublisher = item.get('publisher')
                item['publisher'] = itemPublisher.strip()

                itemTitle = item.get('issue_title')
                item['issue_title'] = itemTitle.strip()

                itemStory = item.get('issue_originalstories')
                if itemStory is not None:
                    words = [w.replace('# ', '#') for w in itemStory]
                    item['issue_originalstories'] = '\n'.join(words)
                if itemStory is not None and len(itemStory) == 0:
                    del item['issue_originalstories']

                itemSub = item.get('issue_subtitle')
                if itemSub is not None:
                    item['issue_subtitle'] = itemSub.replace('| ', '')

                itemDesc = item.get('issue_description')
                if itemDesc is not None:
                    item['issue_description'] = ''.join(itemDesc)

                itemDate = "01/" + item.get('issue_date')
                if "Gennaio" in itemDate:
                    itemDate = itemDate.replace("Gennaio ", "01/")
                if "Febbraio" in itemDate:
                    itemDate = itemDate.replace("Febbraio ", "02/")
                if "Marzo" in itemDate:
                    itemDate = itemDate.replace("Marzo ", "03/")
                if "Aprile" in itemDate:
                    itemDate = itemDate.replace("Aprile ", "04/")
                if "Maggio" in itemDate:
                    itemDate = itemDate.replace("Maggio ", "05/")
                if "Giugno" in itemDate:
                    itemDate = itemDate.replace("Giugno ", "06/")
                if "Luglio" in itemDate:
                    itemDate = itemDate.replace("Luglio ", "07/")
                if "Agosto" in itemDate:
                    itemDate = itemDate.replace("Agosto ", "08/")
                if "Settembre" in itemDate:
                    itemDate = itemDate.replace("Settembre ", "09/")
                if "Ottobre" in itemDate:
                    itemDate = itemDate.replace("Ottobre ", "10/")
                if "Novembre" in itemDate:
                    itemDate = itemDate.replace("Novembre ", "11/")
                if "Dicembre" in itemDate:
                    itemDate = itemDate.replace("Dicembre ", "12/")

                day,month,year = itemDate.split("/")
                date = datetime(int(year), int(month), int(day), 1, 1)
                item['issue_date'] = date

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

    def process_item(self, item, spider):
        if isinstance(item, ComicsBoxWeeklyItem):
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

                today = DT.date.today()
                week_before = today - DT.timedelta(days=7)
                weekFormatted = week_before.strftime('%d/%m/%Y')
                if datetime.strptime(item.get('date'), '%d/%m/%Y') > datetime.strptime(weekFormatted, '%d/%m/%Y'):
                    itemAuthors = item.get('authors')
                    if itemAuthors is not None:
                        temp = list(dict.fromkeys(itemAuthors))
                        item['authors'] = ', '.join(temp)

                    itemProtagonists = item.get('protagonists')
                    if itemProtagonists is not None:
                        temp = list(dict.fromkeys(itemProtagonists))
                        item['protagonists'] = ', '.join(temp)

                    itemStory = item.get('issue_originalstories')
                    if itemStory is not None:
                        words = [w.replace('# ', '#') for w in itemStory]
                        item['issue_originalstories'] = '\n'.join(words)
                    if itemStory is not None and len(itemStory) == 0:
                        del item['issue_originalstories']

                    itemSub = item.get('issue_subtitle')
                    if itemSub is not None:
                        item['issue_subtitle'] = itemSub.replace('| ', '')

                    itemDesc = item.get('issue_description')
                    if itemDesc is not None:
                        item['issue_description'] = ''.join(itemDesc)

                    itemDate = "01/" + item.get('issue_date')
                    if "Gennaio" in itemDate:
                        itemDate = itemDate.replace("Gennaio ", "01/")
                    if "Febbraio" in itemDate:
                        itemDate = itemDate.replace("Febbraio ", "02/")
                    if "Marzo" in itemDate:
                        itemDate = itemDate.replace("Marzo ", "03/")
                    if "Aprile" in itemDate:
                        itemDate = itemDate.replace("Aprile ", "04/")
                    if "Maggio" in itemDate:
                        itemDate = itemDate.replace("Maggio ", "05/")
                    if "Giugno" in itemDate:
                        itemDate = itemDate.replace("Giugno ", "06/")
                    if "Luglio" in itemDate:
                        itemDate = itemDate.replace("Luglio ", "07/")
                    if "Agosto" in itemDate:
                        itemDate = itemDate.replace("Agosto ", "08/")
                    if "Settembre" in itemDate:
                        itemDate = itemDate.replace("Settembre ", "09/")
                    if "Ottobre" in itemDate:
                        itemDate = itemDate.replace("Ottobre ", "10/")
                    if "Novembre" in itemDate:
                        itemDate = itemDate.replace("Novembre ", "11/")
                    if "Dicembre" in itemDate:
                        itemDate = itemDate.replace("Dicembre ", "12/")

                    day, month, year = itemDate.split("/")
                    date = datetime(int(year), int(month), int(day), 1, 1)
                    item['issue_date'] = date

                    self.store_in_db(item)
                else:
                    raise DropItem("Issue release more than week ago, discard it")
            pass
        return item

    def store_in_db(self, item):
        # If the comics is already in the DB i must upgrade its content
        if self.collection.count_documents({'link_albo': item.get('link_albo')}, limit=1):
            #Check if object is has a recent modify
            cursor = self.collection.find_one({"link_albo": item.get('link_albo')})

            if len(cursor.get('date')) != 0:
                dateModify = cursor.get('date')
                day, month, year = dateModify.split("/")
                dateModify = datetime(int(year), int(month), int(day), 1, 1)

                dateItemModify = item.get('date')
                dayM, monthM, yearM = dateItemModify.split("/")
                dateItemModify = datetime(int(yearM), int(monthM), int(dayM), 1, 1)

                #if the modify on the item is older than the actual modify
                if dateModify <= dateItemModify:
                    self.collection.find_one_and_update({'link_albo': item.get('link_albo')}, {'$set': item})
                else:
                    print("THE DOCUMENT HAS A RECENT MODIFY")
            else:
                self.collection.find_one_and_update({'link_albo': item.get('link_albo')}, {'$set': item})
        else:
            self.collection.insert(dict(item))

    def close_spider(self, spider):
        self.conn.close()