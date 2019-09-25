# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.exceptions import NotConfigured
from datetime import datetime
import datetime as DT
from scrapy.exceptions import DropItem


class ComicscraperPipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)

    def open_spider(self, spider):
        self.conn = pymysql.connect(db=self.db,
                                    user=self.user, passwd=self.passwd,
                                    host=self.host,
                                    charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        itemSerieTitle = item.get('serie_title')
        item['serie_title'] = itemSerieTitle.strip()

        itemPublisher  = item.get('publisher')
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
        itemDate = "01/" + item.get('issue_date')
        if "Gennaio" in itemDate:
            itemDate = itemDate.replace("Gennaio ","01/")
        if "Febbraio" in itemDate:
            itemDate = itemDate.replace("Febbraio ","02/")
        if "Marzo" in itemDate:
            itemDate = itemDate.replace("Marzo ","03/")
        if "Aprile" in itemDate:
            itemDate = itemDate.replace("Aprile ","04/")
        if "Maggio" in itemDate:
            itemDate = itemDate.replace("Maggio ","05/")
        if "Giugno" in itemDate:
            itemDate = itemDate.replace("Giugno ","06/")
        if "Luglio" in itemDate:
            itemDate = itemDate.replace("Luglio ","07/")
        if "Agosto" in itemDate:
            itemDate = itemDate.replace("Agosto ","08/")
        if "Settembre" in itemDate:
            itemDate = itemDate.replace("Settembre ","09/")
        if "Ottobre" in itemDate:
            itemDate = itemDate.replace("Ottobre ","10/")
        if "Novembre" in itemDate:
            itemDate = itemDate.replace("Novembre ","11/")
        if "Dicembre" in itemDate:
            itemDate = itemDate.replace("Dicembre ","12/")
        item['issue_date'] = itemDate

        self.store_db(item)
        return item

    def store_db(self, item):
        date = datetime.strptime(item.get('issue_date'), "%d/%m/%Y").strftime("%Y/%m/%d")
        self.cursor.execute("""INSERT INTO italiancomics values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (
            item.get('serie_title'),
            item.get('link_albo'),
            item.get('serie_year'),
            item.get('serie_numbers'),
            item.get('publisher'),
            item.get('issue_title'),
            item.get('issue_originalstories'),
            item.get('issue_subtitle'),
            date,
            item.get('issue_description'),
            item.get('issue_link_image'),
        ))
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()




    def store_dbPANINI(self, item):
        query = "SELECT * FROM italiancomics where link=" + "'" + item.get('link')[0] + "'"
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            if datetime.today().strftime('%Y/%m/%d') > item.get('publication_date') :
                self.cursor.execute("""INSERT INTO italiancomics values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (
                    item.get('title'),
                    item.get('link'),
                    item.get('subtitle'),
                    item.get('series'),
                    item.get('price'),
                    item.get('publication_date'),
                    item.get('include'),
                    item.get('authors'),
                    item.get('image_url'),
                    item.get('description'),
                    item.get('pages')
                ))
                self.conn.commit()


class ComicscraperWeeklyPipeline(object):
    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        passwd = db_settings['passwd']
        host = db_settings['host']
        return cls(db, user, passwd, host)

    def open_spider(self, spider):
        self.conn = pymysql.connect(db=self.db,
                                    user=self.user, passwd=self.passwd,
                                    host=self.host,
                                    charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
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
            itemDate = item.get('issue_date')
            if 'Gennaio' in itemDate:
                itemDate = itemDate.replace("Gennaio ", "01/")
            if 'Febbraio' in itemDate:
                itemDate =itemDate.replace("Febbraio ", "02/")
            if 'Marzo' in itemDate:
                itemDate =itemDate.replace("Marzo ", "03/")
            if 'Aprile' in itemDate:
                itemDate =itemDate.replace("Aprile ", "04/")
            if 'Maggio' in itemDate:
                itemDate =itemDate.replace("Maggio ", "05/")
            if 'Giugno' in itemDate:
                itemDate =itemDate.replace("Giugno ", "06/")
            if 'Luglio' in itemDate:
                itemDate =itemDate.replace("Luglio ", "07/")
            if 'Agosto' in itemDate:
                itemDate =itemDate.replace("Agosto ", "08/")
            if 'Settembre' in itemDate:
                itemDate =itemDate.replace("Settembre ", "09/")
            if 'Ottobre' in itemDate:
                itemDate =itemDate.replace("Ottobre ", "10/")
            if 'Novembre' in itemDate:
                itemDate =itemDate.replace("Novembre ", "11/")
            if 'Dicembre' in itemDate:
                itemDate =itemDate.replace("Dicembre ", "12/")
            item['issue_date'] = "01/" + itemDate
            self.store_db(item)
            return item
        else:
            raise DropItem("before Week")

    def store_db(self, item):
        date = datetime.strptime(item.get('issue_date'), "%d/%m/%Y").strftime("%Y/%m/%d")
        query = "SELECT * FROM italiancomics where link_albo=" + "'" + item.get('link_albo') + "'"
        self.cursor.execute(query)
        #Se l'albo non e' gia' presente nel dp lo aggiungo, altrimenti faccio un update
        if self.cursor.rowcount == 0:
            self.cursor.execute("""INSERT INTO italiancomics values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """, (
                item.get('serie_title'),
                item.get('link_albo'),
                item.get('serie_year'),
                item.get('serie_numbers'),
                item.get('publisher'),
                item.get('issue_title'),
                item.get('issue_originalstories'),
                item.get('issue_subtitle'),
                date,
                item.get('issue_description'),
                item.get('issue_link_image')
            ))
            self.conn.commit()
        else:
            self.cursor.execute("""UPDATE italiancomics SET serie_title=%s, publisher=%s, issue_title=%s, issue_originalstories=%s, issue_subtitle=%s, issue_date=%s, issue_link_image=%s, issue_description=%s WHERE link_albo=%s""", (
                item.get('serie_title'),
                item.get('publisher'),
                item.get('issue_title'),
                item.get('issue_originalstories'),
                item.get('issue_subtitle'),
                item.get('issue_date'),
                item.get('issue_link_image'),
                item.get('issue_description'),
                item.get('link_albo')
            ))
            self.conn.commit()





    def close_spider(self, spider):
        self.conn.close()



