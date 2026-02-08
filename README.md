🧠 SentinelX – AI-Powered Smart Factory Safety System

SentinelX is a real-time AI-based industrial safety monitoring system that detects PPE violations and restricted zone intrusions using computer vision, and provides instant alerts with a live monitoring dashboard.

“Because safety should be automatic, not optional.”

🚀 Key Features

🎥 Real-time PPE Detection

Detects No Helmet, No Safety Vest

🚷 Restricted Zone Monitoring

Alerts when workers enter unsafe areas

🔔 Instant Alerts

Buzzer sound

Voice warning

Telegram alert notification

📊 Live Monitoring Dashboard

Live video feed

Violation counters

Recent violation logs

🧾 Violation Logging

Timestamped JSON-based logs

⚙ Plug & Play

Works with existing CCTV / webcam

🌐 Offline Detection + Online Alerts

🏗 System Architecture
Camera / Video Feed
        ↓
AI Detection Engine (YOLO)
        ↓
Violation Analysis
        ↓
├── Buzzer + Voice Alert
├── Telegram Alert
├── Violation Logs (JSON)
└── Streamlit Dashboard (Live View)

🛠 Tech Stack

Programming Language: Python 3.9+

AI Model: YOLO (Ultralytics)

Computer Vision: OpenCV

Dashboard: Streamlit

Alerts: Telegram Bot API

Data Storage: JSON

OS: Windows / Linux

📂 Project Structure
SentinelX/
│
├── detection.py            # AI detection & alert engine
├── dashboard.py            # Live monitoring dashboard
├── run_all.py              # Run detection + dashboard together
│
├── assets/
│   ├── best.pt              # Trained YOLO model
│   ├── live_feed.jpg        # Live frame for dashboard
│   └── restricted_zone.json #Generates anutomatically
│
└── README.md

⚙ Installation
1️⃣ Clone the Repository
git clone https://github.com/vikram-S8/SentinelX.git
cd SentinelX

2️⃣ Install Dependencies
pip install ultralytics opencv-python streamlit pandas numpy requests pyttsx3

▶ How to Run
Option 1: Run Everything Together (Recommended)
python run_all.py

Option 2: Run Separately

Detection Engine

python detection.py


Dashboard

streamlit run dashboard.py


Open dashboard at:

http://localhost:8501

📱 Telegram Alert Setup

Create a bot using @BotFather

Get your Bot Token

Get your Chat ID

Add them to telegram_alerts.py

Example:

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

📊 Dashboard Capabilities

Live AI video feed

Total violations count

PPE violations count

Restricted zone entries

Recent violation table

Auto-refresh control

🌟 Unique Innovation Highlights

No wearable devices required

Works with existing surveillance

Offline AI processing

Multi-alert system (sound + voice + Telegram)

Lightweight & scalable

Industry-ready prototype

🔮 Future Enhancements

Multi-camera support

Heatmap of unsafe zones

Cloud-based analytics

Face recognition for worker ID

Mobile dashboard app

Predictive safety risk analysis

👨‍💻 Team & Credits

Developed by VIKRAM - NexaVerse
Domain: AI | Computer Vision | Industrial Safety | Cyber-Physical Systems

📜 License

This project is developed for academic, innovation, and demonstration purposes.