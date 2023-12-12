from backend.parser.yt_parser import init_and_auth_youtube
import googleapiclient.errors
import sqlite3


# @query is set of keywords to look up that are split by commas
# @max_videos is API-usage optimal only if max_videos % 50 == 0
def get_popular_videos_with_query(youtube, query, max_videos=300):
    try:
        relevant_videos = {}
        next_page_token = None

        while sum(len(videos) for videos in relevant_videos.values()) < max_videos:
            try:
                video_response = youtube.search().list(
                    part='snippet,id',
                    maxResults=50,  # May optimize this value (add var) since usually we know how much we need to fetch
                    type='video',
                    regionCode='RU',
                    q=query,
                    safeSearch='none',
                    relevanceLanguage='ru',
                    order='relevance',
                    pageToken=next_page_token
                ).execute()

                for video in video_response.get('items', []):
                    channel_id = video['snippet']['channelId']
                    video_title = video['snippet']['title']
                    video_description = video['snippet']['description']
                    video_id = video['id']['videoId']

                    if channel_id not in relevant_videos:
                        relevant_videos[channel_id] = []

                    relevant_videos[channel_id].append({
                        'video_title': video_title,
                        'video_description': video_description,
                        'video_id': video_id
                    })

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
    conn = sqlite3.connect('existing_database.db')
    cursor = conn.cursor()

    # Запрос на получение профессий и ключевых слов
    cursor.execute("SELECT name, keywords FROM professions_table")
    professions = cursor.fetchall()

    # Подключаемся к новой базе данных
    new_conn = sqlite3.connect('new_database.db')
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
            for video in videos_info:
                # Сохраняем результаты в новую базу данных
                new_cursor.execute(
                    "INSERT INTO videos (profession, video_id, channel_id, video_title, video_description) VALUES (?, "
                    "?, ?, ?, ?)",
                    (name, video['video_id'], video['channel_id'], video['video_title'], video['video_description']))
                if remaining <= 0:
                    break
                remaining -= 1
            new_conn.commit()

    # Закрываем соединения с базами данных
    conn.close()
    new_conn.close()
