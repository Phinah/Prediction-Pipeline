"""
Medical Records CRUD Operations
Route: /medical-records
"""

from fastapi import APIRouter, HTTPException
from heart_project.models import MedicalRecord
from heart_project.db import medical_records_coll, patients_coll
from bson.objectid import ObjectId
from bson.errors import InvalidId

router = APIRouter()


@router.post("/medical-records", status_code=201)
def create_medical_record(record: MedicalRecord):
    """Create a new medical record"""
    data = record.dict()
    
    # Verify patient exists 
    patient_id = data.get("patient_id")
    if patient_id:
        # Check if patient exists
        patient = patients_coll.find_one({"patient_id": patient_id})
        if not patient:
            raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    
    try:
        res = medical_records_coll.insert_one(data)
        return {"inserted_id": str(res.inserted_id), "message": "Medical record created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/medical-records")
def get_all_medical_records():
    """Get all medical records"""
    try:
        records = list(medical_records_coll.find())
        for record in records:
            record["_id"] = str(record["_id"])
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/medical-records/{record_id}")
def get_medical_record(record_id: str):
    """Get specific medical record by ID"""
    try:
        try:
            oid = ObjectId(record_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid record id")
        
        record = medical_records_coll.find_one({"_id": oid})
        if not record:
            raise HTTPException(status_code=404, detail="Medical record not found")
        
        record["_id"] = str(record["_id"])
        return record
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/medical-records/patient/{patient_id}")
def get_patient_records(patient_id: str):
    """Get all medical records for a specific patient"""
    try:
        records = list(medical_records_coll.find({"patient_id": patient_id}))
        if not records:
            raise HTTPException(status_code=404, detail=f"No records found for patient {patient_id}")
        
        for record in records:
            record["_id"] = str(record["_id"])
        return records
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/medical-records/{record_id}")
def update_medical_record(record_id: str, record: MedicalRecord):
    """Update a medical record"""
    data = record.dict()
    
    try:
        try:
            oid = ObjectId(record_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid record id")
        
        res = medical_records_coll.update_one({"_id": oid}, {"$set": data})
        if res.matched_count == 0:
            raise HTTPException(status_code=404, detail="Medical record not found")
        
        return {
            "matched_count": res.matched_count,
            "modified_count": res.modified_count,
            "message": "Medical record updated"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/medical-records/{record_id}")
def delete_medical_record(record_id: str):
    """Delete a medical record"""
    try:
        try:
            oid = ObjectId(record_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid record id")
        
        res = medical_records_coll.delete_one({"_id": oid})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Medical record not found")
        
        return {
            "deleted_count": res.deleted_count,
            "message": "Medical record deleted"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))