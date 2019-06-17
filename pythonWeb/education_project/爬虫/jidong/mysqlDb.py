# -*- coding: utf-8 -*-
import pymysql
from setting import *
import re

# 连接MySQL配置信息
config = {
    'host': mysql_host,
    'port': mysql_port,
    'user': mysql_user,
    'password': mysql_password,
    'db': mysql_db,
    'charset': mysql_charset,
    'cursorclass': pymysql.cursors.DictCursor,
}


def is_existMysql(productName):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "select productId from first_app_jingdong where productName = " +"'" +str(productName)+"'"
    try:
        cursor.execute(sql)
        productId = cursor.fetchall()
        #print(productId)
        if productId == ():
            #print("不存在")
            return False
        else:
            #print("存在")
            return True
    except Exception as e:
        print(e)
        print('is_existMysql查询失败')
    finally:
        db.close()

def select_update(query):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    reg = r'\d*-\d*-(\d*)'
    
    sql = "select updete_time from first_app_jingdong where from_name = " +"'" +str(query)+"'"
    try:
        cursor.execute(sql)
        update_time = cursor.fetchall()
        try:
            if update_time == None:
                print('update_time None')
                update_time = '33'
            else:
                update_time = update_time[0]['updete_time']       
                update_time = re.findall(reg,update_time)[0]
        except Exception:
            update_time = '33'
        # supdate_time = update_time[0]
        print('查询成功')
    except Exception as e:
        print(e)
        print('查询失败')
    db.close()
    return update_time

def into_mysql(prices,commentNums,productName,shopName,productId,links,image):
    if( not is_existMysql(productName) ):
        db = pymysql.connect(**config)
        cursor = db.cursor()
        sql = "REPLACE INTO first_app_jingdong " \
            "values(null,'%s', '%s', '%s','%s', '%s', '%s', '%s')" % \
            (productId, productName, shopName, commentNums, prices, links, image)
        try:
            cursor.execute(sql)
            db.commit()
            print('插入成功')
        except Exception as e:
            print(e)
            print('插入失败')
            db.rollback()
        db.close()
    else:
        print("已经存在")
    
if __name__ == '__main__':
    #update_time = select_update('瑞安公安')
    #print(update_time)
    if( not is_existMysql("联想(Lenovo)小新青春版 英特尔酷睿i7 14英寸 轻薄笔记本电脑(I7-8565U 8G 1T+128G FHD 2G独显)追梦银")):
        print("bucunz")
    else:
        print("cunz")
