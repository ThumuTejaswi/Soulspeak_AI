💙 SoulSpeak AI
A simple text-based emotional support system that detects basic emotions from user input and provides comforting responses.

🚀 Features (Only what is done now)
Accepts text input from the user
Detects emotions using:
Simple keyword-based emotion detection
Hugging Face Transformers model (emotion-english-distilroberta-base)
Provides supportive and empathetic responses
Two working versions:
Streamlit App
Flask App (with HTML & CSS)

📁 Project Structure (Current)
SoulSpeak_AI/
│
├── app_streamlit.py        # Streamlit version
├── app.py                  # Flask backend
├── templates/
│   └── index.html          # HTML UI
├── static/
│   └── style.css           # CSS styling
└── requirements.txt

🧠 Emotion Detection (What is implemented)
✔ Keyword-based detection
✔ Hugging Face model for text emotion classification
✔ Supports emotions like:
joy
sadness
anger
fear
disgust
surprise

🖥️ How to Run (Basic Instructions)

Streamlit
pip install -r requirements.txt
streamlit run app_streamlit.py

Flask
pip install -r requirements.txt
python app.py

💙 Status
This is a basic working version of SoulSpeak AI that currently supports only text-based emotional responses.
