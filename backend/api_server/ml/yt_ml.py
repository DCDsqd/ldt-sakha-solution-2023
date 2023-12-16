import numpy as np

from backend.api_server.parser.common import clean_text_for_model
from backend.api_server.parser.yt_parser import YTChannel, YTVideoInfo


def analyze_youtube_list_of_vids(videos: list[YTVideoInfo],
                                 text_model,
                                 multi_label_binarizer) -> (dict, list):
    classes_list = multi_label_binarizer.classes_
    num_classes = len(classes_list)

    # Инициализируем массивы для хранения общих вероятностей и счетчиков видео
    total_probabilities = np.zeros(num_classes)
    video_count = np.zeros(num_classes)

    # Список для хранения вероятностей каждого видео
    video_probabilities_list = []

    # Анализируем каждое видео
    for video in videos:
        concat_text = video.concatenate_text()
        concat_text = clean_text_for_model(concat_text)
        predicted_probabilities = text_model.predict_proba([concat_text])[0]

        # Добавляем вероятности текущего видео в список
        video_probabilities_list.append(predicted_probabilities)

        # Обновляем общие вероятности и счетчик видео
        total_probabilities += predicted_probabilities
        video_count += (predicted_probabilities > 0).astype(int)

    # Вычисляем средние вероятности для каждой категории
    average_probabilities = total_probabilities / np.maximum(video_count, 1)

    # Считаем разницу каждого видео от среднего
    video_diffs = [np.sum(np.abs(video_probs - average_probabilities)) for video_probs in video_probabilities_list]

    # Сортируем видео по разницам от среднего
    sorted_video_indices = np.argsort(video_diffs)
    sorted_videos = [videos[i] for i in sorted_video_indices]

    # Возвращаем средние вероятности и отсортированный список видео
    return dict(zip(classes_list, average_probabilities)), sorted_videos


def analyze_youtube_user_subscriptions(youtube_user_subscriptions: list[YTChannel],
                                       text_model,
                                       multi_label_binarizer) -> (dict, list):
    classes_list = multi_label_binarizer.classes_
    num_classes = len(classes_list)
    total_channel_probabilities = np.zeros(num_classes)
    channel_count = np.zeros(num_classes)

    channel_diffs = []
    channel_names = []

    # Сначала агрегируем все вероятности
    for youtube_user_subbed_channel in youtube_user_subscriptions:
        channel_videos = youtube_user_subbed_channel.gather_videos(youtube_user_subscriptions)
        for video in channel_videos:
            concat_text = video.concatenate_text()
            concat_text = clean_text_for_model(concat_text)
            predicted_probabilities = text_model.predict_proba([concat_text])[0]
            total_channel_probabilities += predicted_probabilities
            channel_count += (predicted_probabilities > 0).astype(int)

    # Затем вычисляем средние вероятности
    average_probabilities = total_channel_probabilities / np.maximum(channel_count, 1)

    # Теперь вычисляем разницы для каждого канала
    for youtube_user_subbed_channel in youtube_user_subscriptions:
        channel_videos = youtube_user_subbed_channel.gather_videos(youtube_user_subscriptions)
        channel_probabilities = np.zeros(num_classes)  # Сброс для каждого канала

        for video in channel_videos:
            concat_text = video.concatenate_text()
            concat_text = clean_text_for_model(concat_text)
            predicted_probabilities = text_model.predict_proba([concat_text])[0]
            channel_probabilities += predicted_probabilities

        # Вычисляем разницу со средними вероятностями
        diffs = np.sum(np.abs(channel_probabilities / len(channel_videos) - average_probabilities))
        channel_diffs.append(diffs)
        channel_names.append(youtube_user_subbed_channel.title)

    # Сортируем каналы по разницам
    sorted_indices = np.argsort(channel_diffs)
    sorted_channels = [channel_names[i] for i in sorted_indices]

    average_results = dict(zip(classes_list, average_probabilities))

    return average_results, sorted_channels
