# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

class CrawlerPipeline:
    def process_item(self, item, spider):
        if spider.name == 'douban-book':
            for key in item:
                if isinstance(item[key], str) and item[key] == '':
                    item[key] = None
        elif spider.name == 'douban-comment':
            item['content'] = item['content'].replace('\n', '')

        item.save()

        return item
