import torch
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import uvicorn
import pickle
from transformers import BertTokenizer, BertForSequenceClassification
import json
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session


from parser.yt_parser import init_youtube_with_user_token, get_user_yt_subscriptions, get_user_liked_videos, \
    YTChannel, YTVideoInfo, get_youtube_channel_id
from ml.yt_ml import analyze_youtube_user_subscriptions, analyze_youtube_list_of_vids
from parser.vk_parser import init_vk_api_session, get_self_vk_data, VKLike, VKWallPost, VKGroup, get_vk_user_id
from ml.vk_ml import analyze_vk_groups, analyze_vk_likes
from tools.tools import merge_and_average_dicts, split_dict_into_labels_and_values, merge_and_average_multiple_dicts
from ml.tg_ml import analyze_tg_list_of_texts

from db.db_func import yt_save_data_to_db, yt_get_by_id, vk_save_data_to_db, vk_get_by_id, tg_save_data_to_db, \
    tg_get_by_id


with open('cfg.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

SQLALCHEMY_DATABASE_URL = cfg['db_path']

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()

app = FastAPI()

# Флаг для использования BERT
USE_BERT = cfg['use_bert']
NUM_LABLES = 100

# Загрузка BERT модели и токенизатора
if USE_BERT:
    model_name = "DeepPavlov/rubert-base-cased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    bert_model = BertForSequenceClassification.from_pretrained(model_name, num_labels=NUM_LABLES)
    bert_model.load_state_dict(torch.load('models/bert/text_model.pth'))
    bert_model.eval()  # Перевести модель в режим оценки
# Загрузка LR
else:
    with open('models/text_model.sav', 'rb') as file:
        text_model = pickle.load(file)
    tokenizer = None

with open('models/text_model_mlb.pkl', 'rb') as file:
    multi_label_binarizer = pickle.load(file)


# Class that represents API input structure
class InputData(BaseModel):
    yt_token: str
    vk_token: str
    tg_posts: list[str]


@app.post("/predict")
def predict(input_data: InputData, db: Session = Depends(get_db)):
    # VK section
    vk_sum_dict = None
    vk_most_impactful_liked_posts = None
    vk_most_impactful_groups = None
    if input_data.vk_token != "":
        vk = init_vk_api_session(input_data.vk_token)

        vk_self_id = get_vk_user_id(vk)

        vk_cached_res = vk_get_by_id(db, vk_self_id)
        if vk_cached_res is not None:
            vk_sum_dict = vk_cached_res
        else:
            vk_groups, vk_wall, vk_user_likes = get_self_vk_data(vk)

            vk_groups_average_classes_score_dict, vk_most_impactful_groups = analyze_vk_groups(
                vk_user_likes,
                text_model,
                multi_label_binarizer,
                USE_BERT,
                tokenizer
            )

            if len(vk_most_impactful_groups) > 5:
                vk_most_impactful_groups = vk_most_impactful_groups[:5]

            vk_likes_average_classes_score_dict, vk_most_impactful_liked_posts = analyze_vk_likes(
                vk_groups,
                text_model,
                multi_label_binarizer,
                USE_BERT,
                tokenizer
            )

            if len(vk_most_impactful_liked_posts) > 5:
                vk_most_impactful_liked_posts = vk_most_impactful_liked_posts[:5]

            vk_sum_dict = merge_and_average_dicts(vk_likes_average_classes_score_dict,
                                                  vk_groups_average_classes_score_dict,
                                                  weight1=1,
                                                  weight2=3)

            vk_save_data_to_db(db, vk_self_id, vk_sum_dict)

    # YouTube section
    yt_sum_dict = None
    yt_likes_most_impactful_videos = None
    yt_subscriptions_most_impactful_channels = None
    if input_data.yt_token != "":
        try:
            # Initialize YT API
            youtube_api_instance = init_youtube_with_user_token(
                input_data.yt_token,
                'secrets/google_project_secret.apps.googleusercontent.com.json'  # Path to Google App Credentials
            )

            yt_self_id = get_youtube_channel_id(youtube_api_instance)

            yt_cached_res = yt_get_by_id(db, yt_self_id)
            if yt_cached_res is not None:
                yt_sum_dict = yt_cached_res
            else:

                # Get list of user subscriptions
                youtube_user_subscriptions: list[YTChannel] = get_user_yt_subscriptions(youtube_api_instance)
                youtube_user_likes: list[YTVideoInfo] = get_user_liked_videos(youtube_api_instance)

                yt_subscriptions_average_classes_score_dict, yt_subscriptions_most_impactful_channels = \
                    analyze_youtube_user_subscriptions(
                        youtube_user_subscriptions,
                        text_model,
                        multi_label_binarizer,
                        youtube_api_instance,
                        USE_BERT,
                        tokenizer
                    )

                if len(yt_subscriptions_most_impactful_channels) > 5:
                    yt_subscriptions_most_impactful_channels = yt_subscriptions_most_impactful_channels[:5]

                yt_likes_average_classes_score_dict, yt_likes_most_impactful_videos = analyze_youtube_list_of_vids(
                    youtube_user_likes,
                    text_model,
                    multi_label_binarizer,
                    USE_BERT,
                    tokenizer
                )

                if len(yt_likes_most_impactful_videos) > 5:
                    yt_likes_most_impactful_videos = yt_likes_most_impactful_videos[:5]

                yt_sum_dict = merge_and_average_dicts(yt_subscriptions_average_classes_score_dict,
                                                      yt_likes_average_classes_score_dict,
                                                      weight1=2,
                                                      weight2=1)

                yt_save_data_to_db(db, yt_self_id, yt_sum_dict)

        except Exception as e:
            print(e)

        # Do not raise an exception for now (yt api quota lack might cause this, we don't want to terminate cause of it)
        # raise HTTPException(status_code=500, detail=str(e))

    tg_sum_dict = None
    if input_data.tg_posts:
        tg_sum_dict = analyze_tg_list_of_texts(
            input_data.tg_posts,
            text_model,
            multi_label_binarizer,
            USE_BERT,
            tokenizer
        )

    dicts_list = [vk_sum_dict, yt_sum_dict, tg_sum_dict]
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
    uvicorn.run(app, host=cfg['host'], port=cfg['port'])
