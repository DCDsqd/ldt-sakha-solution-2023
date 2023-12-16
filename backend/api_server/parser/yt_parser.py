import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials
import json


def init_youtube_with_user_token(token, client_secrets_file_path, refresh_token=None):
    api_service_name = "youtube"
    api_version = "v3"

    # Чтение client_id и client_secret из файла с секретами клиента
    with open(client_secrets_file_path, 'r') as file:
        secrets_data = json.load(file)
        client_id = secrets_data['installed']['client_id']
        client_secret = secrets_data['installed']['client_secret']

    credentials = Credentials(
        token=token,
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret
    )

    try:
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials
        )
    except Exception as e:
        print(f"Error during YouTube client initialization: {e}")
        return None

    return youtube


def init_and_auth_youtube_local_server(client_secrets_file_path):
    # Disable/Enable OAuthlib's HTTPS verification when running locally.
    # DO NOT leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"

    try:
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file_path,
            scopes=["https://www.googleapis.com/auth/youtube.readonly"]
        )
        credentials = flow.run_local_server(port=8090)
        youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
    except Exception as e:
        print(f"During YT initialization error occurred: {e}")
        return None

    return youtube


def get_yt_category_map(youtube_api, region_code="RU"):
    # Fetch the list of categories and create a map of IDs to names
    request = youtube_api.videoCategories().list(
        part="snippet",
        regionCode=region_code
    )
    response = request.execute()
    category_map = {item['id']: item['snippet']['title'] for item in response.get('items', [])}
    return category_map


# A class to represent a YouTube video
class YTVideoInfo:
    def __init__(self, title, desc, category, yt_video_id=None):
        self.title = title
        self.desc = desc
        self.category = category
        self.yt_video_id = yt_video_id

        self.desc = self.desc

    def __str__(self):
        """
        Returns a string representation of the YouTube channel,
        including its ID, title, and description.
        """
        return f"Video title: {self.title}\nDescription: {self.desc}\nCategory: {self.category}"

    def concatenate_text(self, include_category: bool = False) -> str:
        return " ".join([self.title, self.desc]) if include_category else \
               " ".join([self.title, self.desc, self.category])


# A class to represent a YouTube channel with all the needed data for further processing
class YTChannel:
    def __init__(self, yt_channel_id, yt_title, yt_description):
        self.yt_id = yt_channel_id
        self.title = yt_title
        self.desc = yt_description

    def __str__(self):
        """
        Returns a string representation of the YouTube channel,
        including its ID, title, and description.
        """
        return f"Channel ID: {self.yt_id}\nTitle: {self.title}\nDescription: {self.desc}"

    def gather_videos(self, youtube_api, max_results=10) -> list[YTVideoInfo]:
        # print(f"Analyzing videos for channel ID: {self.yt_id}")

        category_map = get_yt_category_map(youtube_api)

        # First, get the channel's upload playlist ID
        channel_request = youtube_api.channels().list(
            part="contentDetails",
            id=self.yt_id  # Use forUsername=username if you have the username instead of the channel ID
        )
        channel_response = channel_request.execute()

        upload_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Fetch the videos from the upload playlist
        playlist_request = youtube_api.playlistItems().list(
            part="contentDetails",
            playlistId=upload_playlist_id,
            maxResults=max_results
        )
        playlist_response = playlist_request.execute()

        video_ids = [item['contentDetails']['videoId'] for item in playlist_response.get('items', [])]

        # Batch request for video details
        video_request = youtube_api.videos().list(
            part="snippet",
            id=','.join(video_ids)  # Join video IDs with commas for batch request
        )
        video_response = video_request.execute()

        # Process each video
        video_data = []
        for video in video_response.get('items', []):
            title = video['snippet']['title']
            description = video['snippet']['description']
            category_id = video['snippet']['categoryId']
            category = category_map.get(category_id, "Unknown")

            video_data.append(YTVideoInfo(title, description, category))

        return video_data


def get_user_liked_videos(youtube, max_results=100) -> list[YTVideoInfo]:
    # Получаем ID плейлиста с лайкнутыми видео
    channels_response = youtube.channels().list(
        part="contentDetails",
        mine=True
    ).execute()

    liked_videos_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['likes']

    # Получаем видео из плейлиста лайкнутых видео
    playlist_request = youtube.playlistItems().list(
        part="snippet",
        playlistId=liked_videos_playlist_id,
        maxResults=min(max_results, 50)  # YouTube API ограничивает maxResults значением 50
    )

    liked_videos = []
    while playlist_request and len(liked_videos) < max_results:
        playlist_response = playlist_request.execute()
        for item in playlist_response['items']:
            if len(liked_videos) >= max_results:
                break  # Прекращаем добавление видео, если достигнут предел max_results

            video_title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            video_description = item['snippet']['description']

            # "Default" заглушка для категории, т. к. пока нет планов использовать категорию
            liked_videos.append(YTVideoInfo(video_title, video_description, "Default", video_id))

        # Переходим к следующей странице результатов, если она есть и не превышен лимит
        if 'nextPageToken' in playlist_response and len(liked_videos) < max_results:
            playlist_request = youtube.playlistItems().list_next(
                playlist_request, playlist_response
            )
        else:
            break

    return liked_videos


def get_user_yt_subscriptions(youtube, limit=100) -> list[YTChannel]:
    def get_subscriptions(page_token=None):
        return youtube.subscriptions().list(
            part="snippet",
            mine=True,
            maxResults=50,  # Максимальное количество результатов на страницу (максимум 50)
            order="relevance",
            pageToken=page_token
        ).execute()

    # Получение первой страницы подписок
    subscriptions = get_subscriptions()
    all_subscriptions = subscriptions.get('items', [])

    # Пагинация: получение остальных страниц
    while 'nextPageToken' in subscriptions:
        subscriptions = get_subscriptions(subscriptions['nextPageToken'])
        all_subscriptions.extend(subscriptions.get('items', []))

    # file_path = 'latest_youtube_subscriptions_answer.json'
    # with open(file_path, 'w', encoding='utf-8') as file:
    #     json.dump(all_subscriptions, file, ensure_ascii=False, indent=4)

    sub_list = []

    for item in all_subscriptions:
        title = item['snippet']['title']
        channel_id = item['snippet']['resourceId']['channelId']
        desc = item['snippet']['description']
        sub_list.append(YTChannel(channel_id, title, desc))

    return sub_list

# Just a minimal usage example for testing purposes

# if __name__ == "__main__":
# yt = init_and_auth_youtube("../secrets/google_project_secret.apps.googleusercontent.com.json")
# res = get_user_yt_subscriptions(yt)
# print(res)

# print(res[2].gather_videos(yt)[0])
