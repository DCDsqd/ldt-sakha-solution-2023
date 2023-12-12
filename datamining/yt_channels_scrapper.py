from backend.parser.yt_parser import init_and_auth_youtube
import googleapiclient.errors
import sqlite3


# @query is set of keywords to look up that are split by commas
# @max_videos is API-usage optimal only if max_videos % 50 == 0
def get_popular_videos_with_query(youtube, query, max_videos=300):
    try:
        relevant_videos = {}  # Словарь для хранения информации о видео, ключ - video_id
        next_page_token = None

        while sum(len(videos) for videos in relevant_videos.values()) < max_videos:
            try:
                if query is not None:
                    query = query.replace(', ', '|').replace(',', '|')
                    video_response = youtube.search().list(
                        part='snippet,id',
                        maxResults=50,  # May optimize this (add var) since usually we know how much we need to fetch
                        type='video',
                        regionCode='RU',
                        q=query,
                        safeSearch='none',
                        relevanceLanguage='ru',
                        order='relevance',
                        pageToken=next_page_token
                    ).execute()
                else:
                    video_response = youtube.search().list(
                        part='snippet,id',
                        maxResults=50,  # May optimize this (add var) since usually we know how much we need to fetch
                        type='video',
                        regionCode='RU',
                        safeSearch='none',
                        relevanceLanguage='ru',
                        order='relevance',
                        pageToken=next_page_token
                    ).execute()

                for vid in video_response.get('items', []):
                    video_id = vid['id']['videoId']  # Идентификатор видео используется в качестве ключа
                    channel_id = vid['snippet']['channelId']
                    video_title = vid['snippet']['title']
                    video_description = vid['snippet']['description']

                    # Создаем новый словарь для каждого видео
                    relevant_videos[video_id] = {
                        'channel_id': channel_id,
                        'video_title': video_title,
                        'video_description': video_description
                    }

                next_page_token = video_response.get('nextPageToken')
                if not next_page_token:
                    break

            except googleapiclient.errors.HttpError as error:
                print(f'An HTTP error occurred: {error}')
                break

        return relevant_videos

    except googleapiclient.errors.HttpError as error:
        print(f'An HTTP error occurred: {error}')
        return {}


if __name__ == "__main__":
    # Подключаемся к существующей базе данных
    conn = sqlite3.connect('../data/professions.db')
    cursor = conn.cursor()

    # Запрос на получение профессий и ключевых слов
    cursor.execute("SELECT name, keywords FROM data")
    professions = cursor.fetchall()

    # Подключаемся к новой базе данных
    new_conn = sqlite3.connect('../data/yt_videos_for_train.db')
    new_cursor = new_conn.cursor()

    # Создаем таблицу для результатов, если она еще не существует
    new_cursor.execute('''CREATE TABLE IF NOT EXISTS videos (
        profession TEXT,
        video_id TEXT,
        channel_id TEXT,
        video_title TEXT,
        video_description TEXT
    )''')
    new_conn.commit()

    # Авторизация и инициализация YouTube API
    yt = init_and_auth_youtube("../secrets/google_project_secret.apps.googleusercontent.com.json")

    LIMIT = 300

    # Перебираем профессии и их ключевые слова
    for name, keywords in professions:
        # Проверяем, есть ли уже достаточно видео для этой профессии
        new_cursor.execute("SELECT COUNT(*) FROM videos WHERE profession = ?", (name,))
        count = new_cursor.fetchone()[0]
        if count >= LIMIT:
            # Если видео достаточно, пропускаем эту профессию
            continue

        if keywords:  # Проверяем, есть ли ключевые слова
            # Вычисляем, сколько видео еще нужно получить
            remaining = LIMIT - count
            # Получаем популярные видео для данной профессии
            videos_info = get_popular_videos_with_query(yt, keywords, remaining)

            # Debug things
            print(name)
            print(videos_info)

            if not videos_info:
                print(f"No videos found for {name} profession :( Probs not gonna end up well...")

            for video_id, video_info in videos_info.items():
                # Сохраняем результаты в новую базу данных
                new_cursor.execute(
                    "INSERT INTO videos (video_id, channel_id, profession, video_title, video_description) VALUES (?, "
                    "?, ?, ?, ?)",
                    (video_id,
                     video_info['channel_id'],
                     name,
                     video_info['video_title'],
                     video_info['video_description']
                     )
                )
            new_conn.commit()

    # Закрываем соединения с базами данных
    conn.close()
    new_conn.close()
