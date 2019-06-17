# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class MycrawlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    date = Field()
    visitCount = Field()
    content = Field()
    url = Field()

class ZaixianlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    date = Field()
    visitCount = Field()
    content = Field()
    url = Field()