from fastapi import APIRouter, HTTPException
from database import get_collection
from typing import Dict, Any

router = APIRouter()


@router.get("/latest-entry")
def latest_entry() -> Dict[str, Any]:
    """Return the latest combined patient + medical_record + heart_attack_test entry.

    The predict script expects a JSON with keys: 'patient', 'medical_record', 'heart_attack_test'.
    This endpoint finds the most recent heart_attack_tests document (by test_date) and
    joins it with the linked medical_records and patients documents.
    """
    try:
        tests_coll = get_collection("heart_attack_tests")
        records_coll = get_collection("medical_records")
        patients_coll = get_collection("patients")

        # Find latest test by test_date (descending)
        latest_test = tests_coll.find_one(sort=[("test_date", -1)])
        if not latest_test:
            raise HTTPException(status_code=404, detail="No heart attack tests found")

        # Find linked medical record
        record_id = latest_test.get("record_id")
        medical_record = records_coll.find_one({"record_id": record_id}) if record_id else None

        # Find patient (linked from medical_record.patient_id)
        patient = None
        if medical_record:
            patient_id = medical_record.get("patient_id")
            if patient_id:
                patient = patients_coll.find_one({"patient_id": patient_id})

        # Normalize ObjectId and datetime for JSON serialization
        def clean_doc(doc):
            if not doc:
                return None
            doc = dict(doc)
            # remove Mongo internal _id if present
            doc.pop("_id", None)
            return doc

        return {
            "patient": clean_doc(patient),
            "medical_record": clean_doc(medical_record),
            "heart_attack_test": clean_doc(latest_test),
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
