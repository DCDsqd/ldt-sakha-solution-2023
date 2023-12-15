from telethon.sync import TelegramClient
from telethon.tl.types import Channel

api_id = int(input("API ID: "))
api_hash = input("API HASH: ")
username = input("Username: ")

client = TelegramClient(username, api_id, api_hash, system_version="4.16.30-vxTEST")


async def fetch_channels_and_messages():
    await client.start()

    # Получение всех диалогов
    async for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, Channel) and not dialog.entity.megagroup:
            print(f'Канал ID: {dialog.entity.id}, Название: {dialog.entity.title}')

            # Получение последних 10 сообщений из канала
            async for message in client.iter_messages(dialog.entity, limit=10):
                print(f'Сообщение: {message.text}')


# Запуск функции
with client:
    client.loop.run_until_complete(fetch_channels_and_messages())
