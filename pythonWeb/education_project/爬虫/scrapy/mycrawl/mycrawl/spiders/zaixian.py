import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from mycrawl.redisDB import RedisClient
from mycrawl.myfilter import run
from mycrawl.items import ZaixianlItem


class ZaixianSpider(CrawlSpider):
    name = 'zaixian'
    # allowed_domains = ['http://yuedu.anyv.net/']
    start_urls = ['http://www.wz.ccoo.cn/']

    def __init__(self, *args, **kwargs):
        super(ZaixianSpider, self).__init__(*args, **kwargs)
        self.redis = RedisClient()

    rules = (
        # Rule(LinkExtractor(allow=(r'ArticleClass_.*.html',)), callback='parse_item',follow=True),

        # Rule(LinkExtractor(allow=(r'article\d*show.html',)), callback='parse_article', follow=False),
        Rule(LinkExtractor(allow=(r'.*tieba/.*',)
                           ,),
             callback='parse_item', follow=True),

        Rule(LinkExtractor(allow=(r'http://www.wz.ccoo.cn/forum/.*.html',)), callback='parse_article', follow=False),
    )

    def parse_item(self, response):
        # self.logger.info('Hi, this is an item page! %s', response.url)
        print('Hi, this is an item page! %s' % (response.url))
        if not self.redis.is_existZaixian(response.url):
            self.redis.putArticleZaixian(response.url)

        # item = scrapy.Item()
        # item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        # item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        # item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()
        # return item

    def parse_article(self, response):
        item = ZaixianlItem()
        #print('1')
        if not self.redis.is_existZaixian(response.url):
            self.redis.putArticleZaixian(response.url)
            title, ctt, date, visitCount = run(response.url)
            # print(title)
            item['title'] = title
            item['date'] = date
            item['visitCount'] = visitCount
            item['content'] = ctt
            item['url'] = str(response.url)
            yield item

