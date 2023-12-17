import requests
import json

url = 'http://127.0.0.1:8000/predict'
data = {
    "yt_token": "ya29.a0AfB_byDoGvI81nOJ0VCqZNuvO_S66rpNzJoNln9fg8SiLpGgA18gTyfV2ioDexyEshz-rCQgL7L8E8uKrT6JhWHP6hSbMEvOZzUhYV2wO2e-SsnuQUwgwqgkcf1OsTPHOil54sR70jd17oGbiovfjqyLi0imtxW_F07HaCgYKASYSARMSFQHGX2MifUY2TJzd_QT7w6DtAWubJw0171",
    "vk_token": "",
    "debug_text": ""
}

response = requests.post(url, json=data)
print(response.json())
