# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from scrapy.exceptions import NotConfigured


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
        item.setdefault('series', 'null')
        item.setdefault('subtitle', 'null')
        item.setdefault('authors', 'null')
        item.setdefault('include', 'null')
        self.store_db(item)
        return item

    def store_db(self, item):
        self.cursor.execute("""INSERT INTO paninicomics values (%s, %s, %s, %s, %s, %s, %s, %s) """, (
            item.get('title'),
            item.get('link'),
            item.get('subtitle'),
            item.get('series'),
            item.get('price'),
            item.get('publication_date'),
            item.get('include'),
            item.get('authors')
        ))
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
