from pymongo import MongoClient
import pandas as pd

from fastapi import FastAPI, HTTPException , Query
from bson import ObjectId
from typing import List

app = FastAPI(title="Patient mangement")
client = MongoClient("mongodb+srv://vaidkashish290994_db_user:lZaSbQS3kmZJQlQd@kvcluster.kxvrajh.mongodb.net/") 

db = client["Database1"]          # your database name
collection = db["collection1"]         # your collection name

@app.get("/")
def home():
    return {"message":"welcome patient"}

@app.get("/patients")
def get_all_patients():
    patients = list(collection.find({},{"_id": 0}))
    return {"count": len(patients), "data": patients}


@app.get("/patient/{name}")
def get_patient_by_name(name: str):
    patients = list(collection.find({},{"_id": 0}))


    for patient in patients:
        if patient['name'] == name:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/bloodgroup")
def get_patients_blood_group(blood_group : str = Query(...)):
    """
    Find patients by blood group.
    Example: GET /patients?blood_group=B+
    """
    query = {"blood_type": {"$regex": f"^{blood_group}$", "$options": "i"}}
    patients = list(collection.find(query, {"_id": 0}))

    return {"count": len(patients), "data": patients}