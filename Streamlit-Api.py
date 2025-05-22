import streamlit as st
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from PIL import Image

# Load model
model = joblib.load("concrete_xgb_model.pkl")

# Load and display logo
logo = Image.open("Drisa_Logo.jpg")
st.image(logo, width=100)

# Strength classification
emoji_map = {
    "Low Strength": "🔴",
    "Medium Strength": "🟠",
    "High Strength": "🟢",
    "Ultra-high Strength": "🔵"
}

def classify_strength_category(strength_value):
    if strength_value < 30:
        return 'Low Strength'
    elif 30 <= strength_value < 60:
        return 'Medium Strength'
    elif 60 <= strength_value < 100:
        return 'High Strength'
    else:
        return 'Ultra-high Strength'

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("Concrete Compressive Strength Prediction With AI")

# Input Form
with st.form("input_form"):
    cement = st.number_input("Cement (kg/m³)", min_value=0.0, step=1.0)
    slag = st.number_input("Blast Furnace Slag (kg/m³)", min_value=0.0, step=1.0)
    fly_ash = st.number_input("Fly Ash (kg/m³)", min_value=0.0, step=1.0)
    water = st.number_input("Water (kg/m³)", min_value=0.0, step=1.0)
    superplasticizer = st.number_input("Superplasticizer (kg/m³)", min_value=0.0, step=1.0)
    coarse_agg = st.number_input("Coarse Aggregate (kg/m³)", min_value=0.0, step=1.0)
    fine_agg = st.number_input("Fine Aggregate (kg/m³)", min_value=0.0, step=1.0)
    age = st.number_input("Age (days)", min_value=1, step=1)
    
    submit = st.form_submit_button("Predict")
    reset = st.form_submit_button("Reset Input")

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
    strength_category = classify_strength_category(prediction)

    st.success(f"Predicted Compressive Strength: {prediction:.2f} MPa")
    st.write(f"**Strength Category:** {emoji_map[strength_category]} {strength_category}")

    categories = list(emoji_map.keys())
    values = [1 if strength_category == cat else 0 for cat in categories]

    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct=lambda p: f'{p:.0f}%' if p > 0 else '',
           startangle=90, colors=['#FF9999','#FFCC99','#99FF99','#66B2FF'])
    ax.axis('equal')
    st.pyplot(fig)

    # Append to history
    st.session_state.history.append({
        "Cement": cement,
        "Slag": slag,
        "Fly Ash": fly_ash,
        "Water": water,
        "Superplasticizer": superplasticizer,
        "Coarse Agg": coarse_agg,
        "Fine Agg": fine_agg,
        "Age": age,
        "Strength (MPa)": round(prediction, 2),
        "Category": strength_category
    })

if reset:
    st.experimental_rerun()

# Upload for bulk prediction
st.markdown("---")
st.subheader("Bulk Prediction via CSV Upload")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        batch_df = pd.read_csv(uploaded_file)
        batch_predictions = model.predict(batch_df)

        batch_df['Predicted_Strength'] = batch_predictions
        batch_df['Strength_Category'] = [classify_strength_category(val) for val in batch_predictions]

        st.write("### Prediction Results")
        st.dataframe(batch_df)

        csv = batch_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results as CSV", csv, "predictions.csv", "text/csv")
