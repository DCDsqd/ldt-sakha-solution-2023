import requests
import json

url = 'http://127.0.0.1:8000/predict'
data = {
    "yt_token": "ya29.a0AfB_byCxS6UH98Ne6ym2rN50LAnf6aGWEiAgDrVZKT7L4MpAK9XNR6D_ll24-LREMjFw767EhOa-7XnmnzXzQ1I3DGXusNCifRbg073RMvyHAlJQel-qyM0cFk5IDpOIDisLlLTaQBIHqtbXYRUB0xWBkwHNx8GX3wusaCgYKAWwSARMSFQHGX2MiAA9NFKpsUDxGaMKYU4ezfA0171",
    "vk_token": "",
    "tg_posts": []
}

response = requests.post(url, json=data)
print(response.json())
