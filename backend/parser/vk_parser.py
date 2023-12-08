import json
import vk_api

# Path to the JSON file containing the VK access token
config_file_path = 'config.json'

try:
    # Read the token from the JSON file
    with open(config_file_path, 'r') as file:
        config = json.load(file)
        token = config.get('vk_token')

    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    # Replace 'user_id' with the ID of the user whose groups you want to fetch.
    user_id = 'user_id'

    # Fetch the user's groups
    groups = vk.groups.get(user_id=user_id, extended=1)
    print(groups)

except Exception as e:
    print(f"An error occurred: {e}")
