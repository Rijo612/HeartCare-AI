import streamlit as st
import numpy as np
import pandas as pd
import joblib
import plotly.graph_objects as go

# ==========================
# Load Model
# ==========================

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# ==========================
# Page Config
# ==========================

st.set_page_config(
    page_title="HeartCare AI",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# Load CSS
# ==========================

def load_css():
    try:
        with open("style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except:
        pass

load_css()

# ==========================
# Session State
# ==========================

if "history" not in st.session_state:
    st.session_state.history = []

# ==========================
# Sidebar
# ==========================

st.sidebar.image(
    "https://img.icons8.com/color/96/heart-with-pulse.png",
    width=90
)

st.sidebar.title("❤️ HeartCare AI")

st.sidebar.markdown("---")

st.sidebar.success("""
### 🤖 AI Heart Disease Prediction

✔ Random Forest Model

✔ Machine Learning

✔ Accuracy: 98.54%

✔ Streamlit Dashboard
""")

st.sidebar.markdown("---")

st.sidebar.info("""
### About

This application predicts heart disease using Machine Learning.

Developed using:

• Python

• Streamlit

• Scikit-Learn

• Plotly
""")

# ==========================
# Header
# ==========================

st.title("❤️ HeartCare AI")

st.markdown("""
## AI Powered Heart Disease Prediction Dashboard

Predict the possibility of heart disease using Artificial Intelligence.
""")

st.info("""
Enter the patient's information and click **Predict Heart Disease**.
""")

# ==========================
# Dashboard Cards
# ==========================

card1, card2, card3, card4 = st.columns(4)

with card1:
    st.metric(
        "🤖 Model",
        "Random Forest"
    )

with card2:
    st.metric(
        "🎯 Accuracy",
        "98.54%"
    )

with card3:
    st.metric(
        "❤️ Prediction",
        "Binary"
    )

with card4:
    st.metric(
        "⚡ Status",
        "Ready"
    )

st.markdown("---")

# ==========================
# Main Layout
# ==========================

left, right = st.columns([2,1])

# ==========================
# Left Panel
# ==========================

with left:

    st.subheader("👤 Patient Information")

    st.caption("Fill all patient details carefully.")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=30
        )

        sex = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        cp = st.selectbox(
            "Chest Pain Type",
            [0,1,2,3]
        )

        trestbps = st.number_input(
            "Resting Blood Pressure",
            min_value=80,
            max_value=250,
            value=120
        )

        chol = st.number_input(
            "Cholesterol",
            min_value=100,
            max_value=600,
            value=200
        )

        fbs = st.selectbox(
            "Fasting Blood Sugar",
            [0,1]
        )

        restecg = st.selectbox(
            "Resting ECG",
            [0,1,2]
        )

    with col2:

        thalach = st.number_input(
            "Maximum Heart Rate",
            min_value=50,
            max_value=250,
            value=150
        )

        exang = st.selectbox(
            "Exercise Induced Angina",
            [0,1]
        )

        oldpeak = st.number_input(
            "Old Peak",
            min_value=0.0,
            max_value=10.0,
            value=1.0
        )

        slope = st.selectbox(
            "Slope",
            [0,1,2]
        )

        ca = st.selectbox(
            "Major Vessels",
            [0,1,2,3,4]
        )

        thal = st.selectbox(
            "Thal",
            [0,1,2,3]
        )

        height = st.number_input(
            "Height (cm)",
            100,
            250,
            170
        )

        weight = st.number_input(
            "Weight (kg)",
            20,
            200,
            70
        )

    bmi = weight / ((height/100)**2)

    st.metric(
        "🧮 BMI",
        f"{bmi:.1f}"
    )

    if bmi < 18.5:
        st.info("BMI Category : Underweight")
    elif bmi < 25:
        st.success("BMI Category : Normal")
    elif bmi < 30:
        st.warning("BMI Category : Overweight")
    else:
        st.error("BMI Category : Obese")

    predict = st.button(
        "❤️ Predict Heart Disease",
        use_container_width=True
    )

# ==========================
# Right Panel (Placeholder)
# ==========================

with right:

    st.subheader("📊 Prediction Result")

    if predict:

        # Convert Gender
        sex_value = 1 if sex == "Male" else 0

        # Prepare input
        input_data = np.array([[
            age,
            sex_value,
            cp,
            trestbps,
            chol,
            fbs,
            restecg,
            thalach,
            exang,
            oldpeak,
            slope,
            ca,
            thal
        ]])

        # Scale input
        input_scaled = scaler.transform(input_data)

        # Predict
        prediction = model.predict(input_scaled)

        probability = model.predict_proba(input_scaled)

        confidence = np.max(probability) * 100

        # Result
        if prediction[0] == 1:
            st.error("🔴 High Risk of Heart Disease")
        else:
            st.success("🟢 Low Risk of Heart Disease")

        # Confidence
        st.metric("Prediction Confidence", f"{confidence:.2f}%")

        st.progress(confidence / 100)

        # Probability Chart
        st.subheader("📊 Risk Probability")

        low_risk = probability[0][0] * 100
        high_risk = probability[0][1] * 100

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=["Low Risk", "High Risk"],
                    values=[low_risk, high_risk],
                    hole=0.55
                )
            ]
        )

        fig.update_layout(height=350)

        st.plotly_chart(fig, use_container_width=True)

        # Health Score
        health_score = confidence if prediction[0] == 0 else (100 - confidence)

        st.metric("❤️ Health Score", f"{health_score:.0f}/100")

        # Risk Factors
        st.subheader("⚠ Risk Factors")

        risk = []

        if age > 55:
            risk.append("Age above 55")

        if trestbps > 140:
            risk.append("High Blood Pressure")

        if chol > 240:
            risk.append("High Cholesterol")

        if exang == 1:
            risk.append("Exercise Induced Angina")

        if len(risk) == 0:
            st.success("No major risk factors detected.")
        else:
            for item in risk:
                st.write("•", item)

        # Recommendations
        st.subheader("💡 Recommendations")

        if prediction[0] == 1:
            st.warning("""
- 🩺 Consult a cardiologist.
- 🥗 Follow a heart-healthy diet.
- 🚶 Exercise regularly.
- 🚭 Avoid smoking and alcohol.
- ❤️ Monitor blood pressure and cholesterol.
""")
        else:
            st.success("""
- ✅ Maintain a healthy lifestyle.
- 🥗 Eat balanced meals.
- 🏃 Exercise regularly.
- 😴 Get enough sleep.
- 🩺 Have regular health checkups.
""")

    else:
        st.info("👈 Enter patient details and click **Predict Heart Disease**.")
