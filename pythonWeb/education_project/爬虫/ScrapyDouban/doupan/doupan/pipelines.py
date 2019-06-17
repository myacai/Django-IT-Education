# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import  pymysql
from doupan import settings

"""

class DoupanPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
               insert into first_app_doupantop
                  value (null,%s,%s,%s,%s),
                (item['title'],
                 item['movieInfo'],
                 item['star'],
                 item['quote']))
            self.connect.commit()
        except Exception as err:
            print("重复插入了==>错误信息为：" + str(err))
        return item
"""

class DoupanPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
               """insert into first_app_doupantop
                  value (null,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (item['no'],
                                          item['movie_name'],
                                          item['director'],
                                          item['writer'],
                                          item['actor'],
                                          item['typee'],
                                          item['region'],
                                          item['language'],
                                          item['date'],
                                          item['length'],
                                          item['another_name'],
                                          item['introduction'],
                                          item['grade'],
                                          item['comment_times']))
            self.connect.commit()
        except Exception as err:
            print("重复插入了==>错误信息为：" + str(err))
        return item