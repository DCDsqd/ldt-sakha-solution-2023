import numpy as np

from parser.common import clean_text_for_model
from parser.yt_parser import YTChannel, YTVideoInfo
from ml.model_predict import universal_predict


def analyze_youtube_list_of_vids(videos: list[YTVideoInfo],
                                 text_model,
                                 multi_label_binarizer,
                                 USE_BERT,
                                 tokenizer) -> (dict, list[YTVideoInfo]):
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
        _predictions_classes, predicted_probabilities = universal_predict(
            text_model,
            USE_BERT,
            concat_text,
            tokenizer,
            multi_label_binarizer
        )

        # Добавляем вероятности текущего видео в список
        video_probabilities_list.append(predicted_probabilities)

        # Обновляем общие вероятности и счетчик видео
        total_probabilities += predicted_probabilities
        video_count += (np.array(predicted_probabilities) > 0).astype(int)

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
                                       multi_label_binarizer,
                                       youtube_api_instance,
                                       USE_BERT,
                                       tokenizer) -> (dict, list[YTChannel]):
    classes_list = multi_label_binarizer.classes_
    num_classes = len(classes_list)
    total_channel_probabilities = np.zeros(num_classes)
    channel_count = np.zeros(num_classes)

    # Сначала агрегируем все вероятности
    for youtube_user_subbed_channel in youtube_user_subscriptions:
        channel_videos = youtube_user_subbed_channel.gather_videos(youtube_api_instance)
        if channel_videos:  # Проверка на наличие видео в канале
            for video in channel_videos:
                concat_text = video.concatenate_text()
                concat_text = clean_text_for_model(concat_text)
                _predictions_classes, predicted_probabilities = universal_predict(
                    text_model,
                    USE_BERT,
                    concat_text,
                    tokenizer,
                    multi_label_binarizer
                )
                total_channel_probabilities += predicted_probabilities
                channel_count += (np.array(predicted_probabilities) > 0).astype(int)

    # Вычисляем средние вероятности
    average_probabilities = total_channel_probabilities / np.maximum(channel_count, 1)

    channel_diffs = np.array([])
    channels = []

    # Теперь вычисляем разницы для каждого канала
    for youtube_user_subbed_channel in youtube_user_subscriptions:
        channel_videos = youtube_user_subbed_channel.gather_videos(youtube_api_instance)
        channel_probabilities = np.zeros(num_classes)

        if channel_videos:
            for video in channel_videos:
                concat_text = video.concatenate_text()
                concat_text = clean_text_for_model(concat_text)
                _predictions_classes, predicted_probabilities = universal_predict(
                    text_model,
                    USE_BERT,
                    concat_text,
                    tokenizer,
                    multi_label_binarizer
                )
                channel_probabilities += predicted_probabilities

            # Вычисляем разницу со средними вероятностями
            channel_avg_probabilities = channel_probabilities / len(channel_videos)
            diffs = np.sum(np.abs(channel_avg_probabilities - average_probabilities))
        else:
            diffs = np.inf

        channel_diffs = np.append(channel_diffs, diffs)
        channels.append(youtube_user_subbed_channel)

    # Сортировка индексов каналов на основе их различий
    sorted_indices = np.argsort(channel_diffs)
    sorted_channels = [channels[i] for i in sorted_indices]

    return dict(zip(classes_list, average_probabilities)), sorted_channels
