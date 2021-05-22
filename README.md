# Graduation Project Backend

毕业设计采用前后端分离的开发方式，本仓库为后端部分，使用 Rest Framework 做后端接口。

**主要依赖：**
+ django 2.2
+ djangorestframework
+ django-cors-headers
+ djongo
+ scrapy
+ scrapy-djangoitem 
+ scrapy-fake-useragent
+ scrapyd
+ selenium

**数据库：**
+ MongoDB

**注意：**
1. 运行项目前确保已运行 `MongoDB Server`
2. Python环境中已配置 `Chromedriver`
3. 爬取豆瓣评论需要账号密码并完成手动登录

## 安装依赖
安装 Poetry<br>
`osx / linux / bashonwindows install instructions`
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
进入项目根目录使用 Poetry 安装依赖
```
poetry install 
```

## 运行流程

### 运行 Django

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

创建超级用户
```
python manage.py createsuperuser 
```

### 运行 Scrapy

进入根目录下的 `crawler` 文件夹

爬取豆瓣电影个体的示例，参数为该电影的豆瓣 id
```
scrapy crawl douban-movie -a douban_id=1291561
```