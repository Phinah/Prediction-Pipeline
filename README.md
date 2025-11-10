# Heart Attack Prediction Pipeline

## Overview

This project demonstrates a complete machine learning pipeline for heart attack risk prediction, featuring:
- Database design using MongoDB (NoSQL) and MySQL (SQL)
- RESTful API with FastAPI for CRUD operations on patient data
- Machine Learning integration with a trained Random Forest classifier
- Prediction pipeline that fetches latest patient data from API and predicts heart attack risk
- Cloud deployment infrastructure using Docker and Render

## Project Structure

```
Prediction-Pipeline/
├── mongodb/                    # MongoDB API implementation
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # MongoDB connection configuration
│   ├── config.py               # Application configuration
│   ├── routes/                 # API route handlers
│   │   ├── patients.py
│   │   ├── medical_records.py
│   │   └── heart_attack_tests.py
│   ├── get_endpoints.py        # GET endpoints including /api/latest-entry
│   └── post_endpoints.py       # POST endpoints
├── mySQL/                      # MySQL API implementation
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # MySQL connection configuration
│   ├── models.py               # Database models
│   ├── create_table_main.sql   # Table creation scripts
│   ├── sample_data.sql         # Sample data insertion
│   ├── stored_procedure.sql    # Stored procedures
│   └── trigger.sql             # Database triggers
├── predict/                    # Prediction scripts
│   ├── predict.py              # Main prediction script
│   ├── heart_attack_model.pkl  # Trained ML model
│   └── feature_names.pkl       # Feature names for model input
├── ml_model/                   # Model training notebooks
├── Dockerfile                  # Docker configuration for deployment
├── render.yaml                 # Render.com deployment configuration
├── requirements.txt            # Python dependencies
└── .env.example                # Environment variables template
```

## Prerequisites

- Python 3.11 or higher
- MongoDB installed locally or MongoDB Atlas account
- MySQL Server 8.0 or higher
- Git
- Virtual environment tool (venv)

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Phinah/Prediction-Pipeline.git
cd Prediction-Pipeline
```

### 2. Create and Activate Virtual Environment

Windows PowerShell:
```powershell
python -m venv myenv
.\myenv\Scripts\Activate.ps1
```

Linux/Mac:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## MongoDB Setup and Usage

### Step 1: Install and Configure MongoDB

**Option A: Local MongoDB Installation**

1. Download MongoDB Community Server from https://www.mongodb.com/try/download/community
2. Install and start the MongoDB service
3. MongoDB will run on default port 27017

**Option B: MongoDB Atlas (Cloud)**

1. Create a free account at https://www.mongodb.com/cloud/atlas/register
2. Create a new cluster
3. Create a database user with read/write permissions
4. Get your connection string:
   ```
   mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Whitelist your IP address or use 0.0.0.0/0 for all IPs

### Step 2: Configure Environment Variables

Create a `.env` file in the `mongodb` directory:

```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=heart_attack_prediction_db
```

For MongoDB Atlas, use your connection string:
```
MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=heart_attack_prediction_db
```

### Step 3: Database Schema

The MongoDB database uses three collections:

