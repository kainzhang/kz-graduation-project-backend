import requests


def main():
    url = 'http://127.0.0.1:6800/schedule.json'

    params = {
        'project': 'default',
        'spider': 'douban-movie',
        'douban_id': '1849031'
    }

    response = requests.post(url=url, data=params)
    print(response.json())


if __name__ == '__main__':
    main()
