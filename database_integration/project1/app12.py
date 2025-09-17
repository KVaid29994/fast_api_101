from fastapi import FastAPI, HTTPException
from typing import List
from models import Patient, PatientOut
import crud

app = FastAPI()

@app.post("/patients/", response_model=PatientOut)
async def create_patient(patient: Patient):
    new_patient = await crud.create_patient(patient.dict())
    return new_patient

@app.get("/patients/", response_model=List[PatientOut])
async def get_patients():
    return await crud.list_patients()

@app.get("/patients/{id}", response_model=PatientOut)
async def get_patient(id: str):
    patient = await crud.get_patient(id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.put("/patients/{id}", response_model=PatientOut)
async def update_patient(id: str, patient: Patient):
    updated = await crud.update_patient(id, patient.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated

@app.delete("/patients/{id}")
async def delete_patient(id: str):
    deleted = await crud.delete_patient(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}
