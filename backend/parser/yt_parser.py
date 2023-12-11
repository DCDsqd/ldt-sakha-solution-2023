import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json


def init_and_auth_youtube():
    # Disable/Enable OAuthlib's HTTPS verification when running locally.
    # DO NOT leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "../../secrets/google_project_secret.apps.googleusercontent.com.json"

    try:
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file,
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


# A class to represent a YouTube channel with all the needed data for further processing
class YTChannel:
    def __init__(self, yt_channel_id, yt_title, yt_description):
        self.yt_id = yt_channel_id
        self.title = yt_title
        self.desc = yt_description

    def analyze_videos(self, youtube_api):
        print(f"Analyzing videos for channel ID: {self.yt_id}")

        category_map = get_yt_category_map(youtube_api)

        # First, get the channel's upload playlist ID
        channel_request = youtube_api.channels().list(
            part="contentDetails",
            id=self.yt_id  # Use forUsername=username if you have the username instead of the channel ID
        )
        channel_response = channel_request.execute()

        upload_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # Fetch the videos from the upload playlist
        video_data = []
        playlist_request = youtube_api.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=upload_playlist_id,
            maxResults=20  # Adjust as needed
        )
        playlist_response = playlist_request.execute()

        for item in playlist_response.get('items', []):
            video_id = item['contentDetails']['videoId']

            # Fetch additional video details for each video ID
            video_request = youtube_api.videos().list(
                part="snippet",
                id=video_id
            )
            video_response = video_request.execute()

            for video in video_response.get('items', []):
                title = video['snippet']['title']
                description = video['snippet']['description']
                category_id = video['snippet']['categoryId']
                category = category_map.get(category_id, "Unknown")

                video_data.append({'title': title, 'description': description, 'category': category})

        return video_data


def get_user_yt_subscriptions(youtube) -> list[YTChannel]:
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

    file_path = 'latest_youtube_subscriptions_answer.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(all_subscriptions, file, ensure_ascii=False, indent=4)

    sub_list = []

    for item in all_subscriptions:
        title = item['snippet']['title']
        channel_id = item['snippet']['resourceId']['channelId']
        desc = item['snippet']['description']
        sub_list.append(YTChannel(channel_id, title, desc))

    return sub_list


yt = init_and_auth_youtube()
res = get_user_yt_subscriptions(yt)
# print(res)

print(res[0].analyze_videos(yt))
