# Concrete-Compressive-Strength-PredictConcrete-Compressive-Strength-Predictor
# Smart Concrete Strength Predictor

**Predict the compressive strength of concrete using AI.**  
An intelligent regression-based web app powered by machine learning models trained on real-world data from the [UCI Concrete Compressive Strength Dataset](https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength).

---

## Overview

Concrete's compressive strength is a vital metric in civil engineering and infrastructure development. However, traditional testing methods are time-consuming and costly. This project offers a smarter alternative—leveraging machine learning to predict concrete strength based on mix proportions and curing age.

Using 1,030 experimental records containing 8 input variables (cement, slag, fly ash, water, superplasticizer, coarse and fine aggregates, and age in days), the app delivers quick, accurate predictions. Models implemented include:

- Linear Regression  
- Random Forest Regressor  
- XGBoost Regressor (Best Performing Model)

---

## Demo

![Demo Screenshot](Concrete-Compressive-Strength-Predictor/inages/demo1.jpg)- Replace with your actual screenshot path -->
![Demo Screenshot](Concrete-Compressive-Strength-Predictor/images/demo.jpg)-

---

## Features

- Predict concrete strength (MPa) from user-defined mix designs
- Feature importance visualization using XGBoost
- Strength category pie chart (Low, Medium, High)
- Interactive Streamlit web interface
- Model trained and tested on clean, real-world dataset

---

## Dataset

- Source: [UCI Machine Learning Repository – Concrete Compressive Strength](https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength)
- 1,030 samples, no missing values
- Input Features:
  - Cement, Slag, Fly Ash, Water, Superplasticizer, Coarse Aggregate, Fine Aggregate, Age
- Target Variable:
  - Concrete compressive strength (MPa)

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/concrete-strength-predictor.git
cd concrete-strength-predictor

## Create and activate virtual environment (optional but recommende)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

## Install dependencies

pip install -r requirements.txt

Or manually install:

pip install streamlit pandas scikit-learn xgboost matplotlib seaborn joblib

## Run the Streamlit app

streamlit run app.py

## Usage

1. Open the app in your browser (usually http://localhost:8501)


2. Enter the values for each input feature


3. Click "Predict Strength"


4. View:

Predicted compressive strength in MPa

Strength category (Low, Medium, High)

Pie chart visualization

## Strength Categories

Low: < 20 MPa

Medium: 20–40 MPa

High: > 40 MPa

## Project Structure

├── app.py                  # Streamlit app
├── train_model.ipynb       # Colab notebook for model training & evaluation
├── concrete_xgb_model.pkl  # Trained model file
├── requirements.txt
├── README.md
└── images/
    └── demo

Example Input & Output (Optional but Helpful)

## Example

**Input:**

- Cement: 400 kg/m³  
- Water: 200 kg/m³  
- Fly Ash: 100 kg/m³  
- Age: 28 days  
*(...other values)*

**Predicted Output:**  
- **Strength:** 38.56 MPa  
- **Category:** Medium Strength

2. Model Performance Summary

## Model Performance (Test Set)

| Model             | R² Score | RMSE (MPa) |
|------------------|----------|------------|
| Linear Regression| 0.62     | 10.85      |
| Random Forest     | 0.88     | 6.15       |
| XGBoost (Best)    | 0.91     | 5.42       |

3. Contributing (Optional for GitHub)

## Contributing

Contributions are welcome! Feel free to fork this repo and submit pull requests. For major changes, please open an issue first to discuss what you’d like to improve.

## Rquirements.txt

To match the app, create a requirements.txt file:

streamlit
pandas
numpy
scikit-learn
xgboost
matplotlib
seaborn
joblib
