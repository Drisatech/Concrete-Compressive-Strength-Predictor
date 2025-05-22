# app.py
import streamlit as st
import numpy as np
import joblib

def classify_strength_category(strength_value):
    if strength_value < 30:
        return 'Low Strength'
    elif 30 <= strength_value < 60:
        return 'Medium Strength'
    elif 60 <= strength_value < 100:
        return 'High Strength'
    else:
        return 'Ultra-high Strength'

# Load trained model
model = joblib.load('concrete_xgb_model.pkl')  # path should be correct

# App Title
st.title("Concrete Compressive Strength Prediction")
st.subheader("Enter the mixture composition and age to predict strength (MPa)")

# Input Fields
cement = st.number_input("Cement (kg/m³)", min_value=0.0)
slag = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0)
fly_ash = st.number_input("Fly Ash (kg/m³)", min_value=0.0)
water = st.number_input("Water (kg/m³)", min_value=0.0)
superplasticizer = st.number_input("Superplasticizer (kg/m³)", min_value=0.0)
coarse_agg = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0)
fine_agg = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0)
age = st.number_input("Age (days)", min_value=1, max_value=365)

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

    # Predict strength
    prediction = model.predict(input_data)[0]
    strength_category = classify_strength_category(prediction)

    st.success(f"Predicted Compressive Strength: {prediction:.2f} MPa")
    st.info(f"Strength Category: **{strength_category}**")

    # Visualization: Pie chart for strength distribution
    categories = ['Low Strength', 'Medium Strength', 'High Strength', 'Ultra-high Strength']
    values = [0, 0, 0, 0]
    idx = categories.index(strength_category)
    values[idx] = 1

    st.subheader("Strength Category Distribution")
    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct=lambda p: f'{p:.1f}%' if p > 0 else '', startangle=90, colors=['#FF9999','#FFCC99','#99FF99','#66B2FF'])
    ax.axis('equal')
    st.pyplot(fig)

color_map = {
    "Low Strength": "red",
    "Medium Strength": "orange",
    "High Strength": "green",
    "Ultra-high Strength": "blue"
}
st.markdown(f"<h4 style='color:{color_map[strength_category]}'>{strength_category}</h4>", unsafe_allow_html=True)
