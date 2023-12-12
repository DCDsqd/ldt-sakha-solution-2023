import sqlite3


# Путь к файлу базы данных
db_path = '../yt_videos_for_train.db'

# Подключаемся к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создаем новую таблицу без дубликатов
cursor.execute('''
CREATE TABLE IF NOT EXISTS videos_deduplicated AS
SELECT DISTINCT profession, video_id, channel_id, video_title, video_description
FROM videos;
''')

# Сохраняем изменения
conn.commit()

# Закрываем соединение с базой данных
conn.close()
