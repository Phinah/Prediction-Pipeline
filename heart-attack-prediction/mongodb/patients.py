from fastapi import APIRouter, HTTPException
from heart_project.models import Patient
from heart_project.db import patients_coll
from bson.objectid import ObjectId
from bson.errors import InvalidId

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Heart Patients API is running!"}


@router.post("/patients", status_code=201)
def create_patient(patient: Patient):
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
        res = patients_coll.insert_one(data)
        return {"inserted_id": str(res.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patients")
def get_all_patients():
    try:
        patients = list(patients_coll.find())
        for patient in patients:
            patient["_id"] = str(patient["_id"])
        return patients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/patients/{patient_id}")
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


@router.delete("/patients/{patient_id}")
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
