import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

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


def get_subscriptions(youtube, page_token=None):
    return youtube.subscriptions().list(
        part="snippet",
        mine=True,
        maxResults=50,  # Максимальное количество результатов на страницу (максимум 50)
        pageToken=page_token
    ).execute()


try:
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    # Получение первой страницы подписок
    subscriptions = get_subscriptions(youtube)
    all_subscriptions = subscriptions.get('items', [])

    # Пагинация: получение остальных страниц
    while 'nextPageToken' in subscriptions:
        subscriptions = get_subscriptions(youtube, subscriptions['nextPageToken'])
        all_subscriptions.extend(subscriptions.get('items', []))

    # Вывод названий и ID каналов
    for item in all_subscriptions:
        title = item['snippet']['title']
        channel_id = item['snippet']['resourceId']['channelId']
        print(f"Title: {title}, Channel ID: {channel_id}")

except Exception as e:
    print(f"An error occurred: {e}")
