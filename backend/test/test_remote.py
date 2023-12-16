import requests
import json

ip = input('Введите ip: ')

url = f'http://{ip}/predict'
data = {
    "yt_token": "afaksfkaofmsufioasf",
    "vk_token": "",
    "debug_text": "СПАСАЕМ ОГУРЦЫ ОТ ВСЕХ БОЛЕЗНЕЙ! Диагностика болезней огурцов по фотографиям Приобретая растения в "
                  "магазинах Procvetok вы помогаете развитию канала! ✓Россия: https://procvetok.ru/ ✓Беларусь: ..."
}

response = requests.post(url, json=data)
print(response.json())
