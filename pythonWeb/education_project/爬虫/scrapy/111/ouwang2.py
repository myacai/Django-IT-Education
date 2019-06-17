from redisDB import RedisClient
from myMongodb import MongodbClient
from myfilter import run
from multiprocessing import Pool
import os
import time, random

def main():
    print('开始一个进程')
    rconn = RedisClient()
    mconn = MongodbClient()
    while rconn.get_len() > 0:
        try:
            time.sleep(random.random())
            url = rconn.get()
            result = mconn.mycol.find_one({"url": url})
            if result:
                print('url已经爬取')
            else:
                print('进入一个url')
                title, ctt, date, visitCount = run(url)
                print(title)
                if title == "有道首页":
                    continue
                if ctt == "":
                    continue
                if title == "":
                    print('title为空')
                    rconn.put(url)
                    continue
                info = {"url":url, "content":ctt, 
                              "date":date, "title":title, 
                              "visitCount":visitCount}
                mconn.put(info)
        except Exception:
            print('异常')
            rconn.put(url)
            print(url)
    print('结束一个进程')
        
    
if __name__ == "__main__":
    print('Parent process %s.' % os.getpid())
    p = Pool(10)

    for i in range(11):
        p.apply_async(main, args=())
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
