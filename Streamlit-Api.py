import streamlit as st
import numpy as np
import pandas as pd
import joblib
from PIL import Image

# Load model
model = joblib.load("concrete_xgb_model.pkl")

# Load and display logo
logo = Image.open("Drisa_Logo.jpg")
logo = logo.resize((100, 100))
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image(logo)

st.markdown("<h2 style='text-align: center;'>Concrete Strength Prediction</h2>", unsafe_allow_html=True)

# Define strength classification function
def classify_strength_category(value):
    if value < 30:
        return "Low Strength"
    elif 30 <= value < 60:
        return "Medium Strength"
    elif 60 <= value < 100:
        return "High Strength"
    else:
        return "Ultra-high Strength"

emoji_map = {
    "Low Strength": "🔴",
    "Medium Strength": "🟠",
    "High Strength": "🟢",
    "Ultra-high Strength": "🔵"
}

# Reset function
def reset_inputs():
    for key in st.session_state.keys():
        del st.session_state[key]

# Input form
with st.form("strength_form"):
    cement = st.number_input("Cement (kg/m³)", min_value=0.0, step=1.0, key="cement")
    slag = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, step=1.0, key="slag")
    fly_ash = st.number_input("Fly Ash (kg/m³)", min_value=0.0, step=1.0, key="fly_ash")
    water = st.number_input("Water (kg/m³)", min_value=0.0, step=1.0, key="water")
    superplasticizer = st.number_input("Superplasticizer (kg/m³)", min_value=0.0, step=1.0, key="superplasticizer")
    coarse_agg = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, step=1.0, key="coarse_agg")
    fine_agg = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0, step=1.0, key="fine_agg")
    age = st.number_input("Age (days)", min_value=1, max_value=365, step=1, key="age")

    col1, col2 = st.columns([1, 1])
    with col1:
        predict_btn = st.form_submit_button("Predict Strength")
    with col2:
        reset_btn = st.form_submit_button("Reset Input")

# Predict logic
if predict_btn:
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
    strength_category = classify_strength_category(prediction)

    st.success(f"Predicted Strength: {prediction:.2f} MPa")
    st.info(f"**Strength Category:** {emoji_map[strength_category]} {strength_category}")

    # Pie chart
    import matplotlib.pyplot as plt
    categories = list(emoji_map.keys())
    values = [1 if strength_category == c else 0 for c in categories]
    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct=lambda p: f'{p:.0f}%' if p > 0 else '', startangle=90,
           colors=['#FF9999', '#FFCC99', '#99FF99', '#66B2FF'])
    ax.axis('equal')
    st.pyplot(fig)

# Reset logic
if reset_btn:
    reset_inputs()
    st.experimental_rerun()
