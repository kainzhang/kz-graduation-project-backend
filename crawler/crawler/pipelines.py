# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from math import fabs
from urllib.request import urlretrieve

import jieba
from jieba import analyse
from snownlp import SnowNLP

stop_words = [line.strip() for line in open('../data/stopwords.txt', encoding='utf-8').readlines()]


class CrawlerPipeline:
    def process_item(self, item, spider):
        if spider.name == 'douban-movie' or spider.name == 'douban-book':
            for key in item:
                item[key] = item[key].replace('&#39;', "'")
                if isinstance(item[key], str) and item[key] == '':
                    item[key] = None
            urlretrieve(item['image'], '../media/img/' + item['id'] + '.jpg')

        elif spider.name == 'douban-comment':
            item['content'] = item['content'].replace('\n', '')
            res = SnowNLP(item['content'])
            item['senti_score'] = res.sentiments

            """
            根据评分调整分数
            """
            if item['rating_val'] != '-t' and item['rating_val'] != '':
                rating = int(item['rating_val']) * 2.0 / 100
                if fabs(item['senti_score'] - rating) > 0.3:
                    item['senti_score'] = (item['senti_score'] + rating) * 0.5

            # pattern = re.compile('[^\u4e00-\u9fa5]')
            # content_tmp = pattern.sub('', item['content'])

            keywords_raw = analyse.extract_tags(item['content'])
            keyword_list = []
            for keyword in keywords_raw:
                if len(keyword) == 1 and (keyword < '\u4e00' or keyword > '\u9fa5'):
                    continue
                elif keyword[0] < '\u4e00' or keyword[0] > '\u9fa5':
                    continue
                if keyword not in stop_words:
                    keyword_list.append(keyword)
            item['keywords'] = str(keyword_list[0:5]).replace("'", '"')

        item.save()

        return item
