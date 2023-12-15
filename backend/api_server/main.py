from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import pickle


app = FastAPI()
model = pickle.load(open('models/text_model.sav', 'rb'))


class InputData(BaseModel):
    yt_token: str
    vk_token: str
    tg_token: str
    tg_login: str
    tg_psw: str


@app.post("/predict")
def predict(input_data: InputData):
    try:
        prediction = model.predict([input_data.yt_token])
        return {
            "predictions": prediction.tolist(),
            "predictions_score": prediction.tolist(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Unicorn: uvicorn main:app

# При запуске с помощью Uvicorn, этот блок не требуется.
# Если вы запускаете файл напрямую, он позволяет запустить сервер.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
