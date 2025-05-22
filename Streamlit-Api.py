import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from PIL import Image

# Display DRISA logo
logo = Image.open("Drisa_Logo.jpg")
st.image(logo, use_column_width=False, width=150)

st.markdown("<div style='text-align: center;'><img src='drisa_logo.png' width='150'></div>", unsafe_allow_html=True)

# Load trained model
model = joblib.load('concrete_xgb_model.pkl')

# Strength category classifier
def classify_strength_category(strength_value):
    if strength_value < 30:
        return 'Low Strength'
    elif 30 <= strength_value < 60:
        return 'Medium Strength'
    elif 60 <= strength_value < 100:
        return 'High Strength'
    else:
        return 'Ultra-high Strength'

# App title
st.title("Concrete Compressive Strength Prediction With AI")
st.subheader("Enter the mixture composition and age to predict strength (MPa)")

# Input fields
cement = st.number_input("Cement (kg/m³)", min_value=0.0, key="cement")
slag = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, key="slag")
flyash = st.number_input("Fly Ash (kg/m³)", min_value=0.0, key="flyash")
water = st.number_input("Water (kg/m³)", min_value=0.0, key="water")
superplasticizer = st.number_input("Superplasticizer (kg/m³)", min_value=0.0, key="superplasticizer")
coarseagg = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, key="coarseagg")
fineagg = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0, key="fineagg")
age = st.number_input("Age (days)", min_value=1, max_value=365, key="age")

# Buttons
col1, col2 = st.columns(2)

with col1:
    predict_clicked = st.button("Predict Strength")

with col2:
    reset_clicked = st.button("Reset Inputs")

# Reset logic
if reset_clicked:
    st.experimental_rerun()

# Prediction logic
if predict_clicked:
    input_data = pd.DataFrame([{
        "cement": cement,
        "slag": slag,
        "fly_ash": flyash,
        "water": water,
        "superplasticizer": superplasticizer,
        "coarse_agg": coarseagg,
        "fine_agg": fineagg,
        "age": age
    }])

    prediction = model.predict(input_data)[0]
    strength_category = classify_strength_category(prediction)

    st.success(f"Predicted Compressive Strength: {prediction:.2f} MPa")

    emoji_map = {
        "Low Strength": "🔴",
        "Medium Strength": "🟠",
        "High Strength": "🟢",
        "Ultra-high Strength": "🔵"
    }
    st.write(f"**Strength Category:** {emoji_map[strength_category]} {strength_category}")

    # Pie chart visualization
    categories = ['Low Strength', 'Medium Strength', 'High Strength', 'Ultra-high Strength']
    values = [0, 0, 0, 0]

    if strength_category in categories:
        index = categories.index(strength_category)
        values[index] = 1

    fig, ax = plt.subplots()
    ax.pie(
        values,
        labels=categories,
        autopct=lambda p: f'{p:.0f}%' if p > 0 else '',
        startangle=90,
        colors=['#FF9999', '#FFCC99', '#99FF99', '#66B2FF']
    )
    ax.axis('equal')
    st.pyplot(fig)
