# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

"""
class DoupanItem(scrapy.Item):
    title = scrapy.Field() # 电影名字
    movieInfo = scrapy.Field() # 电影的描述信息，包括导演、主演、电影类型等等
    star = scrapy.Field() # 电影评分
    quote = scrapy.Field() # 电影中最经典或者说脍炙人口的一句话
"""
class DoupanItem(scrapy.Item):
    no = scrapy.Field()
    movie_name = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    actor = scrapy.Field()
    typee = scrapy.Field()
    region = scrapy.Field()
    language = scrapy.Field()
    date = scrapy.Field()
    length = scrapy.Field()
    another_name = scrapy.Field()
    introduction = scrapy.Field()
    grade = scrapy.Field()
    comment_times = scrapy.Field()