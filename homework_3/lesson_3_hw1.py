"""1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
которая будет добавлять только новые вакансии/продукты в вашу базу."""

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

client = MongoClient('127.0.0.1', 27017)

url_hh = 'https://www.hh.ru'
url_sj = 'https://www.superjob.ru'
user_text = input("Enter the direction of work: ")
db = client['base_vacancy']
vacancy_db = db.vacancy

params_hh = {'area': 1,
          'fromSearchLine': 'true',
          'text': user_text,
          'page': 0}

params_sj = {'keywords': user_text,
             'noGeo': 1,
             'page': 1}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

# функция

def add_doc_collection(name_collection,name_doc):
    try:
        name_collection.insert_one(name_doc)
    except dke:
        print(f"Вакансия с id {name_doc['_id']} уже существует в базе")


while True:
    response = requests.get(url_hh + '/search/vacancy', params=params_hh, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

    if response.ok and vacancies:
        for vacancy in vacancies:
            vacancy_data = {}
            info = vacancy.find('a', {'class': 'bloko-link'})
            name = info.text
            link = info['href']
            company_name = vacancy.find('a', {'class': 'bloko-link_secondary'}).text.replace(u'\xa0', u' ')

            try:
                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text.split()
                if salary[0] == "до":
                    salary_min = None
                    salary_max = int(salary[1] + salary[2])
                    salary_currency = salary[3]
                elif salary[0] == "от":
                    salary_min = int(salary[1] + salary[2])
                    salary_max = None
                    salary_currency = salary[3]
                else:
                    salary_min = int(salary[0] + salary[1])
                    salary_max = int(salary[3] + salary[4])
                    salary_currency = salary[5]
            except:
                salary_min = None
                salary_max = None
                salary_currency = None

            vacancy_data['_id'] = name+link+company_name
            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['company_name'] = company_name
            vacancy_data['site'] = 'hh.ru'
            vacancy_data['direction of work'] = user_text
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = salary_currency
            add_doc_collection(vacancy_db, vacancy_data)
        print(f"Обработана {params_hh['page']+1} страница с {url_hh}")
        params_hh['page'] += 1
    else:
        break

while True:
    response = requests.get(url_sj + '/vacancy/search/', params=params_sj, headers=headers)
    dom = bs(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'f-test-search-result-item'})

    if response.ok and vacancies:
        for vacancy in vacancies:
            vacancy_data = {}
            try:
                info = vacancy.find('a')
                name = info.text
                link = url_sj + info['href']
                company_name = vacancy.find('span', {'class': 'f-test-text-vacancy-item-company-name'}).text
            except:
                pass

            try:
                salary = vacancy.find('span', {'class': 'f-test-text-company-item-salary'}).text.split()
                if salary[0] == "По":
                    salary_min = None
                    salary_max = None
                    salary_currency = None
                elif salary[0] == "до":
                    salary_min = None
                    salary_max = int(salary[1] + salary[2])
                    salary_currency = salary[3][0:4]
                elif salary[0] == "от":
                    salary_min = int(salary[1] + salary[2])
                    salary_max = None
                    salary_currency = salary[3][0:4]
                else:
                    salary_min = int(salary[0] + salary[1])
                    salary_max = int(salary[3] + salary[4])
                    salary_currency = salary[5][0:4]
            except:
                pass

            vacancy_data['_id'] = name+link+company_name
            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['company_name'] = company_name
            vacancy_data['site'] = 'superjob.ru'
            vacancy_data['direction of work'] = user_text
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = salary_currency
            add_doc_collection(vacancy_db, vacancy_data)
        print(f"Обработана {params_sj['page']} страница с {url_sj}")
        params_sj['page'] += 1
    else:
        break
