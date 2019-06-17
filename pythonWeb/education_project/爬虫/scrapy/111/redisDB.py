import redis
from setting import HOST, PORT, PASSWORD

class RedisClient(object):
    def __init__(self, host=HOST, port=PORT):
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)

    def put(self, url):
        self._db.sadd("ouwang", url)

    def is_exist(self, url):
        return self._db.sismember('ouwang', url)
    
    def put_Aclass(self, url):
        self._db.sadd("ouwang3", url)


    def putArticle(self, url):
        """
        add proxy to right top
        Article
        """
        self._db.sadd("ouwangArticle2", url)

    def is_existArticle(self, url):
        return self._db.sismember('ouwangArticle2', url)

    
    
    def get(self):
        """
        get url from redis in set
        """
        url = self._db.spop("ouwang")
        return url.decode()

    def get_len(self):
        """
            get len from redis
        """
        return self._db.scard("ouwang")
    
    def get_ip(self):
        """
            get len from redis
        """
        return self._db.scard("ouwang")
    
if __name__ == '__main__':
    conn = RedisClient()
    url = conn.get()
    print(url)
    reg = r'article\d*show.html'

