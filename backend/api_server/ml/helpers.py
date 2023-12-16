import zlib
import numpy as np
from google.cloud import storage
import os
import requests


def download_file_from_dropbox(url, local_destination):
    """Загружает файл по URL и сохраняет его локально."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_destination, 'wb') as file:
            file.write(response.content)
        print(f"Файл успешно загружен и сохранен в {local_destination}")
    else:
        print("Ошибка при загрузке файла:", response.status_code)


def download_model_if_not_exists(local_model_path, bucket_name, blob_name):
    """Загружает модель с Google Cloud Storage, если она не существует локально."""
    if not os.path.exists(local_model_path):
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.download_to_filename(local_model_path)
        print(f"Модель загружена из GCS и сохранена локально: {local_model_path}")
    else:
        print("Модель уже существует локально.")


def save_sklearn_model(model, filename):
    # Сохранение параметров модели в словарь
    model_params = model.get_params()
    # Конвертация словаря в байты
    params_bytes = np.array(list(model_params.items())).dumps()
    # Сжатие байтов
    compressed_bytes = zlib.compress(params_bytes)
    # Запись сжатых байтов в файл
    with open(filename, 'wb') as file:
        file.write(compressed_bytes)


def load_sklearn_model(filename, model_class):
    # Чтение сжатых байтов из файла
    with open(filename, 'rb') as file:
        compressed_bytes = file.read()
    # Распаковка байтов
    params_bytes = zlib.decompress(compressed_bytes)
    # Конвертация байтов обратно в словарь параметров
    model_params = dict(np.loads(params_bytes))
    # Восстановление модели
    model = model_class(**model_params)
    return model
