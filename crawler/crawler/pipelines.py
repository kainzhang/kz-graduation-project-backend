# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
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

            pattern = re.compile('[^\u4e00-\u9fa5]')
            content_tmp = pattern.sub('', item['content'])

            keywords_raw = analyse.extract_tags(content_tmp)
            keyword_list = []
            for keyword in keywords_raw:
                if keyword not in stop_words:
                    keyword_list.append(keyword)
            item['keywords'] = str(keyword_list[0:5]).replace("'", '"')

        item.save()

        return item
