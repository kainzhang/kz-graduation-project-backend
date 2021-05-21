import datetime

import scrapy
from crawler.items import DoubanCommentItem


class DoubanCommentSpider(scrapy.Spider):
    name = 'douban-comment'
    allowed_domains = ['douban.com']
    start_urls = []
    item_type = None
    item_dad = -1
    root_url = 'https://movie.douban.com/subject/%s/comments'
    COMMENT_TYPE = {
        'Movie': 1,
        'Book': 2,
    }

    def __init__(self, douban_type=None, douban_id=None, *args, **kwargs):
        super(eval(self.__class__.__name__), self).__init__(*args, **kwargs)
        self.item_type = douban_type
        self.item_dad = douban_id
        if douban_type == 'Movie':
            print('-' * 15 + ' [Douban Movie][' + douban_id + '][Comments] ' + '-' * 15)
            self.start_urls = ['https://movie.douban.com/subject/%s/comments?start=460&limit=20&status=P&sort=new_score'
                               % douban_id]
        # elif douban_type == 'Book':
        #     print('-' * 15 + ' [Douban Book][' + douban_id + '][Comments] ' + '-' * 15)
        #     self.start_urls = ['https://book.douban.com/subject/%s/comments/' % douban_id]

    def parse(self, response):
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
            item['pub_date'] = datetime.datetime.strptime(pub_date_str, '%Y-%m-%d %H:%M:%S')

            item['content'] = comment.xpath('.//p[@class=" comment-content"]/span/text()').extract_first()
            yield item

        nxt_href = response.xpath('//a[@class="next"]/@href').extract_first()
        if nxt_href is not None:
            print(nxt_href)
            yield scrapy.Request(
                self.root_url + nxt_href,
                callback=self.parse
            )
        else:
            print('GG')
