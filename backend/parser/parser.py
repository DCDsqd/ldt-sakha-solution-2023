import vk_api

# To use VK API, you first need to register your application on VK and get an access token.
# Replace 'YOUR_ACCESS_TOKEN' with the access token you received from VK.

vk_session = vk_api.VkApi(token='YOUR_ACCESS_TOKEN')

try:
    vk = vk_session.get_api()

    # Replace 'user_id' with the ID of the user whose groups you want to fetch.
    user_id = 'user_id'

    # Fetch the user's groups
    groups = vk.groups.get(user_id=user_id, extended=1)
    print(groups)

except Exception as e:
    print(f"An error occurred: {e}")
