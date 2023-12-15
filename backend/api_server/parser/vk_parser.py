import vk_api


def get_vk_data(vk_user_id, access_token):
    vk_session = vk_api.VkApi(token=access_token)
    vk = vk_session.get_api()

    # Получение групп пользователя
    groups = vk.groups.get(user_id=vk_user_id, extended=1)

    # Получение записей со стены пользователя
    wall = vk.wall.get(owner_id=vk_user_id, count=100)

    # Получение лайков для последних постов (например, 100)
    likes = []
    for item in wall['items']:
        post_likes = vk.likes.getList(type='post', owner_id=vk_user_id, item_id=item['id'], count=100)
        likes.append(post_likes)

    return groups, wall, likes


def get_group_data(group_id, access_token):
    vk_session = vk_api.VkApi(token=access_token)
    vk = vk_session.get_api()

    # Получение информации о группе
    group_info = vk.groups.getById(group_id=group_id, fields='members_count,description')

    # Получение записей из группы
    group_posts = vk.wall.get(owner_id=-int(group_id), count=100)  # Префикс "-" используется для обозначения группы

    return group_info, group_posts


def format_vk_output(group_info, group_posts):
    output = ""

    # Проверка и форматирование информации о группе
    if 'response' in group_info:
        for group in group_info['response']:
            output += f"Название группы: {group['name']}\n"
            output += f"Описание: {group['description']}\n"
            output += f"Количество участников: {group['members_count']}\n"
            output += f"Ссылка: https://vk.com/{group['screen_name']}\n"
            output += f"Фото группы: {group['photo_200']}\n\n"

    # Проверка и форматирование записей группы
    if 'items' in group_posts:
        for post in group_posts['items']:
            output += f"Дата публикации: {post['date']}\n"
            output += f"Текст поста: {post.get('text', 'Без текста')}\n"
            output += f"Лайков: {post['likes']['count']}, Репостов: {post['reposts']['count']}\n"
            if 'views' in post:
                output += f"Просмотров: {post['views']['count']}\n"
            output += "\n"

    return output


# group_info, group_posts = get_group_data('113716445')
# print(format_vk_output(group_info, group_posts))
