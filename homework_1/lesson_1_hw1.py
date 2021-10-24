"""1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json."""

import requests
import json

username = input("Enter the github username: ")

request = requests.get('https://api.github.com/users/'+username+'/repos?sort=updated')
json_f = request.json()

for i in range(0,len(json_f)):
  print("Project Number:",i+1)
  print("Project Name:",json_f[i]['name'])
  print("Project URL:",json_f[i]['svn_url'],"\n")

with open('data.json', 'w') as f:
    json.dump(json_f, f)