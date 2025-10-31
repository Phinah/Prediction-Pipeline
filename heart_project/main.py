# main.py
from fastapi import FastAPI, HTTPException
from models import Patient
from db import patients_coll
from bson.objectid import ObjectId
from bson.errors import InvalidId

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


# PUT endpoint to update an existing patient by id
@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient: Patient):
    data = patient.dict()

    # Normalize gender
    g = data.get("gender")
    if isinstance(g, str):
        g = g.strip().lower()
        if g in ("m", "male", "1"):
            data["gender"] = "Male"
        elif g in ("f", "female", "0"):
            data["gender"] = "Female"

    try:
        try:
            oid = ObjectId(patient_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid patient id")

        res = patients_coll.update_one({"_id": oid}, {"$set": data})
        if res.matched_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"matched_count": res.matched_count, "modified_count": res.modified_count}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# DELETE endpoint to remove a patient by id
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    try:
        try:
            oid = ObjectId(patient_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid patient id")

        res = patients_coll.delete_one({"_id": oid})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Patient not found")
        return {"deleted_count": res.deleted_count}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
