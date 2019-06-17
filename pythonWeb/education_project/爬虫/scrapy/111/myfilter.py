import re
from bs4 import BeautifulSoup, Comment
import requests
import chardet
import random

authorset = {'责任编辑', '阿菜'}

ip_list = ['122.114.31.177:808',
         '61.135.217.7:80',
         '122.114.31.177:808',
         '61.135.217.7:80','',
         '61.136.163.244:8103',
         '115.84.179.249:7777',



        '121.42.167.160:3128',
        '177.184.136.74:20183',
        '200.187.87.138:20183',

        '140.205.222.3:80',
         ]


UserAgent_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36 OPR/53.0.2907.99',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0']

first_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Host": "www.wzrb.com.cn",
        "Proxy-Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": UserAgent_list[0],
        }


def getip():
    ip = random.choice(ip_list)
    proxies = {
        'http': ip,
        'https': ip,
    }
    return  proxies

def get_headers():
    UserAgent = random.choice(UserAgent_list)
    first_headers['User-Agent'] = UserAgent
    return first_headers

def getcontentfromweb(src):
    headers = get_headers()
    # proxies = getip()proxies=proxies,
    obj = requests.get(src, headers=headers, timeout=8)
    #obj.encoding = 'gb2312'

    try:
        result = chardet.detect(obj.content)
        obj.encoding = str(result['encoding'])
    except Exception:
        pass
		
    return obj.text


def getTitle(html):
    titleFilter = r'<title>([\s\S]*?)</title>'
    h1Filter = r'<h1.*?>(.*?)</h1>'
    # clearFilter = r"<.*?>"

    title = ""
    match = re.findall(titleFilter, html)
    if match:
        try:
            title = match[0]
        except Exception:
            title = ' '

    match = re.findall(h1Filter, html)
    if match:
        try:
            h1 = match[0]
            if h1 and title.startswith(h1):
                title = h1
        except Exception:
            h1 = ' '

    return title


def getDate(html):
    text = re.sub('(?is)<.*?>', '', html)
    reg = r'((\d{4}|\d{2})(\-|\/)\d{1,2}\3\d{1,2})(\s?\d{2}:\d{2})?|(\d{4}年\d{1,2}月\d{1,2}日)(\s?\d{2}:\d{2})?'
    match = re.findall(reg, text)
    dateStr = ''
    if match:
        try:
            date = match[0]
            if type(date) is tuple:
                dateStr = date[0]
        except Exception:
            date = ''
            dateStr = ''
    return dateStr


def getVisit(html):
    text = re.sub('(?is)<.*?>', '', html)
    reg = r'浏览：(\d*)'
    match = re.findall(reg, text)
    visitCount = 0
    if match:
        try:
            visitCount = int(match[0])
        except Exception:
            visitCount = 0
    """
    reg2 = r'阅读：(\d*)'
    match2 = re.findall(reg2, text)
    if match2 and visitCount == 0:
        try:
            visitCount = int(match2[0])
        except Exception:
            visitCount = 0
    """
    return visitCount


def filter_tags(html_str):
    soup = BeautifulSoup(html_str)
    title = getTitle(html_str)
    date = getDate(html_str)
    visitCount = getVisit(html_str)
    [script.extract() for script in soup.findAll('script')]
    [style.extract() for style in soup.findAll('style')]
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    [comment.extract() for comment in comments]
    reg1 = re.compile("<[^>]*>")
    content = reg1.sub('', soup.prettify()).split('\n')
    return title, content, date, visitCount


def getcontent(lst, title, authorset):
    lstlen = [len(x) for x in lst]
    threshold = 50
    startindex = 0
    maxindex = lstlen.index(max(lstlen))
    endindex = 0
    for i, v in enumerate(lstlen[:maxindex - 3]):
        if v > threshold and lstlen[i + 1] > 5 and lstlen[i + 2] > 5 and lstlen[i + 3] > 5:
            startindex = i
            break
    for i, v in enumerate(lstlen[maxindex:]):
        if v < threshold and lstlen[maxindex + i + 1] < 10 and lstlen[maxindex + i + 2] < 10 and lstlen[
            maxindex + i + 3] < 10:
            endindex = i
            break
    content = ['<p>' + x.strip() + '</p>' for x in lst[startindex:endindex + maxindex] if len(x.strip()) > 0]
    return content


def run(url):
    ctthtml = getcontentfromweb(url)
    title, content, date, visitCount = filter_tags(ctthtml)
    newcontent = getcontent(content, title, authorset)
    ctt = ''.join(newcontent)
    return title, ctt, date, visitCount

if __name__ == '__main__':
    url = "http://www.wzrb.com.cn/ow2016/piclist/article771389show.html"
    title, ctt, date, visitCount = run(url)
    print(title)
