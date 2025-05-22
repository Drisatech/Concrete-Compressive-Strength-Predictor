# Streamlit-Api.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib

# Load the trained XGBoost model
model = joblib.load('concrete_xgb_model.pkl')

# Strength classification function
def classify_strength_category(strength_value):
    if strength_value < 30:
        return 'Low Strength'
    elif 30 <= strength_value < 60:
        return 'Medium Strength'
    elif 60 <= strength_value < 100:
        return 'High Strength'
    else:
        return 'Ultra-high Strength'

# Emoji map for strength categories
emoji_map = {
    "Low Strength": "🔴",
    "Medium Strength": "🟠",
    "High Strength": "🟢",
    "Ultra-high Strength": "🔵"
}

# Streamlit UI
st.set_page_config(page_title="Concrete Strength Predictor", layout="centered")
st.title("Concrete Compressive Strength Prediction with AI")
st.subheader("Enter the concrete mixture composition and age (in days)")

# User Inputs
cement = st.number_input("Cement (kg/m³)", min_value=0.0, value=200.0)
slag = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, value=50.0)
flyash = st.number_input("Fly Ash (kg/m³)", min_value=0.0, value=30.0)
water = st.number_input("Water (kg/m³)", min_value=0.0, value=180.0)
superplasticizer = st.number_input("Superplasticizer (kg/m³)", min_value=0.0, value=5.0)
coarseagg = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, value=900.0)
fineagg = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0, value=800.0)
age = st.number_input("Age (days)", min_value=1, value=28)

# Predict Button
if st.button("Predict Strength"):
    input_data = pd.DataFrame([{
        "Cement": cement,
        "Blast Furnace Slag": slag,
        "Fly Ash": flyash,
        "Water": water,
        "Superplasticizer": superplasticizer,
        "Coarse Aggregate": coarseagg,
        "Fine Aggregate": fineagg,
        "Age": age
    }])

    prediction = model.predict(input_data)[0]
    strength_category = classify_strength_category(prediction)

    st.success(f"Predicted Compressive Strength: {prediction:.2f} MPa")
    st.write(f"**Strength Category:** {emoji_map[strength_category]} {strength_category}")

    # Pie chart visualization
    categories = ['Low Strength', 'Medium Strength', 'High Strength', 'Ultra-high Strength']
    values = [0, 0, 0, 0]

    if strength_category in categories:
        index = categories.index(strength_category)
        values[index] = 1
    else:
        st.error(f"Unexpected strength category: {strength_category}")

    fig, ax = plt.subplots()
    ax.pie(
        values,
        labels=categories,
        autopct=lambda p: f'{p:.0f}%' if p > 0 else '',
        startangle=90,
        colors=['#FF9999', '#FFCC99', '#99FF99', '#66B2FF']
    )
    ax.axis('equal')
    st.subheader("Strength Category Visualization")
    st.pyplot(fig)
