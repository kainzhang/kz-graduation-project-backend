import json

import scrapy
from crawler.items import MovieItem


# 豆瓣电影 TOP250 爬虫
class MovieSpider(scrapy.Spider):
    name = 'douban-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        # 获取当前页面电影列表
        # li_list = response.xpath('//div[@class="article"]//li')
        # for li in li_list:
        #     li_href = li.xpath('.//div[@class="hd"]//a/@href').extract_first()
        #     if li_href is not None:
        #         yield scrapy.Request(
        #             li_href,
        #             callback=self.parse_info
        #         )
        #
        # # 进入下一页
        # nxt_href = response.xpath('//span[@class="next"]/a/@href').extract_first()
        # if nxt_href is not None:
        #     yield scrapy.Request(
        #         'https://movie.douban.com/top250' + nxt_href,
        #         callback=self.parse
        #     )

        # 单条测试
        yield scrapy.Request(
            'https://movie.douban.com/subject/1292722/',
            callback=self.parse_info
        )


    # 获取电影详细信息
    def parse_info(self, response):
        item = MovieItem()
        data = json.loads(
            response.xpath('//script[@type="application/ld+json"]//text()').extract_first(),
            strict=False
        )
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

        item['id'] = '1292722'


        # json 中不包含的数据
        data_aug = response.xpath('//div[@id="info"]')

        item['imbd'] = data_aug.xpath(
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

        yield item
