import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json

from backend.parser.common import remove_urls


from backend.parser.yt_parser import init_and_auth_youtube
import googleapiclient.errors
import sqlite3


def get_popular_videos_with_query(youtube, query: str, next_page_token=None):
    relevant_videos = {}  # Dictionary for storing video information, key - video_id
    query_list = query.split(', ')[:7]
    query_string = '|'.join(query_list)

    # Debug
    print("Query:", query_string)

    max_results = 50

    while True:
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

    return relevant_videos


if __name__ == "__main__":
    conn = sqlite3.connect('../data/professions.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, keywords_extention FROM data")
    professions = cursor.fetchall()

    new_conn = sqlite3.connect('yt_videos_for_train_labeled.db')
    new_cursor = new_conn.cursor()

    new_cursor.execute('''CREATE TABLE IF NOT EXISTS videos (
        profession TEXT,
        video_id TEXT,
        channel_id TEXT,
        video_title TEXT,
        video_description TEXT
    )''')
    new_conn.commit()

    yt = init_and_auth_youtube("../secrets/11google_project_secret.apps.googleusercontent.com.json")

    for name, keywords in professions:
        if name != "Фельдшер":
            continue

        if not keywords:
            print("No keywords, terminating")
            exit(0)

        videos_info = get_popular_videos_with_query(yt, keywords)

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
