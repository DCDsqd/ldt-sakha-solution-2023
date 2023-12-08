import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Disable OAuthlib's HTTPS verification when running locally.
# DO NOT leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "../../secrets/client_secrets.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.readonly"])
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

request = youtube.subscriptions().list(
    part="snippet",
    mine=True
)
response = request.execute()

# Print the names and IDs of the user's subscriptions
for item in response.get('items', []):
    title = item['snippet']['title']
    channel_id = item['snippet']['resourceId']['channelId']
    print(f"Title: {title}, Channel ID: {channel_id}")