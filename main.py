# main.py - AQI Prediction Backend API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os

app = FastAPI(title="AQI Prediction API")

# Allow requests from Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Train model on startup ──────────────────────────────────────────────────
print("Loading dataset and training model...")

df = pd.read_csv("city_day.csv")
df = df.dropna(subset=["AQI"])
df = df.drop(columns=["City", "Date", "AQI_Bucket", "Xylene"], errors="ignore")
df = df.fillna(df.median())

X = df.drop(columns=["AQI"])
y = df["AQI"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

MODEL_METRICS = {
    "mae":      round(mean_absolute_error(y_test, y_pred), 2),
    "rmse":     round(np.sqrt(mean_squared_error(y_test, y_pred)), 2),
    "r2":       round(r2_score(y_test, y_pred), 4),
    "accuracy": round(100 - mape, 2),
}

FEATURE_COLUMNS = X.columns.tolist()
print(f"Model ready! Accuracy: {MODEL_METRICS['accuracy']}%")

# ── Helper ──────────────────────────────────────────────────────────────────
def get_aqi_level(aqi: float) -> dict:
    if aqi <= 50:
        return {"level": "Good", "message": "Air quality is satisfactory", "color": "#00e400"}
    elif aqi <= 100:
        return {"level": "Satisfactory", "message": "Minor concern for sensitive people", "color": "#92d14f"}
    elif aqi <= 200:
        return {"level": "Moderate", "message": "May cause breathing discomfort on prolonged exposure", "color": "#ffff00"}
    elif aqi <= 300:
        return {"level": "Poor", "message": "Causes breathing discomfort to most people", "color": "#ff7e00"}
    elif aqi <= 400:
        return {"level": "Very Poor", "message": "Health warning — limit outdoor exposure", "color": "#ff0000"}
    else:
        return {"level": "Severe", "message": "EMERGENCY! Stay indoors", "color": "#7e0023"}

# ── Request schema ───────────────────────────────────────────────────────────
class PollutantInput(BaseModel):
    PM2_5: float
    PM10: float
    NO: float
    NO2: float
    NOx: float
    NH3: float
    CO: float
    SO2: float
    O3: float
    Benzene: float
    Toluene: float

# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "AQI Prediction API is running"}

@app.get("/metrics")
def get_metrics():
    """Return model performance metrics"""
    return MODEL_METRICS

@app.post("/predict")
def predict(data: PollutantInput):
    """Predict AQI from pollutant values"""
    input_dict = {
        "PM2.5": data.PM2_5,
        "PM10":  data.PM10,
        "NO":    data.NO,
        "NO2":   data.NO2,
        "NOx":   data.NOx,
        "NH3":   data.NH3,
        "CO":    data.CO,
        "SO2":   data.SO2,
        "O3":    data.O3,
        "Benzene": data.Benzene,
        "Toluene": data.Toluene,
    }

    input_df = pd.DataFrame([input_dict], columns=FEATURE_COLUMNS)
    predicted_aqi = round(float(rf.predict(input_df)[0]), 1)
    alert = get_aqi_level(predicted_aqi)

    return {
        "aqi":     predicted_aqi,
        "level":   alert["level"],
        "message": alert["message"],
        "color":   alert["color"],
    }
