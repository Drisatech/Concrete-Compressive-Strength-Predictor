import streamlit as st
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from PIL import Image

# Load model
model = joblib.load("concrete_xgb_model.pkl")

# Load and display logo centered
logo = Image.open("Drisa_Logo.jpg")
logo = logo.resize((100, 100))
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image(logo)

st.markdown("<h2 style='text-align: center;'>Concrete Strength Prediction</h2>", unsafe_allow_html=True)

# App title
st.title("Concrete Compressive Strength Prediction With AI")
st.subheader("Enter the mixture composition and age to predict strength (MPa)")

# Strength categories
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

# Set default values using session_state
default_inputs = {
    'cement': 0.0,
    'slag': 0.0,
    'fly_ash': 0.0,
    'water': 0.0,
    'superplasticizer': 0.0,
    'coarse_agg': 0.0,
    'fine_agg': 0.0,
    'age': 1
}

# Initialize inputs if not present
for key, val in default_inputs.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Form
with st.form("input_form"):
    st.session_state.cement = st.number_input("Cement (kg/m³)", min_value=0.0, step=1.0, value=st.session_state.cement, key="cement")
    st.session_state.slag = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, step=1.0, value=st.session_state.slag, key="slag")
    st.session_state.fly_ash = st.number_input("Fly Ash (kg/m³)", min_value=0.0, step=1.0, value=st.session_state.fly_ash, key="fly_ash")
    st.session_state.water = st.number_input("Water (kg/m³)", min_value=0.0, step=1.0, value=st.session_state.water, key="water")
    st.session_state.superplasticizer = st.number_input("Superplasticizer (kg/m³)", min_value=0.0, step=1.0, value=st.session_state.superplasticizer, key="superplasticizer")
    st.session_state.coarse_agg = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, step=1.0, value=st.session_state.coarse_agg, key="coarse_agg")
    st.session_state.fine_agg = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0, step=1.0, value=st.session_state.fine_agg, key="fine_agg")
    st.session_state.age = st.number_input("Age (days)", min_value=1, max_value=365, step=1, value=st.session_state.age, key="age")

    col1, col2 = st.columns(2)
    with col1:
        predict = st.form_submit_button("Predict Strength")
    with col2:
        reset = st.form_submit_button("Reset Input")

# Handle Reset
if reset:
    for key in default_inputs:
        st.session_state[key] = default_inputs[key]
    st.experimental_rerun()

# Handle Predict
if predict:
    input_data = pd.DataFrame([{
        "cement": st.session_state.cement,
        "slag": st.session_state.slag,
        "fly_ash": st.session_state.fly_ash,
        "water": st.session_state.water,
        "superplasticizer": st.session_state.superplasticizer,
        "coarse_agg": st.session_state.coarse_agg,
        "fine_agg": st.session_state.fine_agg,
        "age": st.session_state.age
    }])

    prediction = model.predict(input_data)[0]
    category = classify_strength_category(prediction)

    st.success(f"Predicted Strength: {prediction:.2f} MPa")
    st.write(f"**Strength Category:** {emoji_map[category]} {category}")

    categories = list(emoji_map.keys())
    values = [1 if category == c else 0 for c in categories]

    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct=lambda p: f'{p:.0f}%' if p > 0 else '', startangle=90,
           colors=['#FF9999', '#FFCC99', '#99FF99', '#66B2FF'])
    ax.axis('equal')
    st.pyplot(fig)
