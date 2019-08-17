# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector


class ComicscraperPipeline(object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='XXX',
            database='italiancomics'
        )
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        item.setdefault('series', 'null')
        item.setdefault('subtitle', 'null')
        item.setdefault('authors', 'null')
        item.setdefault('include', 'null')
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""INSERT INTO paninicomics values (?, ?, ?, ?, ?, ?, ?, ?) """, (
            item['title'][0],
            item['link'][0],
            item['price'][0],
            item['publication_date'][0],
            item['series'][0],
            item['subtitle'][0],
            item['authors'][0],
            item['include'][0]
        ))
        self.conn.commit()

