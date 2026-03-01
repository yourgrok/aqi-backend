# AQI Prediction Backend — Deployment Guide

## Your folder should look like this:
```
aqi-backend/
├── main.py
├── requirements.txt
├── city_day.csv        ← download this from your Colab
└── README.md
```

---

## Step 1 — Download city_day.csv from Colab
In Google Colab, go to the left sidebar → Files icon → right-click `city_day.csv` → Download.
Put it in this folder alongside main.py.

---

## Step 2 — Upload to GitHub
1. Go to github.com → Sign in → Click "New repository"
2. Name it `aqi-backend` → Click "Create repository"
3. Upload all 4 files (main.py, requirements.txt, city_day.csv, README.md)
   - Click "uploading an existing file" → drag and drop all 4 → Commit

---

## Step 3 — Deploy on Render
1. Go to render.com → Log in
2. Click "New +" → "Web Service"
3. Connect your GitHub account → Select `aqi-backend` repo
4. Fill in these settings:
   - **Name:** aqi-backend (or anything)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. Wait ~3 minutes for it to deploy

---

## Step 4 — Get your live URL
After deploy, Render gives you a URL like:
`https://aqi-backend-xxxx.onrender.com`

Test it by opening: `https://your-url.onrender.com/metrics`
You should see your model accuracy in the browser.

---

## Step 5 — Use in Lovable
Paste this Lovable prompt:

```
Build an AQI prediction dashboard. It should have input fields for:
PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene.

When the user clicks "Predict AQI", send a POST request to:
https://YOUR-RENDER-URL.onrender.com/predict

With this JSON body:
{
  "PM2_5": <value>,
  "PM10": <value>,
  "NO": <value>,
  "NO2": <value>,
  "NOx": <value>,
  "NH3": <value>,
  "CO": <value>,
  "SO2": <value>,
  "O3": <value>,
  "Benzene": <value>,
  "Toluene": <value>
}

Display the returned "aqi" value, "level" (e.g. Good/Poor/Severe),
and "message" in a colored card using the returned "color" hex code.

Also fetch GET https://YOUR-RENDER-URL.onrender.com/metrics on load
and display MAE, RMSE, R², and Accuracy in a stats bar.
```

Replace YOUR-RENDER-URL with your actual Render URL.

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | / | Health check |
| GET | /metrics | Model accuracy stats |
| POST | /predict | Predict AQI from pollutant values |
