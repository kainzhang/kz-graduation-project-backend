import json
import re

import scrapy
from crawler.items import DoubanMovieItem


# 豆瓣电影 TOP250 爬虫
class MovieSpider(scrapy.Spider):
    name = 'douban-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def __init__(self, douban_id=None, *args, **kwargs):
        super(eval(self.__class__.__name__), self).__init__(*args, **kwargs)
        print('-' * 15 + ' [Douban Movie][' + douban_id + '] ' + '-' * 15)
        self.start_urls = ['https://movie.douban.com/subject/%s/' % douban_id]

    def parse(self, response):
        item = DoubanMovieItem()
        data = json.loads(
            response.xpath('//script[@type="application/ld+json"]//text()').extract_first(),
            strict=False
        )
        item['id'] = re.sub(r'\D', "", data['url'])
        item['name'] = data['name']
        item['image'] = data['image']
        item['url'] = 'https://movie.douban.com' + data['url']
        item['pub_date'] = data['datePublished']
        genre_li = data['genre']
        item['genre'] = ', '.join(genre_li)
        item['duration'] = data['duration']
        item['rating_val'] = data['aggregateRating']['ratingValue']
        item['description'] = data['description']
        director_li = [d['name'] for d in data['director']]
        item['director'] = ', '.join(director_li)
        author_li = [a['name'] for a in data['author']]
        item['author'] = ', '.join(author_li)
        actor_li = [a['name'] for a in data['actor']]
        item['actor'] = ', '.join(actor_li)

        # json 中不包含的数据
        data_aug = response.xpath('//div[@id="info"]')

        item['imdb'] = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "IMDb:")]/following::text()[1])'
        ).extract_first()

        region_li = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "制片国家/地区:")]/following::text()[1])'
        ).extract_first().split(' / ')
        item['region'] = ', '.join(region_li)

        language_li = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "语言:")]/following::text()[1])'
        ).extract_first().split(' / ')
        item['language'] = ', '.join(language_li)

        alias_li = data_aug.xpath(
            'normalize-space(./span[contains(./text(), "又名:")]/following::text()[1])'
        ).extract_first().split(' / ')
        item['alias'] = ', '.join(alias_li)

        item['stars5'] = response.xpath('//span[@class="stars5 starstop"]/following::span/text()').extract_first()
        item['stars4'] = response.xpath('//span[@class="stars4 starstop"]/following::span/text()').extract_first()
        item['stars3'] = response.xpath('//span[@class="stars3 starstop"]/following::span/text()').extract_first()
        item['stars2'] = response.xpath('//span[@class="stars2 starstop"]/following::span/text()').extract_first()
        item['stars1'] = response.xpath('//span[@class="stars1 starstop"]/following::span/text()').extract_first()

        yield item
