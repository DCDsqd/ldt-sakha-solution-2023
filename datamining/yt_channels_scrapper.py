from backend.parser.yt_parser import init_and_auth_youtube
import googleapiclient.errors
import sqlite3


def get_popular_videos_with_query(youtube, query, max_videos=300, divide_query=False):
    relevant_videos = {}  # Dictionary for storing video information, key - video_id

    if divide_query:
        query_phrases = query.split(',')
        query_groups = [query_phrases[i:i + 3] for i in range(0, len(query_phrases), 3)]

        for query_group in query_groups:
            next_page_token = None
            query_string = '|'.join([phrase.strip() for phrase in query_group])

            while sum(len(videos) for videos in relevant_videos.values()) < max_videos:
                try:
                    print(query_string)
                    max_results = min(50, max_videos - sum(len(videos) for videos in relevant_videos.values()))
                    video_response = youtube.search().list(
                        part='snippet,id',
                        maxResults=max_results,
                        type='video',
                        q=query_string,
                        safeSearch='none',
                        order='relevance',
                        pageToken=next_page_token
                    ).execute()

                    for vid in video_response.get('items', []):
                        vid_id = vid['id']['videoId']
                        if vid_id not in relevant_videos:
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
                break

    else:
        next_page_token = None
        query_string = query.replace(', ', '|').replace(',', '|')

        while sum(len(videos) for videos in relevant_videos.values()) < max_videos:
            try:
                print(query_string)
                max_results = min(50, max_videos - sum(len(videos) for videos in relevant_videos.values()))
                video_response = youtube.search().list(
                    part='snippet,id',
                    maxResults=max_results,
                    type='video',
                    q=query_string,
                    safeSearch='none',
                    order='relevance',
                    pageToken=next_page_token
                ).execute()

                for vid in video_response.get('items', []):
                    vid_id = vid['id']['videoId']
                    if vid_id not in relevant_videos:
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

    yt = init_and_auth_youtube("../secrets/google_project_secret.apps.googleusercontent.com.json")

    LIMIT = 300

    for name, keywords in professions:
        new_cursor.execute("SELECT COUNT(*) FROM videos WHERE profession = ?", (name,))
        count = new_cursor.fetchone()[0]
        remaining = LIMIT - count
        if remaining <= 0:
            continue

        if keywords:
            videos_info = get_popular_videos_with_query(yt, keywords, remaining)

            print(f"Query for '{name}': {keywords.replace(', ', '|')}")
            print(f"Profession: {name}")
            print(f"Videos found: {len(videos_info)}")

            if not videos_info:
                print(f"No videos found for {name} profession. :( Maybe try different keywords?")

            for video_id, video_info in videos_info.items():
                if not new_cursor.execute("SELECT 1 FROM videos WHERE video_id = ?", (video_id,)).fetchone():
                    new_cursor.execute(
                        "INSERT INTO videos (profession, video_id, channel_id, video_title, video_description) VALUES "
                        "(?, ?, ?, ?, ?)",
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
