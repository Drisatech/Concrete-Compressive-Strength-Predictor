# Streamlit-Api.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from PIL import Image

# Page Config
st.set_page_config(page_title="Concrete Strength Predictor", layout="centered")

# Load Trained Model
model = joblib.load("concrete_xgb_model.pkl")

# Load Logo
logo = Image.open("Drisa_Logo.jpg")
st.image(logo, width=100)

# Title
st.title("Concrete Compressive Strength Prediction With AI")
st.subheader("Enter mixture composition and age to predict strength (MPa)")

# Form
with st.form("input_form"):
    cement = st.number_input("Cement (kg/m³)", min_value=0.0, step=1.0, value=0.0, key="cement")
    slag = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, step=1.0, value=0.0, key="slag")
    fly_ash = st.number_input("Fly Ash (kg/m³)", min_value=0.0, step=1.0, value=0.0, key="fly_ash")
    water = st.number_input("Water (kg/m³)", min_value=0.0, step=1.0, value=0.0, key="water")
    superplasticizer = st.number_input("Superplasticizer (kg/m³)", min_value=0.0, step=1.0, value=0.0, key="superplasticizer")
    coarse_agg = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, step=1.0, value=0.0, key="coarse_agg")
    fine_agg = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0, step=1.0, value=0.0, key="fine_agg")
    age = st.number_input("Age (days)", min_value=1, step=1, value=1, key="age")

    submit = st.form_submit_button("Predict Strength")
    reset = st.form_submit_button("Reset Input")

# Reset Logic
if reset:
    st.session_state.clear()
    st.experimental_rerun()

# Prediction and Display
if submit:
    input_data = pd.DataFrame([{
        "cement": cement,
        "slag": slag,
        "fly_ash": fly_ash,
        "water": water,
        "superplasticizer": superplasticizer,
        "coarse_agg": coarse_agg,
        "fine_agg": fine_agg,
        "age": age
    }])

    prediction = model.predict(input_data)[0]

    def classify_strength_category(value):
        if value < 30:
            return "Low Strength"
        elif 30 <= value < 60:
            return "Medium Strength"
        elif 60 <= value < 100:
            return "High Strength"
        else:
            return "Ultra-high Strength"

    strength_category = classify_strength_category(prediction)

    emoji_map = {
        "Low Strength": "🔴",
        "Medium Strength": "🟠",
        "High Strength": "🟢",
        "Ultra-high Strength": "🔵"
    }

    st.success(f"Predicted Compressive Strength: **{prediction:.2f} MPa**")
    st.write(f"**Strength Category:** {emoji_map[strength_category]} {strength_category}")

    # Pie Chart Visualization
    categories = ["Low Strength", "Medium Strength", "High Strength", "Ultra-high Strength"]
    values = [1 if cat == strength_category else 0 for cat in categories]

    fig, ax = plt.subplots()
    ax.pie(
        values,
        labels=categories,
        autopct=lambda p: f'{p:.0f}%' if p > 0 else '',
        startangle=90,
        colors=["#FF9999", "#FFCC99", "#99FF99", "#66B2FF"]
    )
    ax.axis("equal")
    st.pyplot(fig)
