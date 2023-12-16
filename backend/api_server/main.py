from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pickle

from parser.yt_parser import init_youtube_with_user_token, get_user_yt_subscriptions, get_user_liked_videos, \
    YTChannel, YTVideoInfo
from ml.yt_ml import analyze_youtube_user_subscriptions, analyze_youtube_list_of_vids

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
    # VK section

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

            subscriptions_average_classes_score_dict, subscriptions_most_impactful_channels = \
                analyze_youtube_user_subscriptions(
                    youtube_user_subscriptions,
                    text_model,
                    multi_label_binarizer
                )
            likes_average_classes_score_dict, likes_most_impactful_videos = analyze_youtube_list_of_vids(
                youtube_user_likes,
                text_model,
                multi_label_binarizer
            )

        except Exception as e:
            print(e)

        # Do not raise an exception for now
        # raise HTTPException(status_code=500, detail=str(e))

    return {
        "predictions_score": average_results,
        "predictions_classes": classes_list,
    }


# Unicorn: uvicorn main:app

# При запуске с помощью Uvicorn, этот блок не требуется.
# Если вы запускаете файл напрямую, он позволяет запустить сервер.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
