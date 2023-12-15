# Предположим, что 'code' - это код авторизации, который вы получили после редиректа пользователя на redirect_uri
code = 'CODE_FROM_QUERY_PARAMETERS'

# Обмен кода авторизации на access token
token_params = {
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'code': code,
    'grant_type': 'authorization_code'
}

token_response = requests.post("https://oauth.vk.com/access_token", data=token_params)
access_token = token_response.json().get('access_token')

# Получение информации о пользователе с использованием access token
user_params = {
    'v': '5.131',
    'access_token': access_token,
    'fields': 'id,first_name,last_name'  # Укажите необходимые поля
}

user_info_response = requests.get("https://api.vk.com/method/users.get", params=user_params)
user_info = user_info_response.json()

print(user_info)
