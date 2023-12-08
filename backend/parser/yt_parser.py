import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import json


# A class to represent a YouTube channel with all the needed data for further processing
class YTChannel:
    def __init__(self, yt_channel_id, yt_title, yt_description):
        self.yt_id = yt_channel_id
        self.title = yt_title
        self.desc = yt_description


def get_user_yt_subscriptions() -> list[YTChannel]:
    # Disable OAuthlib's HTTPS verification when running locally.
    # DO NOT leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "../../secrets/google_project_secret.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.readonly"])
    credentials = flow.run_local_server(port=8090)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    request = youtube.subscriptions().list(
        part="snippet",
        mine=True
    )
    response = request.execute()

    try:
        youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

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

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    file_path = 'latest_youtube_subscriptions_answer.json'
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(all_subscriptions, file, ensure_ascii=False, indent=4)

    sub_list = []

    for item in all_subscriptions:
        title = item['snippet']['title']
        channel_id = item['snippet']['resourceId']['channelId']
        desc = item['snippet']['description']
        sub_list.append(YTChannel(title, channel_id, desc))

    return sub_list


res = get_user_yt_subscriptions()

print(res)
