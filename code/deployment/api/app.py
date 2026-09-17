from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd


with open("models/model.pkl", "rb") as f:
    model = joblib.load(f)

app = FastAPI(title="Ferrari Predictor API")

class RaceInput(BaseModel):
    grid: int
    laps: int
    year: int
    driverRef: str

@app.post("/predict")
def predict(input_data: RaceInput):
    data = pd.DataFrame([input_data.model_dump()])
    prediction = model.predict(data)
    return {"prediction": int(prediction[0])}