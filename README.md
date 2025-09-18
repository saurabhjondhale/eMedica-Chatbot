⚠️ Disclaimer: This chatbot should not replace professional medical advice.

# 🏥 eMedica Health Chat Bot
eMedica-Health-Chat-Bot/
│── app.py                  # Main Streamlit app
│── requirements.txt        # Python dependencies
│── README.md               # Project overview
│── .gitignore              # Ignore sensitive files
│── example.env             # Safe template for environment variables
│── /data/                  # Datasets (ignored in .gitignore)
│── /models/                # Trained/fine-tuned models (ignored)
│── /generated_reports/     # AI-generated outputs (ignored)
│── /uploaded_reports/      # Uploaded PDFs (ignored)
│── /notebooks/             # For Kaggle/colab experiments
│── /utils/                 # Helper scripts (e.g., preprocessing, database)


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
pip install -r requirements.txt


OPENAI_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///patients.db
