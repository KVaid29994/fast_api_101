from pydantic import BaseModel, EmailStr
from typing import Optional

class Patient(BaseModel):
    id : int
    age: int
    weight: float
    height: int
    gender: str
    blood_type: str
    disease: str
    admission_date: str
    discharged: str
    bmi: float

class PatientOut(Patient):
    _id : str


