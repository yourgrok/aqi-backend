🌫 AQI Prediction Backend API
A Machine Learning powered FastAPI backend that predicts Air Quality Index (AQI) based on pollutant concentrations.
<img width="1460" height="977" alt="image" src="https://github.com/user-attachments/assets/13b915e3-4d9d-4917-befe-8a83392dc825" />

Deployed using Render and built with FastAPI + Uvicorn.
🚀 Features
🔮 Predict AQI using pollutant values
📊 Returns AQI level (Good / Moderate / Poor / Severe etc.)
<img width="1470" height="663" alt="Screenshot 2026-03-04 001906" src="https://github.com/user-attachments/assets/af45442e-8629-4b53-95b3-36709de698ab" />

🎨 Returns color code for UI display
📈 Model performance metrics endpoint
☁️ Deployable on Render (free tier supported)
📁 Project Structure
aqi-backend/
├── main.py              # FastAPI app
├── requirements.txt     # Dependencies
├── city_day.csv         # Dataset (downloaded from Colab)
└── README.md            # Documentation
🧠 Model Inputs
The model expects the following pollutant values:
PM2.5
PM10
NO
NO2
NOx
NH3
CO
SO2
O3
Benzene
Toluene
📡 API Endpoints
1️⃣ Predict AQI
POST /predict
Request Body (JSON)
{
  "PM2_5": 120,
  "PM10": 180,
  "NO": 15,
  "NO2": 40,
  "NOx": 55,
  "NH3": 20,
  "CO": 0.8,
  "SO2": 10,
  "O3": 25,
  "Benzene": 1.5,
  "Toluene": 2.1
}
Response Example
{
  "aqi": 178.34,
  "level": "Poor",
  "message": "Air quality is unhealthy for sensitive groups.",
  "color": "#FF7E00"
}
2️⃣ Model Metrics

GET /metrics

Returns:

{
  "MAE": 18.24,
  "RMSE": 26.51,
  "R2": 0.91,
  "Accuracy": 87.3
}
🛠 Local Setup
1️⃣ Clone the Repository
git clone https://github.com/YOUR-USERNAME/aqi-backend.git
cd aqi-backend
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Server
uvicorn main:app --reload

Open in browser:

http://127.0.0.1:8000/docs

FastAPI Swagger UI will appear.

☁️ Deploy on Render
Step 1 — Push to GitHub
Upload:
main.py
requirements.txt
city_day.csv
README.md
Step 2 — Create Web Service on Render
Go to https://render.com
Click New → Web Service
Connect GitHub repo
Use these settings:
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

Click Create Web Service

Wait ~3 minutes for deployment.

🌍 Live API Usage

After deployment, Render gives a URL like:

https://aqi-backend-xxxx.onrender.com

Test:

https://your-url.onrender.com/metrics
🎨 Frontend Integration (Lovable / React / JS)
Predict Endpoint

Send POST request to:

https://YOUR-RENDER-URL.onrender.com/predict
Metrics Endpoint

Fetch:

https://YOUR-RENDER-URL.onrender.com/metrics

Display:

AQI value

AQI level

Message

Color-coded card (using returned hex code)

MAE, RMSE, R², Accuracy in stats bar

📊 Tech Stack

FastAPI

Uvicorn

Scikit-learn

Pandas

NumPy

Render (Deployment)

📌 Notes

Ensure city_day.csv is in the root directory.

Free Render services may sleep after inactivity.

First request after sleep may take ~30 seconds.

👨‍💻 Author

AQI Prediction Backend
Built for ML Deployment Practice 🚀
