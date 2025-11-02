# main.py
from fastapi import FastAPI, HTTPException
from models import Patient
from db import patients_coll

app = FastAPI(title="Heart Patients API")

# Optional root endpoint
@app.get("/")
def root():
    return {"message": "Heart Patients API is running!"}

# POST endpoint to create a patient
@app.post("/patients", status_code=201)
def create_patient(patient: Patient):
    data = patient.dict()
    
    # Normalize gender
    g = data.get("gender").strip().lower()
    if g in ("m", "male", "1"):
        data["gender"] = "Male"
    elif g in ("f", "female", "0"):
        data["gender"] = "Female"

    try:
        res = patients_coll.insert_one(data)
        return {"inserted_id": str(res.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET endpoint to fetch all patients
@app.get("/patients")
def get_all_patients():
    try:
        patients = list(patients_coll.find())
        # Convert ObjectId to string for JSON serialization
        for patient in patients:
            patient["_id"] = str(patient["_id"])
        return patients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
