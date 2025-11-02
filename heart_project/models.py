# models.py
from pydantic import BaseModel, Field, conint, confloat

class Patient(BaseModel):
    age: conint(ge=0, le=130)
    gender: str
    heart_rate: conint(ge=0)
    systolic_bp: conint(ge=0)
    diastolic_bp: conint(ge=0)
    blood_sugar: confloat(ge=0)
    ck_mb: confloat(ge=0)
    troponin: confloat(ge=0)
    result: conint(ge=0, le=1)
