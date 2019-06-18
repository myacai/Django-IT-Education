from PoolAdder import ValidityTester,PoolAdder
from db import RedisClient
from settings import POOL_UPPER_THRESHOLD
import time

def check():
    raw_proxies = []
    con = RedisClient()
    proxyList = con.get_all()
    for ip in proxyList:
        raw_proxies.append(ip.decode('utf-8'))

    tester = ValidityTester()
    tester.test_check(raw_proxies)
    
def add_ip():
    adder = PoolAdder(POOL_UPPER_THRESHOLD)
    adder.add_to_queue()

def ip_run():
    while(1):
        check()
        add_ip()
        time.sleep(300)
        
if __name__ == '__main__':    
    ip_run()
