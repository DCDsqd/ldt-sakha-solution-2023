import numpy as np

from parser.vk_parser import VKGroup, VKLike, VKWallPost

from ml.model_predict import universal_predict


def analyze_vk_groups(vk_groups: list[VKGroup],
                      text_model,
                      multi_label_binarizer,
                      USE_BERT,
                      tokenizer):

    classes_list = multi_label_binarizer.classes_
    num_classes = len(classes_list)
    total_group_probabilities = np.zeros(num_classes)
    group_count = np.zeros(num_classes)

    group_diffs = []
    group_names = []

    for group in vk_groups:
        group_text = " ".join(group.posts)  # Объединение всех постов группы в один текст
        _predictions_classes, predicted_probabilities = universal_predict(
            text_model,
            USE_BERT,
            group_text,
            tokenizer,
            multi_label_binarizer
        )
        total_group_probabilities += predicted_probabilities
        group_count += (predicted_probabilities > 0).astype(int)
        group_names.append(group.name)

    # Вычисляем среднее значение вероятности для каждой категории по всем группам
    average_probabilities = total_group_probabilities / np.maximum(group_count, 1)

    # Вычисляем разницу для каждой группы
    for group in vk_groups:
        group_text = " ".join(group.posts)
        _predictions_classes, group_probabilities = universal_predict(
            text_model,
            USE_BERT,
            group_text,
            tokenizer,
            multi_label_binarizer
        )
        diffs = np.sum(np.abs(group_probabilities - average_probabilities))
        group_diffs.append((group, diffs))

    # Сортируем группы по разницам
    sorted_groups = sorted(group_diffs, key=lambda x: x[1])

    average_results = dict(zip(classes_list, average_probabilities))
    sorted_group_names = [group[0].name for group in sorted_groups]

    return average_results, sorted_group_names


def analyze_vk_likes(vk_likes: list[VKLike],
                     text_model,
                     multi_label_binarizer,
                     USE_BERT,
                     tokenizer):

    classes_list = multi_label_binarizer.classes_
    num_classes = len(classes_list)
    total_likes_probabilities = np.zeros(num_classes)
    likes_count = np.zeros(num_classes)

    like_diffs = []
    like_texts = []

    for like in vk_likes:
        _predictions_classes, predicted_probabilities = universal_predict(
            text_model,
            USE_BERT,
            like.text,
            tokenizer,
            multi_label_binarizer
        )
        total_likes_probabilities += predicted_probabilities
        likes_count += (predicted_probabilities > 0).astype(int)
        like_texts.append(like.text)

    average_probabilities = total_likes_probabilities / np.maximum(likes_count, 1)

    for like, text in zip(vk_likes, like_texts):
        _predictions_classes, like_probabilities = universal_predict(
            text_model,
            USE_BERT,
            text,
            tokenizer,
            multi_label_binarizer
        )
        diffs = np.sum(np.abs(like_probabilities - average_probabilities))
        like_diffs.append((like, diffs))

    sorted_likes = sorted(like_diffs, key=lambda x: x[1])

    average_results = dict(zip(classes_list, average_probabilities))
    sorted_like_texts = [like[0].text for like in sorted_likes]

    return average_results, sorted_like_texts
