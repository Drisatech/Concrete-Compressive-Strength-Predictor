# app.py
import streamlit as st
import numpy as np
import joblib

import joblib

#Load trained model
model = joblib.load('concrete_xgb_model.pkl')

def classify_strength_category(strength_value):
    if strength_value < 30:
        return 'Low Strength'
    elif 30 <= strength_value < 60:
        return 'Medium Strength'
    elif 60 <= strength_value < 100:
        return 'High Strength'
    else:
        return 'Ultra-high Strength'

# App Title
st.title("Concrete Compressive Strength Prediction With AI")
st.subheader("Enter the mixture composition and age to predict strength (MPa)")

# Construct input data
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

# Optional debug
st.write("Input Data:")
st.write(input_data)

# Predict
prediction = model.predict(input_data)[0]

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
    st.info(f"Strength Category: **{strength_category}**")

    categories = ['Low Strength', 'Medium Strength', 'High Strength', 'Ultra-high Strength']
    values = [0, 0, 0, 0]
    index = categories.index(strength_category)
    values[index] = 1

    fig, ax = plt.subplots()
    ax.pie(values, labels=categories, autopct=lambda p: f'{p:.0f}%' if p > 0 else '', startangle=90, colors=['#FF9999','#FFCC99','#99FF99','#66B2FF'])
    ax.axis('equal')
    st.pyplot(fig)

# After model prediction
prediction = model.predict(input_data)[0]
strength_category = classify_strength_category(prediction)

import streamlit as st

strength_category = "Medium Strength"

color_map = {
    "Low Strength": "red",
    "Medium Strength": "orange",
    "High Strength": "green",
    "Ultra-high Strength": "blue"
}

st.markdown(
    f"<h4 style='color:{color_map[strength_category]}'>{strength_category}</h4>",
    unsafe_allow_html=True
)
