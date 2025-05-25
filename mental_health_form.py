import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Mental Health Detector", layout="centered")
st.title("🧠 Mental Health Self-Assessment Form")

# Your input form here (same as before)...
name = st.text_input("Full Name (Required)")
if not name.strip():
    st.warning("⚠️ Please enter your name to continue.")
    st.stop()

email = st.text_input("Email or Contact Number (Optional)")
age = st.number_input("Age", min_value=10, max_value=100, step=1)
gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Other"])
relationship = st.selectbox("Relationship Status", ["Single", "In a relationship", "Married", "Divorced", "Widowed"])
smoking = st.selectbox("Do you smoke?", ["No", "Yes", "Occasionally"])
alcohol = st.selectbox("Do you consume alcohol?", ["No", "Yes", "Occasionally"])

# Symptom ratings
anxiety = st.slider("Anxiety (nervousness, fear, racing thoughts)", 0, 10, 0)
mood = st.slider("Mood Swings (rapid or extreme emotional changes)", 0, 10, 0)
fatigue = st.slider("Fatigue (constant tiredness, low energy)", 0, 10, 0)
sleep = st.slider("Sleep Issues (insomnia, oversleeping, poor quality sleep)", 0, 10, 0)
adhd = st.slider("ADHD-like Symptoms (difficulty focusing, restlessness, impulsivity)", 0, 10, 0)
stress = st.slider("Stress (feeling overwhelmed, pressured)", 0, 10, 0)
sweaty = st.slider("Sweaty Palms During Nervousness", 0, 10, 0)

if st.button("🧠 Submit and Predict"):
    # Diagnosis logic...

    # Save data
    data = {
        "Name": name,
        "Email/Contact": email,
        "Age": age,
        "Gender": gender,
        "Relationship Status": relationship,
        "Smoking": smoking,
        "Alcohol": alcohol,
        "Anxiety": anxiety,
        "Mood Swings": mood,
        "Fatigue": fatigue,
        "Sleep Issues": sleep,
        "ADHD": adhd,
        "Stress": stress,
        "Sweaty Palms": sweaty,
    }

    df_new = pd.DataFrame([data])
    csv_file = "responses.csv"

    if os.path.exists(csv_file):
        df_existing = pd.read_csv(csv_file)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(csv_file, index=False)
    else:
        df_new.to_csv(csv_file, index=False)

    st.success("Thank you for submitting your responses!")


