from PoolAdder import ValidityTester
from db import RedisClient


if __name__ == '__main__':
    raw_proxies = []
    con = RedisClient()
    proxyList = con.get_all()
    for ip in proxyList:
        raw_proxies.append(ip.decode('utf-8'))

    tester = ValidityTester()
    tester.test_check(raw_proxies)
