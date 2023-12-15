import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
import re
import sqlite3
import nltk
from nltk.corpus import stopwords
import pickle
from sklearn.multiclass import OneVsRestClassifier

nltk.download('stopwords')
russian_stopwords = stopwords.words('russian')

conn = sqlite3.connect('yt_videos_for_train_labeled.db')
videos_df = pd.read_sql('SELECT * FROM videos', conn)


# Предобработка текста
def clean_text(text):
    # Удаление HTML-тегов, специальных символов и цифр
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text


# Конкатенация названия видео и описания
videos_df['text'] = videos_df['video_title'].astype(str) + " " + videos_df['video_description'].astype(str)
videos_df['text'] = videos_df['text'].apply(clean_text)

X = videos_df['text']
y = videos_df['profession']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание конвейера с TF-IDF векторизацией и OneVsRestClassifier с логистической регрессией
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words=russian_stopwords)),
    ('clf', OneVsRestClassifier(LogisticRegression(solver='liblinear')))
])

# Предполагаем, что 'y_train' и 'y_test' теперь имеют мультилейбловый формат
pipeline.fit(X_train, y_train)

# Оценка модели
predictions = pipeline.predict(X_test)

# save the model to disk
filename = 'text_model.sav'
pickle.dump(pipeline, open(filename, 'wb'))

print(classification_report(y_test, predictions))
