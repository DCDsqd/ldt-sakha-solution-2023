import requests
import json

url = 'http://127.0.0.1:8000/predict'
data = {
    "yt_token": "afaksfkaofmsufioasf",
    "vk_token": "",
    "tg_token": "",
    "tg_login": "",
    "tg_psw": ""
}

response = requests.post(url, json=data)
print(response.json())
