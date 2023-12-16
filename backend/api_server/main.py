from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

from parser.yt_parser import init_youtube_with_user_token, get_user_yt_subscriptions, get_user_liked_videos, \
    YTChannel, YTVideoInfo
from parser.common import clean_text_for_model


app = FastAPI()
text_model = pickle.load(open('models/text_model.sav', 'rb'))
loaded_tfidf_vectorizer = pickle.load(open('models/text_model_tfidf_vectorizer.pkl', 'rb'))
multi_label_binarizer = pickle.load(open('models/text_model_mlb.pkl', 'rb'))


# Class that represents API input structure
class InputData(BaseModel):
    yt_token: str
    vk_token: str
    tg_token: str
    tg_login: str
    tg_psw: str


@app.post("/predict")
def predict(input_data: InputData):
    try:
        # YouTube section

        # Initialize YT API
        youtube_api_instance = init_youtube_with_user_token(
            input_data.yt_token,
            'secrets/google_project_secret.apps.googleusercontent.com.json'  # Path to Google App Credentials
        )

        # Get list of user subscriptions
        youtube_user_subscriptions: list[YTChannel] = get_user_yt_subscriptions(youtube_api_instance)
        youtube_user_likes: list[YTVideoInfo] = get_user_liked_videos(youtube_api_instance)

        for youtube_user_subbed_channel in youtube_user_subscriptions:
            channel_videos = youtube_user_subbed_channel.gather_videos(youtube_user_likes)
            united_text = " ".join([video.concatenate_text() for video in channel_videos])
            united_text = clean_text_for_model(united_text)

            text_model.predict()

            # Получение предсказаний вероятности
            predicted_probabilities = text_model.predict_proba(transformed_text)

            # Преобразование вероятностей в список для JSON сериализации
            probabilities_list = predicted_probabilities.tolist()

            # Получение названий классов
            classes_list = mlb.classes_.tolist()

        return {
            "predictions_score": probabilities_list,
            "predictions_classes": classes_list,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Unicorn: uvicorn main:app

# При запуске с помощью Uvicorn, этот блок не требуется.
# Если вы запускаете файл напрямую, он позволяет запустить сервер.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
