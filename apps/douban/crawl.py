import requests


# 爬豆瓣电影、图书信息
def crawl_item(douban_type, douban_id):
    url = 'http://127.0.0.1:6800/schedule.json'
    params = {
        'project': 'default',
        'spider': 'douban-' + douban_type,
        'douban_id': douban_id
    }
    response = requests.post(url=url, data=params)
    print(response.json())
    crawl_comment(douban_type, douban_id)


# 爬豆瓣电影、图书的热评
def crawl_comment(douban_type, douban_id):
    url = 'http://127.0.0.1:6800/schedule.json'
    params = {
        'project': 'default',
        'spider': 'douban-comment',
        'douban_type': douban_type,
        'douban_id': douban_id
    }
    response = requests.post(url=url, data=params)
    print(response.json())
