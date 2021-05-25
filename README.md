# Graduation Project Backend

毕业设计采用前后端分离的开发方式，本仓库为后端部分，使用 Rest Framework 做后端接口。

**主要依赖：**
+ django 2.2
+ djangorestframework
+ django-cors-headers
+ djongo
+ scrapy
+ scrapy-djangoitem
+ scrapyd
+ scrapyd-client
+ selenium
+ requests

**数据库：**
+ MongoDB

**注意：**
1. 运行项目前确保已运行 `MongoDB Server`
2. Python环境中已配置 `Chromedriver`
3. 爬取豆瓣评论需要账号密码并完成手动登录
4. scrapy-deploy 文件的修改问题

## 安装依赖
安装 Poetry：osx / linux / bashonwindows
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```
进入项目根目录使用 Poetry 安装依赖
```
poetry install 
```

## 运行流程

### Django 运行
在项目根目录执行以下指令
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
douban api: [http://localhost:8000/douban/](http://localhost:8000/douban/)
user api: [http://localhost:8000/user/](http://localhost:8000/user/)
Django Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)


创建超级用户
```
python manage.py createsuperuser 
```

### Scrapy 爬虫

进入根目录下的 `crawler` 文件夹

终端命令爬取豆瓣电影个体和豆瓣读书的示例，参数为该作品的豆瓣 id
```
# 爬取电影信息
scrapy crawl douban-movie -a douban_id=1291561

# 爬取图书信息
scrapy crawl douban-book -a douban_id=10554308
```

可以在douban api 页面通过 douban_url 添加电影、图书，后台自动发请求爬取数据（数据显示有延迟，需手动刷新）

### Scrapyd 运行
由于`scrapy.utils.http` 已经不再使用，因此修改 scrapy-deploy
```
from scrapy.utils.project import inside_project
from scrapy.utils.http import basic_auth_header
from scrapy.utils.python import retry_on_eintr
from scrapy.utils.conf import get_config, closest_scrapy_cfg
```
⬆️ 以上第二行修改为
```
from w3lib.http import basic_auth_header
```
修改完毕后在 crawler 目录下运行
```
scrapyd
scrapyd-deploy -l
```
默认运行地址：[http://localhost:6800/
](http://localhost:6800/)

#### 🕷️ 豆瓣热门短评爬虫
热门短评由于豆瓣官方限制，不登录账号最多爬 220 条，登录后最多爬 500 条，由于热度动态改变，可能爬不满 220 或 500，以豆瓣官方 id 作为主键，数据库不会出现重复数据<br>

用户登录采用了手动登录，需要填写个人用户名和密码，运行爬虫时会弹出登录页面，手动拖动滑块完成登录验证<br>

豆瓣热门短评爬虫包括豆瓣电影和读书的热门短评爬取，为区分内容，为 spider 添加了两个参数，分别为评论类型和评论对象的 id，指令示例如下

```
# 豆瓣电影参数为 movie，数据库存储数据为 1
scrapy crawl douban-comment -a douban_type=movie -a douban_id=1292052

# 豆瓣读书类型为 book，数据库存储数据为 2
scrapy crawl douban-comment -a douban_type=book -a douban_id=6082808
```