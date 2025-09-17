from bson import ObjectId
from main import database

patient_collection = database.get_collection("collection1")

def patient_helper(patient) -> dict:
    return {
        "_id": str(patient["_id"]),
        "id": patient.get("id"),
        "name": patient.get("name", "Unknown"),
        "age": patient.get("age", 0),
        "weight": patient.get("weight", 0.0),
        "height": patient.get("height", 0),
        "gender": patient.get("gender", "Unknown"),
        "blood_type": patient.get("blood_type", "Unknown"),
        "disease": patient.get("disease", "Unknown"),
        "admission_date": patient.get("admission_date", "N/A"),
        "discharged": patient.get("discharged", "N/A"),
        "bmi": patient.get("bmi", 0.0),
    }

# Create
async def create_patient(patient_data:dict) -> dict:
    patient =await patient_collection.insert_one(patient_data)
    new_patient = await patient_collection.find_one({"_id": patient.inserted_id})
    return patient_helper(new_patient)

async def list_patients():
    patients = []
    async for patient in patient_collection.find():
        patients.append(patient_helper(patient))
    return patients

async def get_patient(id: str):
    patient = await patient_collection.find_one({"_id": ObjectId(id)})
    if patient:
        return patient_helper(patient)
    
async def update_patient(id: str, data: dict):
    patient = await patient_collection.find_one({"_id": ObjectId(id)})
    if patient:
        await patient_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        updated = await patient_collection.find_one({"_id": ObjectId(id)})
        return patient_helper(updated)
    return False

async def delete_patient(id: str):
    patient = await patient_collection.find_one({"_id": ObjectId(id)})
    if patient:
        await patient_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False