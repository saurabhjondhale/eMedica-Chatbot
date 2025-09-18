⚠️ Disclaimer: This chatbot should not replace professional medical advice.

An AI-powered medical chatbot that:
- Collects patient details (symptoms, history, reports).
- Analyzes conditions and generates structured medical synopses.
- Suggests **medical treatments**, **diet plans**, and **workout recommendations**.
- Saves patient details securely in the backend.
- Built with **Streamlit + Transformers**.

---

## 🚀 Features
- Upload medical reports (PDFs).
- Generate detailed medical synopsis.
- Personalized treatment, diet, and exercise recommendations.
- Reset and start fresh with one click.
- Secure backend storage (no sensitive data committed to GitHub).

---

## 📦 Installation
```bash
git clone https://github.com/<your-username>/eMedica-Health-Chat-Bot.git
cd eMedica-Health-Chat-Bot
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows


requiirements.txt
# Core
streamlit>=1.32.0
torch>=2.2.0
transformers>=4.40.0

# Database
sqlalchemy>=2.0.29

# Utilities
python-dotenv>=1.0.1

# PDF handling (if later needed for OCR/reading)
pypdf2>=3.0.1

# Optional (for extra text processing, if you expand)
pandas>=2.2.2

pip install -r requirements.txt


OPENAI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///patients.db
