from backend.parser.yt_parser import init_and_auth_youtube
import googleapiclient.errors
import pandas as pd
import sqlite3


def get_popular_russian_channel_ids(youtube, max_channels=1000):
    try:
        channel_ids = set()
        next_page_token = None

        while len(channel_ids) < max_channels:
            try:
                # Fetch popular videos in Russia
                video_response = youtube.search().list(
                    part='snippet',
                    maxResults=50,
                    type='channel',
                    regionCode='RU',
                    # q='компьютерные технологии',
                    topicId='/m/07c1v',
                    safeSearch='none',
                    relevanceLanguage='ru',
                    order='relevance',
                    pageToken=next_page_token
                ).execute()

                # Collect channel IDs
                for video in video_response.get('items', []):
                    channel_id = video['snippet']['channelId']
                    video_title = video['snippet']['title']
                    print(video_title)
                    channel_ids.add(channel_id)
                    if len(channel_ids) >= max_channels:
                        break

                next_page_token = video_response.get('nextPageToken')
                if not next_page_token:
                    break

            except googleapiclient.errors.HttpError as error:
                print(f'An HTTP error occurred: {error}')
                break

        return channel_ids

    except googleapiclient.errors.HttpError as error:
        print(f'An HTTP error occurred: {error}')
        return {}


if __name__ == "__main__":
    yt = init_and_auth_youtube("../secrets/google_project_secret.apps.googleusercontent.com.json")
    popular_channel_ids = get_popular_russian_channel_ids(yt, 30)
    print(f"Collected {len(popular_channel_ids)} channel IDs.")
    for channel_id in popular_channel_ids:
        print(channel_id)
