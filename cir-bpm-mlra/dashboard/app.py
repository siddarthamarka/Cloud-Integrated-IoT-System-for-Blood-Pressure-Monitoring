import streamlit as st
import requests
import pandas as pd
import datetime
from utils import get_recommendation
from streamlit_autorefresh import st_autorefresh

API_URL = "http://127.0.0.1:8000"

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Cloud-Integrated IoT System for Real-Time Blood Pressure Monitoring with Machine Learning-Based Risk Analysis",
    layout="wide"
)

# ---------- LOAD CSS ----------
try:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass  # Avoid crash if CSS missing

# ---------- TITLE ----------
st.title("Cloud-Integrated IoT System for Real-Time Blood Pressure Monitoring with Machine Learning-Based Risk Analysis")

# ---------- SESSION ----------
if "token" not in st.session_state:
    st.session_state.token = None

# ---------- SIDEBAR ----------
menu = st.sidebar.selectbox("Menu", ["Login", "Register", "Dashboard"])

# ================= LOGIN =================
if menu == "Login":

    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        r = requests.post(f"{API_URL}/login", json={
            "email": email,
            "password": password
        })

        if r.status_code == 200 and "access_token" in r.json():
            st.session_state.token = r.json()["access_token"]
            st.success("✅ Login Successful")
        else:
            st.error("❌ Invalid Credentials")


# ================= REGISTER =================
elif menu == "Register":

    st.subheader("📝 Register New Patient")

    email = st.text_input("New Email")
    password = st.text_input("New Password", type="password")

    if st.button("Register"):

        r = requests.post(f"{API_URL}/register", json={
            "email": email,
            "password": password
        })

        if r.status_code == 200:
            st.success("✅ User Registered Successfully")
        else:
            st.error("❌ Registration Failed")


# ================= DASHBOARD =================
elif menu == "Dashboard":

    # 🔥 AUTO REFRESH (every 5 seconds)
    st_autorefresh(interval=5000, key="datarefresh")

    if not st.session_state.token:
        st.warning("⚠ Please login first")
        st.stop()

    st.subheader("📊 Patient Health Data")
    st.caption("🔄 Auto refreshing every 5 seconds...")
    st.caption(f"Last updated: {datetime.datetime.now().strftime('%H:%M:%S')}")

    # ---------- FETCH DATA ----------
    try:
        r = requests.get(
            f"{API_URL}/records",
            params={"token": st.session_state.token}
        )

        if r.status_code != 200:
            st.error("❌ Failed to fetch data")
            st.stop()

        df = pd.DataFrame(r.json())

    except Exception as e:
        st.error(f"❌ API Error: {e}")
        st.stop()

    # ---------- EMPTY CHECK ----------
    if df.empty:
        st.warning("No data available yet")
        st.stop()

    # ---------- PROCESS ----------
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    latest = df.iloc[-1]

    # ---------- METRICS ----------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("SBP", latest["sbp"])
    col2.metric("DBP", latest["dbp"])
    col3.metric("HR", latest["hr"])
    col4.metric("Risk", latest["prediction"])

    # ---------- ALERT COLORS ----------
    if latest["prediction"] == "Emergency":
        st.error("🚨 EMERGENCY! Immediate action required!")
    elif latest["prediction"] == "Warning":
        st.warning("⚠ Warning level detected")
    elif latest["prediction"] == "Alert":
        st.info("ℹ Alert condition")
    else:
        st.success("✅ Normal condition")

    # ---------- RECOMMENDATION ----------
    st.info("💡 Recommendation: " + get_recommendation(latest["prediction"]))

    st.markdown("---")

    # ---------- GRAPHS ----------
    st.subheader("📈 Blood Pressure Trends")
    st.line_chart(df.set_index("timestamp")[["sbp", "dbp"]])

    st.subheader("❤️ Heart Rate Trend")
    st.line_chart(df.set_index("timestamp")["hr"])

    st.markdown("---")

    # ---------- TABLE ----------
    st.subheader("📋 Patient History")
    st.dataframe(df)

    # ---------- DOWNLOAD CSV ----------
    st.subheader("⬇ Export Data")

    try:
        response = requests.get(
            f"{API_URL}/download",
            params={"token": st.session_state.token}
        )

        if response.status_code == 200:
            st.download_button(
                label="⬇ Download CSV",
                data=response.content,
                file_name="bp_data.csv",
                mime="text/csv"
            )
        else:
            st.error("❌ Download failed")

    except Exception as e:
        st.error(f"❌ Download error: {e}")

    # ---------- LOGOUT ----------
    st.markdown("---")

    if st.button("🚪 Logout"):
        st.session_state.token = None
        st.success("Logged out successfully")