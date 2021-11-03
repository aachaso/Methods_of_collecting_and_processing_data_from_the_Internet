'''Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru,
lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
Сложить собранные новости в БД'''

import requests
from pprint import pprint
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'}
url = 'https://lenta.ru/'
response = requests.get(url, headers=header)
client = MongoClient('127.0.0.1', 27017)
db = client['base_news']
news_db = db.news

def add_doc_collection(name_collection,name_doc):
    try:
        name_collection.insert_one(name_doc)
    except dke:
        print(f"Запись с id {name_doc['_id']} уже существует в базе")

dom = html.fromstring(response.text)


items = dom.xpath('''//section[@class="row b-top7-for-main js-top-seven"]//div[@class="first-item"]/h2 | 
                        //section[@class="row b-top7-for-main js-top-seven"]//div[@class="item"]''')


news = []
for item in items:
    one_new_data = {}

    name = item.xpath(".//a/text()")
    link = item.xpath(".//a/@href")
    date = item.xpath('.//a/time[@class="g-time"]/@datetime')

    one_new_data['_id'] = f'{url}{"".join(link)}{"".join(name)}'
    one_new_data['site'] = url
    one_new_data['name'] = ''.join(name).replace(u'\xa0', u' ')
    one_new_data['link'] = f'{url}{"".join(link)}'
    one_new_data['date'] = ''.join(date)
    add_doc_collection(news_db, one_new_data)
