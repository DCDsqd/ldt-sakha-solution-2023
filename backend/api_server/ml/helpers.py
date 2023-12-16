import zlib
import numpy as np


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
