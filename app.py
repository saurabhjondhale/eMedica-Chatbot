import streamlit as st
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# --- Load Model ---
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained(
    "/home/heritage-foundation/eMedica/ocr/finetuned/gpt2_finetuned"
)

def generate_report(prompt, max_length=500):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        do_sample=True,
        top_p=0.9,
        temperature=0.7
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# --- Database Setup ---
Base = declarative_base()
engine = create_engine("sqlite:///emedica_reports.db")
Session = sessionmaker(bind=engine)
session = Session()

class PatientReport(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    patient_name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(10))
    symptoms = Column(Text)
    medical_history = Column(Text)
    lab_reports = Column(Text)
    question = Column(Text)
    model_output = Column(Text)
    pdf_file_path = Column(String(200))

Base.metadata.create_all(engine)

# --- UI Layout ---
st.set_page_config(page_title="eMedica Health Chatbot", page_icon="🩺", layout="wide")
st.title("🩺 eMedica Health Chatbot")
st.markdown("Fill in patient details, upload reports, and generate structured medical synopsis.")

# --- Sidebar Input Form ---
st.sidebar.header("📌 Patient Details")

patient_name = st.sidebar.text_input("Patient Name", key="patient_name")
age = st.sidebar.text_input("Age", key="age")
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"], key="gender")
symptoms = st.sidebar.text_area("Symptoms", key="symptoms")
medical_history = st.sidebar.text_area("Medical History", key="medical_history")
lab_reports = st.sidebar.text_area("Lab Reports", key="lab_reports")
question = st.sidebar.text_input(
    "Question",
    value="Provide medical treatment, diet plan, and workout recommendations.",
    key="question"
)

# File uploader (no manual assignment to session_state)
pdf_file = st.sidebar.file_uploader("Upload Medical Report PDF", type=["pdf"], key="pdf_file")

col_btn1, col_btn2 = st.sidebar.columns(2)
submitted = col_btn1.button("🚀 Generate Medical Report")
reset = col_btn2.button("🔄 Reset")

# --- Reset Functionality ---
if reset:
    for key in ["patient_name", "age", "gender", "symptoms",
                "medical_history", "lab_reports", "question"]:
        if key in st.session_state:
            st.session_state[key] = "" if key != "gender" else "Male"

    # Safely clear file_uploader
    st.session_state.pop("pdf_file", None)

    st.rerun()

# --- Main Area ---
if submitted:
    # Save uploaded PDF if any
    pdf_file_path = None
    if pdf_file is not None:
        upload_dir = "uploaded_reports"
        os.makedirs(upload_dir, exist_ok=True)
        pdf_file_path = os.path.join(upload_dir, pdf_file.name)
        with open(pdf_file_path, "wb") as f:
            f.write(pdf_file.read())

    # Prompt Template
    prompt = (
        f"Patient Name: {patient_name}\nAge: {age}\nGender: {gender}\n"
        f"Symptoms: {symptoms}\nMedical History: {medical_history}\n"
        f"Lab Reports: {lab_reports}\nQuestion: {question}\n\n"
        f"Answer in the following structure:\n"
        f"1. Medical Treatment (eMedica):\n2. Diet Plan:\n3. Workout Recommendations:\n"
    )

    with st.spinner("⚙️ Generating structured medical report..."):
        report = generate_report(prompt)

    st.success("✅ Report Generated Successfully!")

    # Display synopsis in detail
    st.subheader("📑 Detailed Synopsis")
    st.write(report)

    # Extract Sections
    sections = report.split("\n")
    treatment = next((line for line in sections if line.lower().startswith("1")), "Not found")
    diet = next((line for line in sections if line.lower().startswith("2")), "Not found")
    workout = next((line for line in sections if line.lower().startswith("3")), "Not found")

    # Action Buttons
    st.subheader("📊 Select Report Section")
    col1, col2, col3 = st.columns(3)
    if col1.button("💊 Medical Treatment"):
        st.info(treatment)
    if col2.button("🥗 Diet Plan"):
        st.success(diet)
    if col3.button("🏋️ Workout Recommendations"):
        st.warning(workout)

    # Save Structured Report to File
    output_dir = "generated_reports"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{patient_name.replace(' ', '_')}_{timestamp}.txt"
    output_file_path = os.path.join(output_dir, filename)

    with open(output_file_path, "w") as f:
        f.write("Patient Details & Synopsis\n")
        f.write("=" * 40 + "\n")
        f.write(f"Name: {patient_name}\nAge: {age}\nGender: {gender}\n")
        f.write(f"Symptoms: {symptoms}\nMedical History: {medical_history}\n")
        f.write(f"Lab Reports: {lab_reports}\n\n")
        f.write("Detailed Synopsis:\n")
        f.write(report)

    # Save to DB
    new_report = PatientReport(
        patient_name=patient_name,
        age=int(age) if age.isdigit() else None,
        gender=gender,
        symptoms=symptoms,
        medical_history=medical_history,
        lab_reports=lab_reports,
        question=question,
        model_output=report,
        pdf_file_path=pdf_file_path
    )
    session.add(new_report)
    session.commit()
    st.success("📄 Report saved to database & text file!")
