# Heart Attack Prediction Pipeline – FastAPI + MongoDB/MySQL + ML

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Phinah/Prediction-Pipeline)

## Overview

This project demonstrates:
- **Database design** using MongoDB (NoSQL) and MySQL (SQL)
- **RESTful API** with FastAPI for CRUD operations on patient data
- **Machine Learning integration** - Heart attack risk prediction model
- **Prediction pipeline** - Fetches latest patient data from API and predicts heart attack risk
- **Cloud deployment** - Dockerized API deployable to Render, Railway, or any container platform

## 🚀 Quick Start (Using Hosted API)

**For users cloning this repo who want to use the prediction script:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Phinah/Prediction-Pipeline.git
   cd Prediction-Pipeline/heart-attack-prediction
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set the API URL to the hosted endpoint:**
   ```bash
   # Windows PowerShell
   $env:API_URL = "https://heart-attack-prediction-api.onrender.com/api/latest-entry"
   
   # Linux/Mac
   export API_URL="https://heart-attack-prediction-api.onrender.com/api/latest-entry"
   ```

4. **Run the prediction script:**
   ```bash
   cd predict
   python predict.py
   ```

The script will fetch the latest patient data from the hosted API, run it through the ML model, and display the prediction results.

---

## 🌐 Deploy Your Own API Instance

### Option 1: Deploy to Render (Recommended - Free Tier Available)

1. **Fork this repository** to your GitHub account

2. **Set up MongoDB Atlas** (free tier):
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
   - Create a free cluster
   - Create a database user and get your connection string:
     ```
     mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
     ```
   - Whitelist all IPs (0.0.0.0/0) in Network Access for Render to connect

