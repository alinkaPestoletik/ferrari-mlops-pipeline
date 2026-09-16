# code/deployment/app/streamlit_app.py
import streamlit as st
import requests

FASTAPI_URL = "http://fastapi:8000/predict"

st.title("🏎️ Scuderia Ferrari Podium Predictor")

grid = st.number_input("Starting Grid Position", min_value=1, max_value=30, value=1)
laps = st.number_input("Laps Completed", min_value=0, max_value=100, value=50)
year = st.number_input("Year", min_value=1950, max_value=2026, value=2024)
driverRef = st.text_input("Driver", value="leclerc")

if st.button("Predict"):
    input_data = {
        "grid": grid,
        "laps": laps,
        "year": year,
        "driverRef": driverRef
    }

    response = requests.post(FASTAPI_URL, json=input_data)

    if response.status_code == 200:
        prediction = response.json()["prediction"]
        if prediction == 1:
            st.success("The model predicts a PODIUM finish")
        else:
            st.warning("No podium predicted this time")
    else:
        st.error("Error connecting to API")