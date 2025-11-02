from fastapi import APIRouter, HTTPException
from typing import List, Optional
from database import get_collection
from bson.objectid import ObjectId
from bson.errors import InvalidId

router = APIRouter()

def heart_tests_coll():
	return get_collection("heart_attack_tests")


@router.post("/heart-attack-tests", status_code=201)
def create_heart_test(payload: dict):
	"""Create a heart attack test document.

	Expects a dict with keys like test_id, record_id, ck_mb, troponin, result, test_date
	"""
	coll = heart_tests_coll()
	try:
		res = coll.insert_one(payload)
		return {"inserted_id": str(res.inserted_id)}
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.get("/heart-attack-tests")
def get_all_heart_tests():
	coll = heart_tests_coll()
	try:
		docs = list(coll.find())
		for d in docs:
			d["_id"] = str(d["_id"])
		return docs
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.get("/heart-attack-tests/{test_id}")
def get_heart_test(test_id: str):
	coll = heart_tests_coll()
	try:
		doc = coll.find_one({"test_id": test_id})
		if not doc:
			raise HTTPException(status_code=404, detail="Test not found")
		doc["_id"] = str(doc["_id"])
		return doc
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.get("/heart-attack-tests/record/{record_id}")
def get_tests_by_record(record_id: str):
	coll = heart_tests_coll()
	try:
		docs = list(coll.find({"record_id": record_id}))
		if not docs:
			raise HTTPException(status_code=404, detail="No tests found for this record")
		for d in docs:
			d["_id"] = str(d["_id"])
		return docs
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.put("/heart-attack-tests/{test_id}")
def update_heart_test(test_id: str, payload: dict):
	coll = heart_tests_coll()
	try:
		res = coll.update_one({"test_id": test_id}, {"$set": payload})
		if res.matched_count == 0:
			raise HTTPException(status_code=404, detail="Test not found")
		return {"matched_count": res.matched_count, "modified_count": res.modified_count}
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))


@router.delete("/heart-attack-tests/{test_id}")
def delete_heart_test(test_id: str):
	coll = heart_tests_coll()
	try:
		res = coll.delete_one({"test_id": test_id})
		if res.deleted_count == 0:
			raise HTTPException(status_code=404, detail="Test not found")
		return {"deleted_count": res.deleted_count}
	except HTTPException:
		raise
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

