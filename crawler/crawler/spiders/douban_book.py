import json
import re

import scrapy
from crawler.items import DoubanBookItem


class DoubanBookSpider(scrapy.Spider):
    name = 'douban-book'
    allowed_domains = ['book.douban.com']
    start_urls = ['http://book.douban.com/top250']

    def __init__(self, douban_id=None, *args, **kwargs):
        super(eval(self.__class__.__name__), self).__init__(*args, **kwargs)
        print('-' * 15 + ' [Douban Book][' + douban_id + '] ' + '-' * 15)
        self.start_urls = ['https://book.douban.com/subject/%s/' % douban_id]

    def parse(self, response):
        item = DoubanBookItem()
        data = json.loads(
            response.xpath('//script[@type="application/ld+json"]//text()').extract_first(),
            strict=False
        )
        item['id'] = re.sub(r'\D', "", data['url'])
        item['name'] = data['name']

        author_li = [a['name'] for a in data['author']]
        item['author'] = ', '.join(author_li)

        item['url'] = data['url']
        item['isbn'] = data['isbn']

        # Json 中没有的信息
        # 评分
        item['rating_val'] = response.xpath(
            'normalize-space(//strong[@class="ll rating_num "]/text())'
        ).extract_first()
        # 封面图片
        item['image'] = response.xpath(
            '//a[@class="nbg"]/@href'
        ).extract_first()

        data_aug = response.xpath('//div[@id="info"]')
        # 出版社
        item['press'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "出版社:")]/following::text()[1])'
        ).extract_first()
        # 出品方
        item['producer'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "出品方:")]/following::a/text())'
        ).extract_first()
        # 副标题
        item['subtitle'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "副标题:")]/following::text()[1])'
        ).extract_first()
        # 原作名
        item['original_title'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "原作名:")]/following::text()[1])'
        ).extract_first()

        # 译者 type1
        translator_li = data_aug.xpath(
            './/span[contains(./text(), " 译者")]/following-sibling::a/text()'
        ).extract()
        if len(translator_li) == 0:
            # 译者 type2
            translator_li = data_aug.xpath(
                'normalize-space(.//span[contains(./text(), "译者:")]/following::a/text())'
            ).extract()
        item['translator'] = ', '.join(translator_li)

        # 出版日期
        item['pub_date'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "出版年:")]/following::text()[1])'
        ).extract_first()
        # 页数
        item['paginal_num'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "页数:")]/following::text()[1])'
        ).extract_first()
        # 定价
        item['price'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "定价:")]/following::text()[1])'
        ).extract_first()
        # 装帧
        item['binding'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "装帧:")]/following::text())'
        ).extract_first()
        # 丛书
        item['series'] = data_aug.xpath(
            './span[contains(./text(), "丛书:")]/following::a/text()'
        ).extract_first()

        yield item