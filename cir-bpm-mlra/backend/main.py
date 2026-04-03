from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import users_collection, bp_collection
from auth import hash_password, verify_password, create_token
from ml_service import predict_bp
from jose import jwt, JWTError
from datetime import datetime
from dotenv import load_dotenv
import os
from fastapi.responses import StreamingResponse
import csv
from io import StringIO

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

app = FastAPI()

# ---------------- MODELS ----------------

class Register(BaseModel):
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class BPData(BaseModel):
    sbp: int
    dbp: int
    hr: int


# ---------------- TOKEN VALIDATION ----------------

def get_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["email"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------- REGISTER ----------------

@app.post("/register")
def register(user: Register):
    try:
        print("👉 Register API called")

        # Check if user exists
        existing_user = users_collection.find_one({"email": user.email})
        if existing_user:
            return {"message": "User already exists"}

        # Insert new user
        users_collection.insert_one({
            "email": user.email,
            "password": hash_password(user.password)
        })

        print("✅ User registered successfully")

        return {"message": "registered"}

    except Exception as e:
        print("❌ REGISTER ERROR:", e)
        return {"error": str(e)}


# ---------------- LOGIN ----------------

@app.post("/login")
def login(user: Login):
    try:
        print("👉 Login API called")

        db_user = users_collection.find_one({"email": user.email})

        if not db_user:
            return {"error": "User not found"}

        if not verify_password(user.password, db_user["password"]):
            return {"error": "Invalid password"}

        token = create_token({"email": user.email})

        print("✅ Login successful")

        return {"access_token": token}

    except Exception as e:
        print("❌ LOGIN ERROR:", e)
        return {"error": str(e)}


# ---------------- PREDICT ----------------

@app.post("/predict")
def predict(data: BPData, token: str):
    try:
        print("👉 Predict API called")

        email = get_user(token)

        risk = predict_bp(data.sbp, data.dbp, data.hr)

        bp_collection.insert_one({
            "email": email,
            "sbp": data.sbp,
            "dbp": data.dbp,
            "hr": data.hr,
            "prediction": risk,
            "timestamp": datetime.utcnow()
        })

        print("✅ Data stored successfully")

        return {"risk": risk}

    except Exception as e:
        print("❌ PREDICT ERROR:", e)
        return {"error": str(e)}


# ---------------- GET RECORDS ----------------

@app.get("/records")
def records(token: str):
    try:
        print("👉 Records API called")

        email = get_user(token)

        data = list(bp_collection.find({"email": email}, {"_id": 0}))

        print(f"✅ Retrieved {len(data)} records")

        return data

    except Exception as e:
        print("❌ RECORDS ERROR:", e)
        return {"error": str(e)}

# ---------------- DOWNLOAD RECORDS ----------------

@app.get("/download")
def download_csv(token: str):
    try:
        email = get_user(token)

        data = list(bp_collection.find({"email": email}, {"_id": 0}))

        if not data:
            return {"message": "No data found"}

        # Convert to CSV
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

        output.seek(0)

        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=bp_data.csv"}
        )

    except Exception as e:
        return {"error": str(e)}