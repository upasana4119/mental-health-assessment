import streamlit as st
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="Mental Health Detector", layout="centered")
st.title("🧠 Mental Health Self-Assessment Form")

st.markdown("Please fill in your basic information and rate your mental health symptoms honestly.")

st.markdown("""
> **🔒 Privacy Notice:**  
> Your responses will remain completely **anonymous** and will only be used for general analysis purposes.  
> No personally identifiable information will be shown, shared, or made public.  
> You **must enter your name** to proceed, but it will not appear in your result.
""")

# User Info
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

st.markdown("---")
st.subheader("🧾 Symptom Rating (0 = None, 10 = Extreme)")

# Sliders with descriptions
anxiety = st.slider("Anxiety (nervousness, fear, racing thoughts)", 0, 10, 0)
mood = st.slider("Mood Swings (rapid or extreme emotional changes)", 0, 10, 0)
fatigue = st.slider("Fatigue (constant tiredness, low energy)", 0, 10, 0)
sleep = st.slider("Sleep Issues (insomnia, oversleeping, poor quality sleep)", 0, 10, 0)
adhd = st.slider("ADHD-like Symptoms (difficulty focusing, restlessness, impulsivity)", 0, 10, 0)
stress = st.slider("Stress (feeling overwhelmed, pressured)", 0, 10, 0)
sweaty = st.slider("Sweaty Palms During Nervousness", 0, 10, 0)

# Submit button
if st.button("🧠 Submit and Predict"):

    # Assessment logic
    diagnosis = []
    if anxiety > 6 and stress > 6 and sweaty > 6:
        diagnosis.append("signs of Anxiety Disorder")
    if mood > 6 and fatigue > 6 and sleep > 6:
        diagnosis.append("possible Depression or Mood Instability")
    if adhd > 6 and mood > 5:
        diagnosis.append("symptoms of ADHD or Attention Dysregulation")
    if fatigue > 6 and sleep > 6 and stress > 6:
        diagnosis.append("likely Burnout or Chronic Stress")

    # Paragraph-style result summary
    if diagnosis:
        final_result = (
            "Based on the symptoms you've rated, your responses indicate potential concerns such as "
            + ", and ".join(diagnosis) +
            ". This suggests you may be facing emotional or psychological challenges that could be impacting your daily life, "
            "energy levels, or emotional well-being. You're not alone—many people experience similar challenges, "
            "and seeking support is a proactive and positive step. \n\n"
            "It’s recommended to consult with a licensed mental health professional for a full evaluation. "
            "Meanwhile, self-care practices like regular sleep, physical activity, open communication, and mindfulness can help. \n\n"
            "Please remember, this tool is a self-check and **not a medical diagnosis**—its purpose is to guide awareness and self-care."
        )
    else:
        final_result = (
            "Your responses suggest no strong signs of common mental health disorders at this time. "
            "This indicates a generally stable emotional and mental state, which is a great sign. \n\n"
            "Still, mental well-being can fluctuate. Regular check-ins, healthy lifestyle habits, and talking to someone you trust "
            "can help maintain emotional resilience. If things ever feel overwhelming, reaching out is always a good idea."
        )

    # Display result only (no personal info)
    st.markdown("---")
    st.subheader("📝 Mental Health Summary")
    st.markdown(final_result)

    st.markdown("---")
    st.info("⚠️ This tool offers a general overview and is not a substitute for medical advice. For an official diagnosis, consult a mental health professional.")

    # Credit note
    st.markdown("<br><hr><center><sub>This mental health self-assessment was created by <strong>Upasana Awasthi</strong>.</sub></center>", unsafe_allow_html=True)

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
    df_combined = df_new.copy()  # ✅ Ensure df_combined is defined

import io

# Convert the DataFrame to CSV in memory
csv_buffer = io.StringIO()
df_combined.to_csv(csv_buffer, index=False)
csv_bytes = io.BytesIO(csv_buffer.getvalue().encode("utf-8"))

# Streamlit download button
st.download_button(
    label="📥 Download My Response Record (Admin Only)",
    data=csv_bytes,
    file_name="responses.csv",
    mime="text/csv"
)

st.markdown("---")
st.subheader("🔐 Admin Panel (Restricted Access)")

admin_password = st.text_input("Enter admin password to access data:", type="password")

if admin_password == "YourSecurePasswordHere":  # Replace with your own password
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
