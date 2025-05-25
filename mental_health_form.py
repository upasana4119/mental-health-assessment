import streamlit as st
import pandas as pd
import os

# (Same setup and user form as before...)

# Submit button
if st.button("🧠 Submit and Predict"):

    # (Assessment logic and result display...)

    # Save responses silently to CSV
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
        "Assessment Result": final_result
    }

    df_new = pd.DataFrame([data])
    csv_file = "responses.csv"

    if os.path.exists(csv_file):
        df_existing = pd.read_csv(csv_file)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(csv_file, index=False)
    else:
        df_new.to_csv(csv_file, index=False)

# --------- ADMIN PANEL ONLY ---------

st.markdown("---")
st.subheader("🔐 Admin Panel (Restricted Access)")

admin_password = st.text_input("Enter admin password to access data:", type="password")

if admin_password == "il060509pr":  # Replace with your password
    if os.path.exists("responses.csv"):
        with open("responses.csv", "rb") as file:
            st.download_button(
                label="📥 Download All User Responses (CSV)",
                data=file,
                file_name="responses.csv",
                mime="text/csv"
            )
    else:
        st.warning("No data file found.")
elif admin_password:
    st.error("❌ Incorrect password.")
