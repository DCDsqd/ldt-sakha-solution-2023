import requests
import json

url = 'http://127.0.0.1:8000/predict'
data = {
    "yt_token": "",
    "vk_token": "",
    "tg_posts": []
}

response = requests.post(url, json=data)
print(response.json())
