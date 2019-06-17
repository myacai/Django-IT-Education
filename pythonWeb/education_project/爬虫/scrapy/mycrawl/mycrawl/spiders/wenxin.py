import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mycrawl.redisDB import RedisClient
from mycrawl.items import MycrawlItem
from scrapy.http import HtmlResponse
import re

class WeixinSpider(CrawlSpider):
    name = 'ouwang'
    # allowed_domains = ['http://yuedu.anyv.net/']
    start_urls = ['http://wzrb.com.cn/']

    def __init__(self, *args, **kwargs):
        super(WeixinSpider, self).__init__(*args, **kwargs)
        self.redis = RedisClient()

    rules = (
        Rule(LinkExtractor(allow=(r'ArticleClass_.*.html',
                                  r'http://www.wzrb.com.cn/piclist.html',
                                  r'http://www.wzrb.com.cn/.*/piclist/.*.html'
                                  )),
             follow=True),

        Rule(LinkExtractor(allow=(r'article\d*show.html',)), follow=False),

    )

    """
    def parse_item(self, response):
        if not self.redis.is_exist(response.url):
            self.redis.put(response.url)
        else:
            return

    def parse_article(self, response):
        item = MycrawlItem()
        title, ctt, date, visitCount = run(response.url)
        item['title'] = title
        item['date'] = date
        item['visitCount'] = visitCount
        item['content'] = ctt
        item['url'] = str(response.url)
        yield item
    """

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return
        reg = r'article\d*show.html'
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                match = re.findall(reg, str(link.url))
                if match == []:
                    if self.redis.is_existArticle(link.url):
                        continue
                    else:
                        self.redis.putArticle(link.url)
                        seen.add(link)
                        r = self._build_request(n, link)
                        yield rule.process_request(r)             
                else:
                    self.redis.put(link.url)
 
                    



