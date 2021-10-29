"""2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
(необходимо анализировать оба поля зарплаты)"""
from pprint import pprint
from pymongo import MongoClient


client = MongoClient('127.0.0.1', 27017)
db = client['base_vacancy']
vacancy_db = db.vacancy


def search_max_salary(name_collection):
    count_num = 1
    try:
        user_salary = int(input("Enter max salary, rub: "))
        for i in name_collection.find({'salary_currency': 'USD','$or':
            [{'salary_max': {'$gt': user_salary * 0.0142}}, {'salary_min': {'$gt': user_salary * 0.0142}}]},
                                      {'_id': 0}):
            pprint(f'{count_num} {i}')
            count_num += 1
        for i in name_collection.find({'salary_currency': 'EUR','$or':
            [{'salary_max': {'$gt': user_salary * 0.0122}}, {'salary_min': {'$gt': user_salary * 0.0122}}]},
                                      {'_id': 0}):
            pprint(f'{count_num} {i}')
            count_num += 1
        for i in name_collection.find({'salary_currency': 'грн.', '$or':
            [{'salary_max': {'$gt': user_salary * 0.373}}, {'salary_min': {'$gt': user_salary * 0.373}}]},
                                      {'_id': 0}):
            pprint(f'{count_num} {i}')
            count_num += 1
        for i in name_collection.find({'salary_currency': 'руб.', '$or':
            [{'salary_max': {'$gt': user_salary}}, {'salary_min': {'$gt': user_salary}}]},
                                      {'_id': 0}):
            pprint(f'{count_num} {i}')
            count_num += 1
    except ValueError:
        print('The requested item must be a number!')




search_max_salary(vacancy_db)