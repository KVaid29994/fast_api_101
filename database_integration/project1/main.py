from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

MONGO_DETAILS = "mongodb+srv://vaidkashish290994_db_user:lZaSbQS3kmZJQlQd@kvcluster.kxvrajh.mongodb.net/"

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.Database1

# # user_collection = database.get_collection("collection1")

# client = MongoClient(MONGO_DETAILS)
# try:
#     # Run a test command
#     client.admin.command("ping")
#     print("✅ Cluster is working and reachable!")
# except Exception as e:
#     print("❌ Error:", e)