**patients**
```json
{
  "patient_id": 1,
  "age": 45,
  "gender": 1
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

### Step 4: Run MongoDB API

Open a terminal and start the FastAPI server:

```bash
cd mongodb
python main.py
```

The API will start on http://localhost:8000

### Step 5: Run Prediction Script

Open a second terminal, activate the virtual environment, and run the prediction script:

Windows PowerShell:
```powershell
.\myenv\Scripts\Activate.ps1
cd predict
python predict.py
```

Linux/Mac:
```bash
source myenv/bin/activate
cd predict
python predict.py
```

The script will:
1. Fetch the latest patient data from http://localhost:8000/api/latest-entry
2. Load the trained machine learning model
3. Make a prediction on the patient's heart attack risk
4. Display the results and save them to `prediction_log.txt`

## MySQL Setup and Usage

### Step 1: Install and Configure MySQL

1. Download MySQL Server 8.0 from https://dev.mysql.com/downloads/mysql/
2. Install MySQL and note the root password you set during installation
3. Start the MySQL service

Windows:
```powershell
net start MySQL80
```

Linux:
```bash
sudo systemctl start mysql
```

### Step 2: Create Database and Tables

1. Log into MySQL:
```bash
mysql -u root -p
```

2. Create the database:
```sql
CREATE DATABASE heart_attack_prediction_db;
USE heart_attack_prediction_db;
```

3. Run the table creation script:
```bash
mysql -u root -p heart_attack_prediction_db < mySQL/create_table_main.sql
```

4. Insert sample data:
```bash
mysql -u root -p heart_attack_prediction_db < mySQL/sample_data.sql
```

5. Create stored procedures and triggers:
```bash
mysql -u root -p heart_attack_prediction_db < mySQL/stored_procedure.sql
mysql -u root -p heart_attack_prediction_db < mySQL/trigger.sql
```

### Step 3: Configure MySQL Connection

Create a `.env` file in the `mySQL` directory:

```
DB_HOST=localhost
DB_USER=root
DB_PASS=your_mysql_password
DB_NAME=heart_attack_prediction_db
```

Replace `your_mysql_password` with your actual MySQL root password.

### Step 4: Database Schema

The MySQL database uses two tables:

**patients**
```sql
CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    age INT NOT NULL,
    gender TINYINT NOT NULL,
    result VARCHAR(50)
);
```

**tests**
```sql
CREATE TABLE tests (
    test_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    heart_rate INT,
    systolic_bp INT,
    diastolic_bp INT,
    blood_sugar FLOAT,
    ck_mb FLOAT,
    troponin FLOAT,
    recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
);
```

### Step 5: Run MySQL API

Open a terminal and start the FastAPI server:

```bash
cd mySQL
python main.py
```

The API will start on http://localhost:8000

### Step 6: Run Prediction Script with MySQL

Open a second terminal, activate the virtual environment, and set the API URL to use the MySQL endpoint:

Windows PowerShell:
```powershell
.\myenv\Scripts\Activate.ps1
$env:API_URL = "http://localhost:8000/api/latest-entry"
cd predict
python predict.py
```

Linux/Mac:
```bash
source myenv/bin/activate
export API_URL="http://localhost:8000/api/latest-entry"
cd predict
python predict.py
```

The prediction script works the same way with MySQL as it does with MongoDB.

## API Endpoints

### MongoDB API Endpoints

**GET /api/latest-entry** - Fetch latest patient with medical record and heart attack test data

**Patients:**
- POST `/patients` - Create a new patient
- GET `/patients` - List all patients
- GET `/patients/{id}` - Get patient by ID
- PUT `/patients/{id}` - Update patient information
- DELETE `/patients/{id}` - Delete a patient

**Medical Records:**
- POST `/medical-records` - Create a new medical record
- GET `/medical-records` - List all medical records
- GET `/medical-records/{id}` - Get medical record by ID
- PUT `/medical-records/{id}` - Update medical record
- DELETE `/medical-records/{id}` - Delete medical record

**Heart Attack Tests:**
- POST `/heart-attack-tests` - Create a new heart attack test
- GET `/heart-attack-tests` - List all heart attack tests
- GET `/heart-attack-tests/{id}` - Get heart attack test by ID
- PUT `/heart-attack-tests/{id}` - Update heart attack test
- DELETE `/heart-attack-tests/{id}` - Delete heart attack test

### MySQL API Endpoints

**GET /api/latest-entry** - Fetch latest patient with test data

**Patients:**
- POST `/patients` - Create a new patient
- GET `/patients` - List all patients
- GET `/patients/{id}` - Get patient by ID
- PUT `/patients/{id}` - Update patient information
- DELETE `/patients/{id}` - Delete a patient

**Tests:**
- POST `/tests` - Create a new test record
- GET `/tests` - List all tests
- GET `/tests/{id}` - Get test by ID
- PUT `/tests/{id}` - Update test record
- DELETE `/tests/{id}` - Delete test record

### Testing the API

Access the interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Machine Learning Model

The prediction model uses a Random Forest classifier trained on heart attack risk factors.

**Features:**
- Age
- Gender (1 = Male, 0 = Female)
- Heart Rate
- Systolic Blood Pressure
- Diastolic Blood Pressure
- Blood Sugar
- CK-MB (Creatine Kinase-MB enzyme level)
- Troponin (Cardiac troponin level)

**Model Files:**
- `heart_attack_model.pkl` - Trained Random Forest model
- `feature_names.pkl` - Feature names in correct order for prediction

**Model Performance:**
The model achieves approximately 85% accuracy on test data. Training details can be found in `ml_model/model.ipynb`.

## Cloud Deployment

### Deploy to Render.com

1. Push your code to GitHub

2. Set up MongoDB Atlas:
   - Create a free cluster at https://www.mongodb.com/cloud/atlas
   - Get your connection string
   - Whitelist all IPs (0.0.0.0/0) in Network Access

3. Create a new Web Service on Render:
   - Go to https://render.com
   - Click "New +" then "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the Dockerfile

4. Set environment variables in Render dashboard:
   ```
   MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME=heart_attack_prediction_db
   ```

5. Deploy and get your API URL from Render

6. Use the hosted API with predict.py:
   ```bash
   $env:API_URL = "https://your-app.onrender.com/api/latest-entry"
   python predict/predict.py
   ```

### Docker Local Deployment

Build and run the Docker container:

```bash
docker build -t heart-attack-api .
docker run -p 8000:8000 -e MONGODB_URL="mongodb://host.docker.internal:27017" -e DATABASE_NAME="heart_attack_prediction_db" heart-attack-api
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` or `mongodb+srv://...` |
| `DATABASE_NAME` | MongoDB database name | `heart_attack_prediction_db` |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASS` | MySQL password | `your_password` |
| `DB_NAME` | MySQL database name | `heart_attack_prediction_db` |
| `API_URL` | API endpoint for predict.py | `http://localhost:8000/api/latest-entry` |
| `PORT` | API server port | `8000` |

## Troubleshooting

**MongoDB connection errors:**
- Verify MongoDB service is running
- Check MONGODB_URL in .env file is correct
- For Atlas, ensure IP is whitelisted
- Verify database user has proper permissions

**MySQL connection errors:**
- Verify MySQL service is running: `mysql -u root -p`
- Check DB_HOST, DB_USER, DB_PASS in .env file
- Ensure database exists: `SHOW DATABASES;`
- Verify tables exist: `SHOW TABLES;`

**API returns 404 errors:**
- Ensure the API server is running on port 8000
- Check that main.py is running without errors
- Verify the endpoint URL is correct

**Prediction script fails:**
- Ensure API_URL environment variable is set
- Verify the API is accessible at the specified URL
- Check that model files exist in predict/ directory
- Confirm the API returns data in the expected format

**Import errors:**
- Activate the virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version is 3.11 or higher

**Port already in use:**
- Change the port in main.py or use `--port` flag
- Kill the process using port 8000

## License

This project is part of an academic assignment for ALU.

## Authors

- Phinah - https://github.com/Phinah
- Contributors - See commit history
