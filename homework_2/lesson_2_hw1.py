"""Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность)
с сайтов HH(обязательно) и/или Superjob(по желанию).
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
- Наименование вакансии.
- Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
- Ссылку на саму вакансию.
- Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv."""

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd



url_hh = 'https://www.hh.ru'
url_sj = 'https://www.superjob.ru'
user_text = input("Enter the direction of work: ")

params_hh = {'area': 1,
          'fromSearchLine': 'true',
          'text': user_text,
          'page': 0}

params_sj = {'keywords': user_text,
             'noGeo': 1,
             'page': 1}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}


vacancy_list = []
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


            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['company_name'] = company_name
            vacancy_data['site'] = 'hh.ru'
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = salary_currency
            vacancy_list.append(vacancy_data)
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


            vacancy_data['name'] = name
            vacancy_data['link'] = link
            vacancy_data['company_name'] = company_name
            vacancy_data['site'] = 'superjob.ru'
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = salary_currency
            vacancy_list.append(vacancy_data)
        print(f"Обработана {params_sj['page']} страница с {url_sj}")
        params_sj['page'] += 1
    else:
        break


df = pd.DataFrame(vacancy_list)
print(df.sample(n=5))

df.to_csv("data.csv", sep=";", encoding="utf-8")


