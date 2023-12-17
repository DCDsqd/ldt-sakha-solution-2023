from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pickle

from parser.yt_parser import init_youtube_with_user_token, get_user_yt_subscriptions, get_user_liked_videos, \
    YTChannel, YTVideoInfo
from ml.yt_ml import analyze_youtube_user_subscriptions, analyze_youtube_list_of_vids
from parser.vk_parser import init_vk_api_session, get_self_vk_data
from ml.vk_ml import analyze_vk_groups, analyze_vk_likes
from tools.tools import merge_and_average_dicts, split_dict_into_labels_and_values, merge_and_average_multiple_dicts

app = FastAPI()
with open('models/text_model.sav', 'rb') as file:
    text_model = pickle.load(file)
with open('models/text_model_mlb.pkl', 'rb') as file:
    multi_label_binarizer = pickle.load(file)


# Class that represents API input structure
class InputData(BaseModel):
    yt_token: str
    vk_token: str
    debug_text: str


@app.post("/predict")
def predict(input_data: InputData):
    if input_data.debug_text != "":
        predicted_probabilities = text_model.predict_proba([input_data.debug_text])[0]

        # Фильтруем классы и их вероятности по заданному порогу
        threshold = 0.01
        filtered_predictions = [(label, prob) for label, prob
                                in zip(multi_label_binarizer.classes_, predicted_probabilities)
                                if prob >= threshold]

        # Разделяем классы и их вероятности
        predictions_classes = [label for label, _ in filtered_predictions]
        predictions_score = [prob for _, prob in filtered_predictions]

        return {
            "top_professions": predictions_classes,
            "top_probabilities": predictions_score,
            "yt_impactful_likes": [],
            "yt_impactful_channels": [],
            "vk_impactful_likes": [],
            "vk_impactful_groups": []
        }

    # VK section
    vk_sum_dict = None
    vk_most_impactful_liked_posts = None
    vk_most_impactful_groups = None
    if input_data.vk_token != "" and input_data.vk_token is not None:
        vk = init_vk_api_session(input_data.vk_token)
        vk_groups, vk_wall, vk_user_likes = get_self_vk_data(vk)

        vk_groups_average_classes_score_dict, vk_most_impactful_groups = analyze_vk_groups(
            vk_user_likes,
            text_model,
            multi_label_binarizer
        )

        if len(vk_most_impactful_groups) > 5:
            vk_most_impactful_groups = vk_most_impactful_groups[:5]

        vk_likes_average_classes_score_dict, vk_most_impactful_liked_posts = analyze_vk_likes(
            vk_groups,
            text_model,
            multi_label_binarizer
        )

        if len(vk_most_impactful_liked_posts) > 5:
            vk_most_impactful_liked_posts = vk_most_impactful_liked_posts[:5]

        vk_sum_dict = merge_and_average_dicts(vk_likes_average_classes_score_dict,
                                              vk_groups_average_classes_score_dict,
                                              weight1=1,
                                              weight2=3)

    # YouTube section
    yt_sum_dict = None
    yt_likes_most_impactful_videos = None
    yt_subscriptions_most_impactful_channels = None
    if input_data.yt_token != "" and input_data.yt_token is not None:
        try:
            # Initialize YT API
            youtube_api_instance = init_youtube_with_user_token(
                input_data.yt_token,
                'secrets/google_project_secret.apps.googleusercontent.com.json'  # Path to Google App Credentials
            )

            # Get list of user subscriptions
            youtube_user_subscriptions: list[YTChannel] = get_user_yt_subscriptions(youtube_api_instance)
            youtube_user_likes: list[YTVideoInfo] = get_user_liked_videos(youtube_api_instance)

            yt_subscriptions_average_classes_score_dict, yt_subscriptions_most_impactful_channels = \
                analyze_youtube_user_subscriptions(
                    youtube_user_subscriptions,
                    text_model,
                    multi_label_binarizer
                )

            if len(yt_subscriptions_most_impactful_channels) > 5:
                yt_subscriptions_most_impactful_channels = yt_subscriptions_most_impactful_channels[:5]

            yt_likes_average_classes_score_dict, yt_likes_most_impactful_videos = analyze_youtube_list_of_vids(
                youtube_user_likes,
                text_model,
                multi_label_binarizer
            )

            if len(yt_likes_most_impactful_videos) > 5:
                yt_likes_most_impactful_videos = yt_likes_most_impactful_videos[:5]

            yt_sum_dict = merge_and_average_dicts(yt_subscriptions_average_classes_score_dict,
                                                  yt_likes_average_classes_score_dict,
                                                  weight1=2,
                                                  weight2=1)

        except Exception as e:
            print(e)

        # Do not raise an exception for now (yt api quota lack might cause this, we don't want to terminate cause of it)
        # raise HTTPException(status_code=500, detail=str(e))

    dicts_list = [vk_sum_dict, yt_sum_dict]
    dicts_list = [dict_ for dict_ in dicts_list if dict_ is not None]

    final_dict = merge_and_average_multiple_dicts(dicts_list, [1] * len(dicts_list))

    yt_likes_most_impactful_videos_json = None
    yt_subscriptions_most_impactful_channels_json = None
    if yt_sum_dict:
        yt_likes_most_impactful_videos_json = [video.to_json() for video
                                               in yt_likes_most_impactful_videos]
        yt_subscriptions_most_impactful_channels_json = [video.to_json() for video
                                                         in yt_subscriptions_most_impactful_channels]

    vk_most_impactful_liked_posts_json = None
    vk_most_impactful_groups_json = None
    if vk_sum_dict:
        vk_most_impactful_liked_posts_json = [video.to_json() for video
                                              in vk_most_impactful_liked_posts]
        vk_most_impactful_groups_json = [video.to_json() for video
                                         in vk_most_impactful_groups]

    top_profs, top_probs = split_dict_into_labels_and_values(final_dict)

    return {
        "top_professions": top_profs,
        "top_probabilities": top_probs,
        "yt_impactful_likes": yt_likes_most_impactful_videos_json,
        "yt_impactful_channels": yt_subscriptions_most_impactful_channels_json,
        "vk_impactful_likes": vk_most_impactful_liked_posts_json,
        "vk_impactful_groups": vk_most_impactful_groups_json
    }


# Чтобы запустить с помощью Unicorn: uvicorn main:app --host 0.0.0.0 --port 8090 (example)

# При запуске с помощью Uvicorn, этот блок не требуется.
# Если вы запускаете файл напрямую, он позволяет запустить сервер.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
