from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pickle
import sys
from pathlib import Path

from parser.yt_parser import init_youtube_with_user_token, get_user_yt_subscriptions, get_user_liked_videos, \
    YTChannel, YTVideoInfo
from ml.yt_ml import analyze_youtube_user_subscriptions, analyze_youtube_list_of_vids
from parser.vk_parser import init_vk_api_session, get_self_vk_data
from ml.vk_ml import analyze_vk_groups, analyze_vk_likes


# Добавляем корневую папку проекта в sys.path
root_path = str(Path(__file__).resolve().parent.parent)  # Поднимаемся на два уровня выше от текущего файла
if root_path not in sys.path:
    sys.path.append(root_path)


app = FastAPI()
text_model = pickle.load(open('models/text_model.sav', 'rb'))
loaded_tfidf_vectorizer = pickle.load(open('models/text_model_tfidf_vectorizer.pkl', 'rb'))
multi_label_binarizer = pickle.load(open('models/text_model_mlb.pkl', 'rb'))


# Class that represents API input structure
class InputData(BaseModel):
    yt_token: str
    vk_token: str
    debug_text: str


@app.post("/predict")
def predict(input_data: InputData):
    if input_data.debug_text != "":
        predicted_probabilities = text_model.predict_proba([input_data.debug_text])[0]
        print(predicted_probabilities)
        return {
            "predictions_score": predicted_probabilities,
            "predictions_classes": predicted_probabilities,
        }

    # VK section
    if input_data.vk_token is None or input_data.vk_token == "":
        print('NO VK TOKEN PROVIDED! Should never happen!')

    vk = init_vk_api_session(input_data.vk_token)
    vk_groups, vk_wall, vk_user_likes = get_self_vk_data(vk)

    vk_groups_average_classes_score_dict = analyze_vk_groups(
        vk_user_likes,
        text_model,
        multi_label_binarizer
    )

    vk_likes_average_classes_score_dict = analyze_vk_likes(
        vk_groups,
        text_model,
        multi_label_binarizer
    )

    # YouTube section
    if input_data.yt_token is not "" and input_data.yt_token is not None:
        try:
            # Initialize YT API
            youtube_api_instance = init_youtube_with_user_token(
                input_data.yt_token,
                'secrets/google_project_secret.apps.googleusercontent.com.json'  # Path to Google App Credentials
            )

            # Get list of user subscriptions
            youtube_user_subscriptions: list[YTChannel] = get_user_yt_subscriptions(youtube_api_instance)
            youtube_user_likes: list[YTVideoInfo] = get_user_liked_videos(youtube_api_instance)

            yt_subscriptions_average_classes_score_dict, subscriptions_most_impactful_channels = \
                analyze_youtube_user_subscriptions(
                    youtube_user_subscriptions,
                    text_model,
                    multi_label_binarizer
                )
            yt_likes_average_classes_score_dict, likes_most_impactful_videos = analyze_youtube_list_of_vids(
                youtube_user_likes,
                text_model,
                multi_label_binarizer
            )

        except Exception as e:
            print(e)

        # Do not raise an exception for now (yt api quota lack might cause this, we don't want to terminate cause of it)
        # raise HTTPException(status_code=500, detail=str(e))

    return {
        "predictions_score": average_results,
        "predictions_classes": classes_list,
    }


# Чтобы запустить с помощью Unicorn: uvicorn main:app

# При запуске с помощью Uvicorn, этот блок не требуется.
# Если вы запускаете файл напрямую, он позволяет запустить сервер.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
