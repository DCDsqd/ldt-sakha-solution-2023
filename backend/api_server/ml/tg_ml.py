import numpy as np

from model_predict import universal_predict


def analyze_tg_list_of_texts(texts: list[str],
                             text_model,
                             multi_label_binarizer,
                             USE_BERT,
                             tokenizer) -> dict:

    classes_list = multi_label_binarizer.classes_
    num_classes = len(classes_list)

    # Инициализируем массивы для хранения общих вероятностей
    total_probabilities = np.zeros(num_classes)

    for text in texts:
        if text:  # Проверка, что текст не пустой
            _predictions_classes, predicted_probabilities = universal_predict(
                text_model,
                USE_BERT,
                text,
                tokenizer,
                multi_label_binarizer
            )
            total_probabilities += predicted_probabilities

    # Вычисляем средние вероятности
    if len(texts) > 0:
        average_probabilities = total_probabilities / len(texts)
    else:
        average_probabilities = total_probabilities

    return dict(zip(classes_list, average_probabilities))
