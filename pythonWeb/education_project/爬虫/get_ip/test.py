"""
import requests
import json
import re

ipHtml = requests.get('http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=b42ecf23a4ce4f4b9f8c43b84f400523&count=1&expiryDate=0&format=2&newLine=2')
reg = r'(.*?):'
i = re.findall(reg, ipHtml.text)[0]
reg2 = r':(\d*)'
port = re.findall(reg2, ipHtml.text)[0]
ip= i + ':' + port
#ip = i['msg'][0]['ip'] +':'+ i['msg'][0]['port'] 
print(ip)
proxies = {
                            'http': ip,
                            'https': ip,
                            }
r = requests.get('https://mp.weixin.qq.com/',proxies=proxies)
print(r.status_code)


"""


# -*- coding: utf-8 -*-

import requests
weixinId= "温州市发改委"
appid="c849a719741826b274ce1585676fc2f8"
url = "https://api.shenjian.io/?appid="+appid+"&weixinId="+weixinId
response = requests.get(url,
headers={
"Accept-Encoding": "gzip",
})
response.encoding = 'utf-8'
print(response.text)