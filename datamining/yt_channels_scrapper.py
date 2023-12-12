from backend.parser.yt_parser import init_and_auth_youtube
import googleapiclient.errors
import sqlite3


def get_popular_videos_with_query(youtube, query, max_videos=300):
    relevant_videos = {}  # Словарь для хранения информации о видео, ключ - video_id

    # Разделение запроса на фразы и группировка по 3 фразы
    # Почему-то YT API плохо обрабатывает ключевые слова, если их более 3 в запросе...
    # См. https://github.com/youtube/api-samples/issues/248
    query_phrases = query.split(',')
    query_groups = [query_phrases[i:i + 3] for i in range(0, len(query_phrases), 3)]

    for query_group in query_groups:
        next_page_token = None
        query_string = '%7C'.join([phrase.strip() for phrase in query_group])  # Создание строки запроса для группы

        while sum(len(videos) for videos in relevant_videos.values()) < max_videos:
            try:
                print(query_string)
                video_response = youtube.search().list(
                    part='snippet,id',
                    maxResults=50,
                    type='video',
                    q=query_string,
                    safeSearch='none',
                    relevanceLanguage='ru',
                    order='relevance',
                    pageToken=next_page_token
                ).execute()

                for vid in video_response.get('items', []):
                    vid_id = vid['id']['videoId']
                    channel_id = vid['snippet']['channelId']
                    video_title = vid['snippet']['title']
                    video_description = vid['snippet']['description']

                    relevant_videos[vid_id] = {
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

        if sum(len(videos) for videos in relevant_videos.values()) >= max_videos:
            break  # Выход из цикла, если достигнут лимит

    return relevant_videos


if __name__ == "__main__":
    conn = sqlite3.connect('../data/professions.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, keywords FROM data")
    professions = cursor.fetchall()

    new_conn = sqlite3.connect('../data/yt_videos_for_train.db')
    new_cursor = new_conn.cursor()

    new_cursor.execute('''CREATE TABLE IF NOT EXISTS videos (
        profession TEXT,
        video_id TEXT,
        channel_id TEXT,
        video_title TEXT,
        video_description TEXT
    )''')
    new_conn.commit()

    yt = init_and_auth_youtube("../secrets/2google_project_secret.apps.googleusercontent.com.json")

    LIMIT = 300

    for name, keywords in professions:
        new_cursor.execute("SELECT COUNT(*) FROM videos WHERE profession = ?", (name,))
        count = new_cursor.fetchone()[0]
        if count >= LIMIT:
            continue

        if keywords:
            remaining = LIMIT - count
            videos_info = get_popular_videos_with_query(yt, keywords, remaining)

            print(keywords.replace(', ', '|'))
            print(name)
            print(videos_info)

            if not videos_info:
                print(f"No videos found for {name} profession :( Probs not gonna end up well...")

            for video_id, video_info in videos_info.items():
                new_cursor.execute(
                    "INSERT INTO videos (profession, video_id, channel_id, video_title, video_description) VALUES (?, "
                    "?, ?, ?, ?)",
                    (name,
                     video_id,
                     video_info['channel_id'],
                     video_info['video_title'],
                     video_info['video_description']
                     )
                )
            new_conn.commit()

    conn.close()
    new_conn.close()
