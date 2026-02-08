# dashboard.py
import streamlit as st
import json, os, time
import pandas as pd

# ================= CONFIG =================
LOG_FILE = "violations_log.json"
VIOLATION_IMAGE = "assets/live_feed.jpg"
REFRESH_INTERVAL = 2
# =========================================

st.set_page_config(
    page_title="SentinelX Safety Dashboard",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 SentinelX – Safety Violation Dashboard")

# -------- Sidebar --------
st.sidebar.header("Dashboard Controls")
auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)

if st.sidebar.button("Manual Refresh"):
    st.rerun()

# -------- Load Logs --------
logs = []
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

df = pd.DataFrame(logs)

# -------- Only START events = real violations --------
violations_df = df[df["status"] == "START"] if not df.empty else pd.DataFrame()

# -------- Summary --------
st.subheader("📊 Violation Summary")

c1, c2 = st.columns(2)

with c1:
    st.metric("🚨 Total Violations", len(violations_df))

with c2:
    if not violations_df.empty:
        last = violations_df.iloc[-1]
        st.metric(
            "📝 Latest Violation",
            f"{last['event']} @ {last['timestamp']}"
        )
    else:
        st.metric("📝 Latest Violation", "No violations")

# -------- SAFE IMAGE LOADING (NO STREAMLIT FILE ACCESS) --------
st.subheader("📸 Latest Violation Screenshot")

if "last_image_bytes" not in st.session_state:
    st.session_state.last_image_bytes = None

def load_image_bytes(path, retries=3, delay=0.1):
    for _ in range(retries):
        try:
            with open(path, "rb") as f:
                return f.read()
        except:
            time.sleep(delay)
    return None

if os.path.exists(VIOLATION_IMAGE):
    image_bytes = load_image_bytes(VIOLATION_IMAGE)

    if image_bytes:
        st.session_state.last_image_bytes = image_bytes
        st.image(image_bytes, use_container_width=True)
    elif st.session_state.last_image_bytes:
        st.image(st.session_state.last_image_bytes, use_container_width=True)
    else:
        st.info("Waiting for first violation image…")
else:
    st.info("No violation screenshot available.")

# -------- Recent Violations --------
st.subheader("📄 Recent Violations")

if not violations_df.empty:
    st.dataframe(
        violations_df.tail(10)[
            ["event", "location", "timestamp"]
        ],
        use_container_width=True
    )
else:
    st.info("No violations recorded yet.")

# -------- Auto Refresh --------
if auto_refresh:
    time.sleep(REFRESH_INTERVAL)
    st.rerun()
