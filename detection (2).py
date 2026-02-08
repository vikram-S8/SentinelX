import cv2, time, json, os, winsound, pyttsx3, requests
from datetime import datetime
from threading import Thread
from ultralytics import YOLO

# ================= CONFIG =================
MODEL_PATH = "assets/best.pt"
VIDEO_SOURCE = 0
LIVE_FEED = "assets/live_feed.jpg"
LOG_FILE = "violations_log.json"

BOT_TOKEN = "YOUR BOT TOKEN" # replace with your bot token
CHAT_ID = "YOUR BOT CHAT ID"  # replace with your chat ID

START_FRAMES = 5
END_FRAMES = 5
# =========================================

os.makedirs("assets", exist_ok=True)

model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(VIDEO_SOURCE)
engine = pyttsx3.init()

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

# ===== STATE =====
violation_active = False
current_violation = None
violation_frame_count = 0
no_violation_frame_count = 0
# =================

def log_event(event, status):
    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    data.append({
        "event": event,
        "status": status,
        "location": "Zone A",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(LOG_FILE, "w") as f:
        json.dump(data[-200:], f, indent=2)

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload, timeout=5)

def alert(event, status):
    try:
        winsound.Beep(1200, 500)
    except:
        pass

    engine.say(f"{event} {status}")
    engine.runAndWait()

    send_telegram_alert(
        f"🚨 SAFETY VIOLATION {status}\n"
        f"Violation: {event}\n"
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

send_telegram_alert("✅ SentinelX started successfully")
print("✅ Detection running (Helmet + Vest fixed)")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    results = model(frame, verbose=False)
    annotated = results[0].plot()

    detected_violation = None

    helmet_violation = False
    vest_violation = False

    if results[0].boxes is not None and len(results[0].boxes.cls) > 0:
        class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
        classes = [model.names[c] for c in class_ids]

        for cls in classes:
            cls_lower = cls.lower()

            if "helmet" in cls_lower and "no" in cls_lower:
                helmet_violation = True

            if "vest" in cls_lower and "no" in cls_lower:
                vest_violation = True

    # 🎯 PRIORITY DECISION
    if helmet_violation:
        detected_violation = "No Helmet"
    elif vest_violation:
        detected_violation = "No Vest"

    # ===== FRAME STABILITY =====
    if detected_violation:
        violation_frame_count += 1
        no_violation_frame_count = 0
    else:
        no_violation_frame_count += 1
        violation_frame_count = 0

    # 🔴 START
    if violation_frame_count >= START_FRAMES and not violation_active:
        violation_active = True
        current_violation = detected_violation
        violation_frame_count = 0

        Thread(
            target=alert,
            args=(current_violation, "START"),
            daemon=True
        ).start()

        log_event(current_violation, "START")

    # 🟢 END
    if no_violation_frame_count >= END_FRAMES and violation_active:
        Thread(
            target=alert,
            args=(current_violation, "END"),
            daemon=True
        ).start()

        log_event(current_violation, "END")

        violation_active = False
        current_violation = None
        no_violation_frame_count = 0

    cv2.imwrite(LIVE_FEED, annotated)
    cv2.imshow("SentinelX Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

