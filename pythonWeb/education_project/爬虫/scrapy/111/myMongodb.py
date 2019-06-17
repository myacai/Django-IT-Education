# -*- coding:utf-8 -*-
from pymongo import MongoClient
from setting import MONGO_URI,MONGO_PORT,MONGO_DATABASE,MONGO_SETNAME
import openpyxl

class MongodbClient(object):
    def __init__(self, host=MONGO_URI, port=MONGO_PORT, 
                 dbName=MONGO_DATABASE, setName=MONGO_SETNAME):
        
        # 建立连接
        self.client = MongoClient(host, port)
        # 获取数据库
        self.db = self.client[dbName]
        # 获取集合
        self.mycol = self.db[setName]
    
    def put(self, result):
        self.mycol.insert(result)
"""
m = MongodbClient(MONGO_URI,MONGO_PORT,MONGO_DATABASE,MONGO_SETNAME)
print('1')
url = 'http://www.wzrb.com.cn/ow2016/piclist/article657284show.html'
result = m.mycol.find_one({"url": url})
if result:
    print(result)
else: 
    print('不存在')
"""


def write(sheet, raw, value):
    for j in range(0, len(value)):
        # print('i %d j %d'% (raw,j))
        sheet.cell(row=raw + 1, column=j + 1, value=str(value[j]))
        
        
if __name__ == '__main__':
    conn = MongodbClient()
    filepath = r'C:\Users\Administrator\Desktop\ouwang.xlsx'
    sheetTitle = 'ouwang'
    raw = 0
    text = ['url', 'title', 'date', 'visitCount','content']
    
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = sheetTitle
    write(sheet, raw, text)
    
    for i in conn.mycol.find():
        raw = raw + 1
        value = [i['url'], i['title'], i['date'], i['visitCount'], i['content']]
        try:
            write(sheet, raw, value)
        except Exception:
            print('异常')
    
    wb.save(filepath)
    print("写入数据成功！")


        
    
    
    
    
    
    