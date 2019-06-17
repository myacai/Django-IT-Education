import redis
from mycrawl.settings import HOST, PORT, PASSWORD


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


    def putArticle(self, url):
        self._db.sadd("ouwangArticle", url)

    def is_existArticle(self, url):
        return self._db.sismember('ouwangArticle', url)



    def putArticleZaixian(self, url):
        """
        add proxy to right top
        Article
        """
        self._db.sadd("zaixian", url)

    def is_existZaixian(self, url):
        return self._db.sismember('zaixian', url)