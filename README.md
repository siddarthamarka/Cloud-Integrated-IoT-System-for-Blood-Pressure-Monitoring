## 📌 Overview

This project presents an **end-to-end IoT-based healthcare system** that monitors blood pressure in real-time and predicts health risk using machine learning.

The system integrates:

* **IoT (ESP32 + BP Sensor)** for data acquisition
* **FastAPI backend** for processing
* **Machine Learning model** for risk prediction
* **MongoDB Atlas** for cloud storage
* **Streamlit dashboard** for visualization

---

## 🚀 Features

* 📡 Real-time BP data collection (SBP, DBP, HR)
* ☁️ Cloud-based data storage (MongoDB Atlas)
* 🤖 ML-based risk prediction (Normal, Alert, Warning, Emergency)
* 📊 Interactive dashboard with live data visualization
* 🔐 User authentication (login/register system)
* 🌐 WiFi-based communication (ESP32 → Cloud)

---

## 🏗️ System Architecture

```text
BP Sensor → ESP32 → WiFi → FastAPI → ML Model → MongoDB → Streamlit Dashboard
```

---

## ⚙️ Tech Stack

### 🔹 Hardware

* ESP32-WROOM-32
* Digital Blood Pressure Sensor

### 🔹 Software

* Python
* FastAPI
* Streamlit
* MongoDB Atlas
* TensorFlow / Keras
* Arduino IDE

---

## 📁 Project Structure

```text
cir-bpm-mlra/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   ├── .env
│
├── dashboard/
│   ├── app.py
│
├── esp32/
│   ├── code.ino
│
└── README.md
```

---

## 🔧 Setup Instructions

---

### 🧪 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

👉 Open:

```
http://127.0.0.1:8000/docs
```

---

### 📊 2. Dashboard Setup

```bash
cd dashboard
streamlit run app.py
```

👉 Open:

```
http://localhost:8501
```

---

### 🌐 3. Configure ESP32

Update in code:

```cpp
String server = "http://YOUR_IP:8000/predict";
String token = "YOUR_LOGIN_TOKEN";
```

👉 Upload code and open Serial Monitor

---

### 📡 4. Network Setup

* Connect **ESP32 and Laptop to same WiFi**
* Allow port **8000 in firewall**

---

## 🤖 Machine Learning Model

* Input: SBP, DBP, HR
* Model: Neural Network (Dense Layers)
* Output Classes:

  * Normal
  * Alert
  * Warning
  * Emergency

---

## 📊 Sample Output

```text
SBP: 120
DBP: 80
HR : 75
Prediction: Normal
```

---

## 🎯 Use Cases

* Remote patient monitoring
* Early detection of hypertension
* Smart healthcare systems
* Telemedicine applications

---

## 🔮 Future Enhancements

* 📱 Mobile application integration
* 🚨 SMS/Email alerts for abnormal conditions
* 📈 Advanced analytics & trends
* ⌚ Wearable device integration
* ☁️ Full cloud deployment (public access)

---

## 🧠 Key Learnings

* IoT communication using ESP32
* REST API development with FastAPI
* Cloud database integration
* ML model deployment
* Real-time dashboard development
