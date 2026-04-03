import certifi
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# ✅ LOAD .env FILE
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

print("Mongo URL:", MONGO_URL)  # DEBUG

client = MongoClient(MONGO_URL, tlsCAFile=certifi.where())

db = client["bpdb"]

users_collection = db["users"]
bp_collection = db["bpdata"]