import time
from multiprocessing import Process
import asyncio
import aiohttp
try:
    from aiohttp.errors import ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError,ServerDisconnectedError,ClientResponseError,ClientConnectorError
from db import RedisClient
from error import ResourceDepletionError
from getter import FreeProxyGetter
from settings import *
from asyncio import TimeoutError



class ValidityTester(object):
    test_api = TEST_API

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies
        self._conn = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        text one proxy, if valid, put them to usable_proxies.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36',
            'Connection': 'keep-alive'}

        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    self._conn.put(proxy)
                    print('Testing', proxy)
                    async with session.get(self.test_api, proxy=real_proxy, headers=headers, timeout=get_proxy_timeout) as response:
                        if response.status == 200:
                            #self._conn.put(proxy)
                            print('有效 proxy', proxy)
                except (ProxyConnectionError, TimeoutError, ValueError):
                    print('无效 proxy', proxy)
        except (ServerDisconnectedError, ClientResponseError,ClientConnectorError) as s:
            print(s)
            pass

    def test(self):
        """
        aio test all proxies.
        """
        print('ValidityTester is working')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            print('Async Error')

    def test_check(self, raw_proxies):
        """
        aio test all proxies.
        """
        print('ValidityTester is working')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy_check(proxy) for proxy in raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            print('Async Error')

    async def test_single_proxy_check(self, proxy):
        """
        text one proxy, if valid, put them to usable_proxies.
        """
        con = RedisClient()
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36', 'Connection':'keep-alive'}

        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    async with session.get(self.test_api, proxy=real_proxy, headers=headers, timeout=get_proxy_timeout) as response:
                        if response.status == 200:
                            print('有效 proxy', proxy)
                        else:
                            self._conn.remove(proxy)
                            print('无效 proxy里', proxy)
                except (ProxyConnectionError, TimeoutError, ValueError):
                    con.remove(proxy)
                    print('无效 proxy外', proxy)
        except (ServerDisconnectedError, ClientResponseError, ClientConnectorError) as s:
            con.remove(proxy)
            print('无效 proxy外', proxy)
            print(s)
            pass



class PoolAdder(object):
    """
    add proxy to pool
    """

    def __init__(self, threshold):
        self._threshold = threshold      # 代理池最大界限
        self._conn = RedisClient()
        self._tester = ValidityTester()
        self._crawler = FreeProxyGetter()

    def is_over_threshold(self):
        """
        judge if count is overflow.
        """
        if self._conn.get_len() >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        print('PoolAdder is working')
        proxy_count = 0
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback)
                # test crawled proxies
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError


if __name__ == '__main__':
    adder = PoolAdder(POOL_UPPER_THRESHOLD)
    adder.add_to_queue()