3. **Deploy to Render:**
   - Sign up at [Render](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render will auto-detect the `Dockerfile`
   - Set environment variables in Render dashboard:
     - `MONGODB_URL`: Your MongoDB Atlas connection string
     - `DATABASE_NAME`: `heart_attack_prediction_db`
   - Click "Create Web Service"

4. **Load data into MongoDB:**
   ```bash
   # After deployment, run this locally pointing to your Atlas cluster
   $env:MONGODB_URL = "your-atlas-connection-string"
   cd heart-attack-prediction
   python mongodb/load_data.py
   ```

5. **Your API is now live!** Get the URL from Render (e.g., `https://your-app.onrender.com`)

6. **Update predict.py to use your hosted API:**
   ```bash
   $env:API_URL = "https://your-app.onrender.com/api/latest-entry"
   python predict/predict.py
   ```

### Option 2: Deploy to Railway

1. Install Railway CLI: `npm install -g @railway/cli`
2. Login: `railway login`
3. Create project: `railway init`
4. Add MongoDB plugin: `railway add mongodb`
5. Set environment variables:
   ```bash
   railway variables set MONGODB_URL=$MONGO_URL
   railway variables set DATABASE_NAME=heart_attack_prediction_db
   ```
6. Deploy: `railway up`

### Option 3: Run Locally with Docker

```bash
cd heart-attack-prediction

# Build image
docker build -t heart-attack-api .

# Run container (connect to local MongoDB or Atlas)
docker run -p 8000:8000 \
  -e MONGODB_URL="mongodb://host.docker.internal:27017" \
  -e DATABASE_NAME="heart_attack_prediction_db" \
  heart-attack-api
```

---

## 📁 Project Structure

```
heart-attack-prediction/
├── mongodb/                    # MongoDB API implementation
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # MongoDB connection & utilities
│   ├── config.py               # Configuration
│   ├── routes/                 # API endpoints
│   │   ├── patients.py
│   │   ├── medical_records.py
│   │   └── heart_attack_tests.py
│   ├── get_endpoints.py        # /api/latest-entry endpoint
│   └── load_data.py            # Script to populate MongoDB from CSV
├── predict/                    # Prediction scripts
│   └── predict.py              # Fetch data from API and predict
├── ml_model/                   # Model training notebooks
│   └── model.ipynb
├── Dockerfile                  # Docker configuration for deployment
├── render.yaml                 # Render deployment config
├── requirements.txt            # Python dependencies
└── .env.example                # Environment variables template
```

---

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- MongoDB (local or Atlas)
- Git

### Setup Steps

1. **Clone and install:**
   ```bash
   git clone https://github.com/Phinah/Prediction-Pipeline.git
   cd Prediction-Pipeline/heart-attack-prediction
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB connection string
   ```

3. **Load sample data:**
   ```bash
   python mongodb/load_data.py
   ```

4. **Run the API:**
   ```bash
   uvicorn mongodb.main:app --reload --port 8000
   ```

5. **Test the API:**
   - Swagger UI: http://localhost:8000/docs
   - Get latest entry: http://localhost:8000/api/latest-entry

6. **Run prediction:**
   ```bash
   cd predict
   python predict.py
   ```

---

## 🧪 API Endpoints

### MongoDB Endpoints

**GET** `/api/latest-entry` - Fetch latest patient + medical record + heart attack test (for prediction)

**Patients:**
- POST `/patients` - Create patient
- GET `/patients` - List all patients
- GET `/patients/{id}` - Get patient by ID
- PUT `/patients/{id}` - Update patient
- DELETE `/patients/{id}` - Delete patient

**Medical Records:**
- POST `/medical-records` - Create record
- GET `/medical-records` - List all records
- GET `/medical-records/{id}` - Get record
- PUT `/medical-records/{id}` - Update record
- DELETE `/medical-records/{id}` - Delete record

**Heart Attack Tests:**
- POST `/heart-attack-tests` - Create test
- GET `/heart-attack-tests` - List all tests
- GET `/heart-attack-tests/{id}` - Get test
- PUT `/heart-attack-tests/{id}` - Update test
- DELETE `/heart-attack-tests/{id}` - Delete test

### MySQL Endpoints (Legacy)

See `mySQL/main.py` for MySQL-based endpoints.

---

## 🤖 Machine Learning Model

The prediction model is trained on heart attack risk factors:
- **Features**: Age, Gender, Heart Rate, Blood Pressure, Blood Sugar, CK-MB, Troponin
- **Model**: Random Forest Classifier
- **Accuracy**: ~85% (see `ml_model/model.ipynb` for training details)

**Model files** (generated after training):
- `heart_attack_model.pkl` - Trained model
- `feature_names.pkl` - Feature order for inference

---

## 🔐 Environment Variables

Required for deployment:

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb+srv://user:pass@cluster0.mongodb.net/` |
| `DATABASE_NAME` | Database name | `heart_attack_prediction_db` |
| `PORT` | API port (auto-set by Render) | `8000` |
| `API_URL` | (For predict.py) Hosted API endpoint | `https://your-app.onrender.com/api/latest-entry` |

---

## 📊 Data Schema

### MongoDB Collections

**patients**
```json
{
  "patient_id": 1,
  "age": 45,
  "gender": 1  // 1=Male, 0=Female
}
```

**medical_records**
```json
{
  "patient_id": 1,
  "heart_rate": 75,
  "systolic_blood_pressure": 120,
  "diastolic_blood_pressure": 80,
  "blood_sugar": 100,
  "record_date": "2025-11-09"
}
```

**heart_attack_tests**
```json
{
  "patient_id": 1,
  "medical_record_id": 1,
  "ck_mb": 25,
  "troponin": 0.03,
  "result": "negative",
  "test_date": "2025-11-09"
}
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is part of an academic assignment for ALU.

---

## 👥 Authors

- **Phinah** - [GitHub](https://github.com/Phinah)
- **Contributors** - See commit history

---

## 🆘 Troubleshooting

**"Cannot connect to API" error in predict.py:**
- Ensure `API_URL` environment variable is set
- Check that the hosted API is running (visit the /health endpoint)
- Verify MongoDB Atlas is accessible (check Network Access whitelist)

**MongoDB connection errors:**
- Check `MONGODB_URL` is correct
- Ensure database user has read/write permissions
- Verify IP whitelist includes 0.0.0.0/0 for cloud deployments

**Docker build fails:**
- Ensure `requirements.txt` is up to date
- Check Docker has enough disk space
- Try `docker system prune` to free up space

---

For more help, open an issue on GitHub!
