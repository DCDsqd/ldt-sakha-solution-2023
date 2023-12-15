import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

nltk.download('stopwords', quiet=True)

# Списки стоп-слов для русского и английского языков
russian_stopwords = set(stopwords.words('russian'))
english_stopwords = set(stopwords.words('english'))


def clean_text_for_model(text: str) -> str:
    text = remove_stop_words(text)
    text = remove_urls(text)
    text = clean_text_from_unnecessary_symbols(text)
    return text


def clean_text_from_unnecessary_symbols(text: str) -> str:
    """
    Функция для очистки текста от ненужных символов и избыточных пробелов.

    :param text: Исходный текст для обработки.
    :return: Очищенный текст.
    """
    # Удаление специальных символов и цифр
    text = re.sub(r'[^а-яА-Яa-zA-Z\s]', '', text)

    # Замена одного или нескольких пробелов, табов, переводов строки на один пробел
    text = re.sub(r'\s+', ' ', text)

    # Удаление ведущих и завершающих пробелов
    text = text.strip()

    return text


def remove_urls(text: str) -> str:
    """
    Removes all URLs from the given text.

    Args:
    text (str): The input string from which URLs need to be removed.

    Returns:
    str: The text with all URLs removed.
    """
    # Regex pattern for matching URLs
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, '', text)


def remove_stop_words(text: str) -> str:
    # Токенизируем текст
    words = word_tokenize(text)

    # Удаление стоп-слов из токенизированного текста
    filtered_words = [word for word in words if
                      word.lower() not in russian_stopwords and word.lower() not in english_stopwords]

    # Возвращаем отфильтрованный текст
    return ' '.join(filtered_words)


