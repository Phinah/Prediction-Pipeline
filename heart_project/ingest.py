# ingest.py
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/patients"
CSV_PATH = "data/heart.csv"

def transform_row(row):
    return {
        "age": int(row["Age"]),
        "gender": str(row["Gender"]),
        "heart_rate": int(row["Heart rate"]),
        "systolic_bp": int(row["Systolic blood pressure"]),
        "diastolic_bp": int(row["Diastolic blood pressure"]),
        "blood_sugar": float(row["Blood sugar"]),
        "ck_mb": float(row["CK-MB"]),
        "troponin": float(row["Troponin"]),
        "result": int(row["Result"])
    }

df = pd.read_csv(CSV_PATH)
for _, row in df.iterrows():
    payload = transform_row(row)
    resp = requests.post(API_URL, json=payload)
    if resp.status_code not in (200,201):
        print("Failed row:", _, resp.text)
