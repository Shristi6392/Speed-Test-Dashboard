import streamlit as st
from speed_test import run_speed_test
import pandas as pd
import datetime
import requests
import plotly.graph_objects as go

# 🔹 Page Config
st.set_page_config(page_title="Speed Test Tool", layout="centered")

# 🎨 FULL UI STYLING
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0e1117;
    color: white;
}

/* Navbar */
div[role="radiogroup"] {
    display: flex;
    justify-content: space-around;
    background: #1a1f2e;
    padding: 15px;
    border-radius: 12px;
}

/* Navbar Text */
div[role="radiogroup"] label div {
    color: #00f2fe !important;
    font-size: 22px !important;
    font-weight: bold !important;
}

/* Active Tab */
div[role="radiogroup"] input:checked + div {
    border-bottom: 3px solid #00f2fe;
}

/* Button */
.stButton>button {
    background: linear-gradient(135deg, #00f2fe, #4facfe);
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 20px;
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background: #1a1f2e;
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 10px;
    text-align: center;
}

/* Metric Labels */
div[data-testid="stMetric"] label {
    color: #9aa4b2 !important;
    font-weight: bold !important;
}

/* Metric Values */
div[data-testid="stMetric"] div {
    color: white !important;
    font-size: 32px !important;
    font-weight: bold !important;
}

/* Remove green success */
div[data-testid="stAlert"] {
    background-color: #1a1f2e !important;
    color: #00f2fe !important;
    border-left: 5px solid #00f2fe !important;
}

/* Titles */
h1, h2, h3 {
    text-align: center;
    font-weight: bold;
    color: white;
}

/* Font */
html, body {
    font-size: 18px;
}

div[data-testid="stToggle"] > label > div {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# 🔹 Title
st.title("Internet Speed Test Tool")

# 🔹 NAVBAR
menu = st.radio(
    "",
    ["Dashboard", "History", "Network", "Settings"],
    horizontal=True
)

st.markdown("---")

# 🔹 Session State
if "history" not in st.session_state:
    st.session_state.history = []

if "show_graph" not in st.session_state:
    st.session_state.show_graph = True

if "show_analysis" not in st.session_state:
    st.session_state.show_analysis = True

# ------------------ DASHBOARD ------------------
if menu == "Dashboard":

    if st.button("Run Speed Test"):

        with st.spinner("Testing your internet speed..."):
            download, upload, ping = run_speed_test()

            if download is None:
                st.error(f"Error: {ping}")
                st.stop()

        # Aqua success box
        st.markdown("""
        <div style="
            background: #1a1f2e;
            padding: 12px;
            border-radius: 10px;
            border-left: 5px solid #00f2fe;
            color: #00f2fe;
            font-weight: bold;
            text-align: center;
        ">
            Test Completed Successfully
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Metrics with gap
        col1, col2, col3 = st.columns(3, gap="large")
        col1.metric("Download", f"{download:.2f} Mbps")
        col2.metric("Upload", f"{upload:.2f} Mbps")
        col3.metric("Ping", f"{ping:.2f} ms")

        st.markdown("<br>", unsafe_allow_html=True)

        # Analysis
        def analyze_speed(download, upload, ping):
            if download > 50 and upload > 20 and ping < 20:
                return "Excellent connection"
            elif download > 20:
                return "Good speed"
            elif download > 5:
                return "Average speed"
            else:
                return "Slow connection"

        if st.session_state.show_analysis:
            st.subheader("Smart Analysis")
            st.markdown(f"""
            <div style="
                background: #1a1f2e;
                padding: 12px;
                border-radius: 10px;
                border-left: 5px solid #00f2fe;
                color: #00f2fe;
                font-weight: bold;
                text-align: center;
            ">
                {analyze_speed(download, upload, ping)}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Aqua Speedometer
        if st.session_state.show_graph:
            st.subheader("Speed Meter")

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=download,
                number={'font': {'color': "#00f2fe", 'size': 40}},
                title={'text': "Download Speed", 'font': {'color': "#00f2fe", 'size': 22}},
                gauge={
                    'axis': {'range': [0, 200], 'tickcolor': "#00f2fe"},
                    'bar': {'color': "#00f2fe"},
                    'bgcolor': "#0e1117",
                    'borderwidth': 2,
                    'bordercolor': "#00f2fe",
                    'steps': [
                        {'range': [0, 50], 'color': "#0f2027"},
                        {'range': [50, 100], 'color': "#203a43"},
                        {'range': [100, 200], 'color': "#2c5364"},
                    ],
                }
            ))

            fig.update_layout(
                paper_bgcolor="#0e1117",
                font={'color': "#00f2fe"}
            )

            st.plotly_chart(fig, use_container_width=True)

        # Save History
        st.session_state.history.append({
            "Time": datetime.datetime.now().strftime("%H:%M:%S"),
            "Download": download,
            "Upload": upload,
            "Ping": ping
        })

# ------------------ HISTORY ------------------
elif menu == "History":

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df)

        if len(df) > 1:
            st.markdown("<br>", unsafe_allow_html=True)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["Time"], y=df["Download"], name="Download"))
            fig.add_trace(go.Scatter(x=df["Time"], y=df["Upload"], name="Upload"))
            fig.update_layout(paper_bgcolor="#0e1117", font={'color': "white"})
            st.plotly_chart(fig)
    else:
        st.info("No data yet")

# ------------------ NETWORK ------------------
elif menu == "Network":

    st.subheader("Network Info")

    try:
        ip = requests.get("https://api.ipify.org?format=json").json()["ip"]
        st.write("IP Address:", ip)
    except:
        st.error("Failed to fetch IP")

# ------------------ SETTINGS ------------------
elif menu == "Settings":

    st.subheader("Settings")

    st.session_state.show_graph = st.toggle(
        "Show Speed Meter", value=st.session_state.show_graph
    )

    st.session_state.show_analysis = st.toggle(
        "Show Smart Analysis", value=st.session_state.show_analysis
    )