# ==========================
# Prediction History
# ==========================

st.markdown("---")
st.subheader("📜 Prediction History")

if st.session_state.history:

    history_df = pd.DataFrame(st.session_state.history)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    if st.button("🗑 Clear History"):
        st.session_state.history = []
        st.rerun()

else:
    st.info("No predictions made yet.")

# ==========================
# Daily Health Tip
# ==========================

tips = [
    "🥗 Eat more fruits and vegetables.",
    "🏃 Exercise at least 30 minutes every day.",
    "💧 Drink 2-3 litres of water daily.",
    "😴 Sleep at least 7-8 hours.",
    "🚭 Avoid smoking and alcohol.",
    "🩺 Schedule regular health checkups.",
    "❤️ Reduce stress with meditation or yoga.",
    "🥜 Choose healthy fats instead of saturated fats."
]

st.markdown("---")

st.subheader("💡 Daily Health Tip")

st.info(np.random.choice(tips))

# ==========================
# Learn About Features
# ==========================

st.markdown("---")

st.subheader("📖 Learn About Heart Disease Features")

with st.expander("🫀 Chest Pain Type (cp)"):

    st.write("""
0 → Typical Angina

1 → Atypical Angina

2 → Non-anginal Pain

3 → Asymptomatic
""")

with st.expander("🩸 Cholesterol"):

    st.write("""
Serum Cholesterol level measured in mg/dl.

Higher values increase the risk of heart disease.
""")

with st.expander("❤️ Resting Blood Pressure"):

    st.write("""
Blood pressure while resting.

Normal:
90 - 120 mm Hg
""")

with st.expander("🏃 Maximum Heart Rate"):

    st.write("""
Maximum heart rate achieved during exercise.
""")

with st.expander("💪 Exercise Induced Angina"):

    st.write("""
Chest pain caused by physical activity.
""")

with st.expander("🧮 BMI"):

    st.write("""
BMI Categories

Underweight : <18.5

Normal : 18.5 - 24.9

Overweight : 25 - 29.9

Obese : ≥30
""")

# ==========================
# Model Information
# ==========================

st.markdown("---")

st.subheader("🤖 Machine Learning Model")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Algorithm",
        "Random Forest"
    )

with col2:
    st.metric(
        "Features",
        "13"
    )

with col3:
    st.metric(
        "Accuracy",
        "98.54%"
    )

# ==========================
# Medical Disclaimer
# ==========================

st.markdown("---")

st.warning("""
### ⚠ Medical Disclaimer

This application is developed for educational purposes.

It should NOT be used as a replacement for professional medical diagnosis.

Always consult a qualified healthcare professional before making medical decisions.
""")

# ==========================
# Footer
# ==========================

st.markdown("---")

st.markdown("""
<div style='text-align:center;'>

<h2>❤️ HeartCare AI</h2>

<h4>AI Powered Heart Disease Prediction System</h4>

Developed by <b>Rijo Thomas</b>

Python | Streamlit | Scikit-Learn | Plotly

© 2026 HeartCare AI

</div>
""", unsafe_allow_html=True)