# Script to load CSV to MongoDB

"""
Simple script to load CSV into MongoDB
Just run: python load_data_simple.py
"""

import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "heart_attack_db")

print(" Connecting to MongoDB Atlas...")
client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

# Test connection
try:
    client.admin.command('ping')
    print(" Connected successfully!")
except Exception as e:
    print(f" Connection failed: {e}")
    exit()

# Read your CSV file
print("\n Reading Medicaldataset.csv...")
df = pd.read_csv("Medicaldataset.csv")
print(f" Found {len(df)} records in CSV")

# Get collections (like tables in SQL)
patients_col = db["patients"]
medical_records_col = db["medical_records"]
heart_attack_tests_col = db["heart_attack_tests"]

# Clear existing data (fresh start)
print("\n Clearing existing data...")
patients_col.delete_many({})
medical_records_col.delete_many({})
heart_attack_tests_col.delete_many({})

# Load data into 3 collections
print("\n💾 Loading data into MongoDB...")

for index, row in df.iterrows():
    # Generate IDs
    patient_id = f"P{str(index + 1).zfill(4)}"
    record_id = f"R{str(index + 1).zfill(4)}"
    test_id = f"T{str(index + 1).zfill(4)}"
    timestamp = datetime.now()
    
    # Collection 1: Patients (demographics)
    patients_col.insert_one({
        "patient_id": patient_id,
        "age": int(row['Age']),
        "gender": int(row['Gender']),
        "created_at": timestamp
    })
    
    # Collection 2: Medical Records (vital signs)
    medical_records_col.insert_one({
        "record_id": record_id,
        "patient_id": patient_id,  # Links to patients collection
        "heart_rate": int(row['Heart rate']),
        "systolic_blood_pressure": int(row['Systolic blood pressure']),
        "diastolic_blood_pressure": int(row['Diastolic blood pressure']),
        "blood_sugar": int(row['Blood sugar']),
        "recorded_at": timestamp
    })
    
    # Collection 3: Heart Attack Tests (lab results)
    heart_attack_tests_col.insert_one({
        "test_id": test_id,
        "record_id": record_id,  # Links to medical_records collection
        "ck_mb": float(row['CK-MB']),
        "troponin": float(row['Troponin']),
        "result": row['Result'].strip().lower(),
        "test_date": timestamp
    })

# Create indexes (like primary keys in SQL)
print("\n Creating indexes...")
patients_col.create_index("patient_id", unique=True)
medical_records_col.create_index("record_id", unique=True)
heart_attack_tests_col.create_index("test_id", unique=True)

# Summary
print("\n" + "="*50)
print(" SUCCESS! Data loaded into MongoDB")
print("="*50)
print(f" Patients collection: {patients_col.count_documents({})} records")
print(f" Medical records collection: {medical_records_col.count_documents({})} records")
print(f" Heart attack tests collection: {heart_attack_tests_col.count_documents({})} records")
print("\n Task 1 database creation is COMPLETE!")
print("\n Next: Check your data in MongoDB Atlas web interface")
print("   Go to: Browse Collections → heart_attack_db")

client.close()