# run_all.py
import subprocess
import sys
import time
import signal
import os

print("🚀 Starting SentinelX AI Safety System...\n")

processes = []

try:
    # 1️⃣ Start Detection (includes alerts)
    print("▶ Starting Detection Engine (PPE + Restricted Zone + Alerts)...")
    det_process = subprocess.Popen(
        [sys.executable, "detection (2).py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    processes.append(det_process)

    # Allow detection to initialize camera/video
    time.sleep(4)

    # 2️⃣ Start Streamlit Dashboard
    print("▶ Starting Smart Dashboard...")
    dash_process = subprocess.Popen(
        ["streamlit", "run", "dashboard (2).py"],
        shell=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    processes.append(dash_process)

    print("\n✅ SentinelX is LIVE!")
    print("📊 Dashboard → http://localhost:8501")
    print("🚨 Alerts → Telegram + Buzzer")
    print("❌ Press CTRL+C here to stop EVERYTHING.\n")

    # Wait forever
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Shutting down SentinelX...")

    for p in processes:
        try:
            p.terminate()
        except Exception:
            pass

    print("✅ Detection stopped")
    print("✅ Dashboard stopped")
    print("🔒 SentinelX shutdown complete")
