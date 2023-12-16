import vk_api


def init_vk_api_session(access_token):
    try:
        vk_session = vk_api.VkApi(token=access_token)
        vk = vk_session.get_api()
        return vk
    except vk_api.AuthError as error_msg:
        print(f"Ошибка аутентификации: {error_msg}")
        return None


class VKGroup:
    def __init__(self, vk_id, name, desc, members_count, posts):
        self.vk_id = vk_id
        self.name = name
        self.desc = desc
        self.members_count = members_count
        self.posts = posts  # Список последних 50 постов (только текст)


class VKWallPost:
    def __init__(self, post_id, owner_id, text):
        self.post_id = post_id
        self.owner_id = owner_id
        self.text = text  # Текст поста


class VKLike:
    def __init__(self, item_id, owner_id, text):
        self.item_id = item_id  # ID поста, которому пользователь поставил лайк
        self.owner_id = owner_id  # ID владельца поста
        self.text = text  # Текст поста


def get_group_data(vk, group_id):
    # Получение информации о группе
    group_info = vk.groups.getById(group_id=group_id, fields='members_count,description')[0]

    # Получение последних 50 постов из группы
    group_posts_data = vk.wall.get(owner_id=-int(group_id), count=50)  # Префикс "-" используется для обозначения группы
    group_posts_texts = [post['text'] for post in group_posts_data['items']]  # Сохраняем только текст каждого поста

    # Создание объекта VKGroup с информацией о группе и последних постах
    group = VKGroup(
        vk_id=group_info['id'],
        name=group_info['name'],
        desc=group_info.get('description', ''),
        members_count=group_info.get('members_count', 0),
        posts=group_posts_texts
    )
    return group


def get_self_vk_data(vk, wall_limit=50, likes_limit=100):
    # Получение групп пользователя
    groups_data = vk.groups.get(extended=1)
    vk_groups = []
    for group_data in groups_data['items']:
        vk_group = get_group_data(vk, group_data['id'])
        vk_groups.append(vk_group)

    # Получение и фильтрация записей со стены пользователя
    filtered_wall_posts = []
    wall_offset = 0
    while len(filtered_wall_posts) < wall_limit:
        wall_data = vk.wall.get(count=100, offset=wall_offset)
        if not wall_data['items']:
            break
        for item in wall_data['items']:
            if len(item['text']) >= 35:
                post = VKWallPost(post_id=item['id'], owner_id=item['owner_id'], text=item['text'])
                filtered_wall_posts.append(post)
            if len(filtered_wall_posts) >= wall_limit:
                break
        wall_offset += 100

    # Получение информации о лайках, сделанных пользователем
    user_likes = []
    likes_offset = 0
    while len(user_likes) < likes_limit:
        likes_data = vk.wall.get(count=100, offset=likes_offset)
        if not likes_data['items']:
            break
        for item in likes_data['items']:
            if len(item['text']) >= 35:
                like_obj = VKLike(item_id=item['id'], owner_id=item['owner_id'], text=item['text'])
                user_likes.append(like_obj)
            if len(user_likes) >= likes_limit:
                break
        likes_offset += 100

    return vk_groups, filtered_wall_posts, user_likes


def get_vk_data(vk, vk_user_id):
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


# Debug function
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
