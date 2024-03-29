from datetime import datetime

import pydispatch.dispatcher
import scrapy
from crawler.items import DoubanCommentItem
from scrapy import signals
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class DoubanCommentSpider(scrapy.Spider):
    name = 'douban-comment'
    allowed_domains = ['douban.com']
    start_urls = []

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'crawler.middlewares.CrawlerDownloaderMiddleware': 400,
            'crawler.middlewares.DoubanLoginMiddleware': 500,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        },
    }

    item_type = None
    item_dad = -1
    root_url = None
    COMMENT_TYPE = {
        'movie': 1,
        'book': 2,
    }

    def __init__(self, douban_type=None, douban_id=None, *args, **kwargs):
        self.item_type = douban_type
        self.item_dad = douban_id

        if self.item_type == 'movie':
            print('-' * 15 + ' [Douban Movie][' + self.item_dad + '][Comments] ' + '-' * 15)
            self.root_url = 'https://movie.douban.com/subject/%s/comments' % self.item_dad
            self.start_urls = ['https://movie.douban.com/subject/%s/comments'
                               % self.item_dad]
        elif self.item_type == 'book':
            print('-' * 15 + ' [Douban Book][' + self.item_dad + '][Comments] ' + '-' * 15)
            self.root_url = 'https://book.douban.com/subject/%s/comments' % self.item_dad
            self.start_urls = ['https://book.douban.com/subject/%s/comments' % self.item_dad]

        my_settings = get_project_settings()
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(my_settings['WINDOW_WIDTH'], my_settings['WINDOW_HEIGHT'])
        self.browser.set_page_load_timeout(my_settings['SELENIUM_TIMEOUT'])
        self.wait = WebDriverWait(self.browser, 30)  # 加载元素超时时间

        super(eval(self.__class__.__name__), self).__init__(*args, **kwargs)
        pydispatch.dispatcher.connect(
            receiver=self.close_handle,
            signal=signals.spider_closed
        )

    def close_handle(self, spider):
        print('=' * 15 + 'Close Handle')
        self.browser.quit()

    def parse_content(self, response):
        if self.item_type == 'movie':
            comment_list = response.xpath('//div[@id="comments"]//div[@class="comment-item "]')
            for comment in comment_list:
                item = DoubanCommentItem()
                item['id'] = comment.xpath('@data-cid').extract_first()
                item['comment_type'] = self.COMMENT_TYPE[self.item_type]
                item['dad_id'] = self.item_dad
                item['author'] = comment.xpath('.//span[@class="comment-info"]/a/text()').extract_first()
                item['author_url'] = comment.xpath('.//span[@class="comment-info"]/a/@href').extract_first()

                item['rating_val'] = comment.xpath(
                    './/span[@class="comment-info"]/span[2]/@class'
                ).extract_first()[7:9]

                pub_date_str = comment.xpath('.//span[@class="comment-time "]/@title').extract_first()
                item['pub_date'] = datetime.strptime(pub_date_str, '%Y-%m-%d %H:%M:%S')
                item['content'] = comment.xpath('.//p[@class=" comment-content"]/span/text()').extract_first()
                yield item

        elif self.item_type == 'book':
            comment_list = response.xpath('//div[@id="comments"]//li[@class="comment-item"]')
            if len(comment_list) == 0:
                return

            for comment in comment_list:
                item = DoubanCommentItem()
                item['id'] = comment.xpath('@data-cid').extract_first()
                item['comment_type'] = self.COMMENT_TYPE[self.item_type]
                item['dad_id'] = self.item_dad
                item['author'] = comment.xpath('.//span[@class="comment-info"]/a/text()').extract_first()
                item['author_url'] = comment.xpath('.//span[@class="comment-info"]/a/@href').extract_first()

                item['rating_val'] = comment.xpath(
                    './/span[@class="comment-info"]/span[1]/@class'
                ).extract_first()[18:20]

                pub_date_str = comment.xpath('.//span[@class="comment-time"]/text()').extract_first()
                item['pub_date'] = datetime.strptime(pub_date_str, '%Y-%m-%d')
                item['content'] = comment.xpath('.//p[@class="comment-content"]/span/text()').extract_first()
                yield item

        # 翻页
        nxt_href = response.xpath('//a[@data-page="next"]/@href').extract_first()
        if nxt_href is not None:
            print(nxt_href)
            yield scrapy.Request(
                self.root_url + nxt_href,
                meta={'needLogin': False},
                callback=self.parse_content,
            )
        else:
            print('GG')

    def parse(self, response):
        # 验证登录
        login_sign = response.xpath('//a[@class="nav-login"]/text()').extract_first()
        if login_sign is not None:  # 未登录
            print('+' * 20 + '去登录了!')
            yield scrapy.Request(
                self.start_urls[0],
                meta={'needLogin': True},
                callback=self.parse_content
            )
        else:
            yield scrapy.Request(
                self.start_urls[0],
                meta={'needLogin': False},
                callback=self.parse_content
            )
