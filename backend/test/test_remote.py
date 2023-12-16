import requests
import json

ip = input('Введите ip: ')

url = f'http://{ip}/predict'
data = {
    "yt_token": "afaksfkaofmsufioasf",
    "vk_token": "",
    "debug_text": "вау я люблю лечить людей и быть врачем ммм круто"
}

response = requests.post(url, json=data)
print(response.json())
