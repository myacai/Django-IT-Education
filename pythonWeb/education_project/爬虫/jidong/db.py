# -*- coding: utf-8 -*-
import redis
from .error import PoolEmptyError
from .setting import HOST, PORT, PASSWORD
import random

# redis set操作
class RedisClient(object):
    def __init__(self, host=HOST, port=PORT):
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def get_notpop(self):
        """
        get one from redis 不删除
        """
        proxies = self._db.spop("proxies")
        self._db.sadd("proxies", proxies)
        return proxies.decode('utf-8')
    
    def get_pop(self):
        """
        get one from redis 删除
        """
        proxies = self._db.spop("proxies")
        return proxies
    
    def get_len(self):
        """
            get len from redis
        """
        return self._db.scard("proxies")
    
    def put(self, proxy):
        self._db.sadd("proxies", proxy)

    def is_exist(self, proxy):
        return self._db.sismember('proxies', proxy)
    
    def get_all(self):
        return self._db.smembers('proxies')
    
    def remove(self, proxy):
        return self._db.srem('proxies', proxy)


if __name__ == '__main__':
    conn = RedisClient()
    #ip = conn.get_index()
    #len = conn.queue_len()

    #ip = conn.get_notpop()
    #print(ip)
    
    #proxyList = conn.get_all()
    #for i in proxyList:
        #print(i.decode('utf-8'))
    conn.get_notpop()
    #print(ip)
    #print(len)