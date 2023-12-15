import requests
import json

ip = input('Введите ip: ')

url = f'http://{ip}/predict'
data = {
    "yt_token": "afaksfkaofmsufioasf",
    "vk_token": "",
    "tg_token": "",
    "tg_login": "",
    "tg_psw": ""
}

response = requests.post(url, json=data)
print(response.json())
