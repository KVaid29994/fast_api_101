from fastapi import FastAPI, HTTPException
import json

app = FastAPI(title="My practice app", description="patient data app", version="1.00.0.1")

with open("patient.json") as f:
    patient_data = json.load(f)

@app.get("/")
def intro():
    return {"message": "patient information system"} 

@app.get("/about")
def about():
    return {"about": "get information about patients and their diagnosis"}

@app.get("/calculate/{num1}/{num2}")
def multiply(num1: int, num2: int):
    return {"message": f"the product of {num1} and {num2} is", "result": num1 * num2}

@app.get("/patient/{patient_id}")
def fetch_info(patient_id: int):
    for item in patient_data:
        if item["patient_id"] == patient_id:   # ✅ fixed
            return item
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/patient")
def patient_info():
    return patient_data
