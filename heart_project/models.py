from pydantic import BaseModel
from typing import Optional


class Patient(BaseModel):
    # Minimal fields used by the API; allow extra fields to pass through
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

    class Config:
        extra = "allow"
