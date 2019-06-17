# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from mycrawl.items import MycrawlItem,ZaixianlItem

class MycrawlPipeline(object):
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db



    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            # mongo_db_tmail=crawler.settings.get('MONGO_DATABASE_TMAIL'),
            # mongo_db_commentTaobao=crawler.settings.get('MONGO_DATABASE_TAOBAOCOMMENT'),
            # mongo_db_commentTmail=crawler.settings.get('MONGO_DATABASE_TMAILCOMMENT'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, MycrawlItem):
            self.db['article'].update({'url': item['url']}, {'$set': item}, True)
        elif isinstance(item, ZaixianlItem):
            self.db['articleZaixian'].update({'url': item['url']}, {'$set': item}, True)
        return item
