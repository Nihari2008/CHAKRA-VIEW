import streamlit as st
import requests
import pandas as pd

BACKEND = "http://localhost:8000"

st.set_page_config(page_title="Chakra-View", layout="wide")

# -------------------------
# TECHIE CSS THEME (Pure UI)
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@500;700&family=JetBrains+Mono:wght@400&display=swap');

/* Dark Techie Base */
.main { background: linear-gradient(135deg, #0A0E1A 0%, #1A1F2E 100%); }
.stApp { background: transparent; }

/* Header Glow */
h1 { font-family: 'Orbitron', monospace !important; font-weight: 900 !important; 
     background: linear-gradient(135deg, #00D4FF 0%, #7C3AED 50%, #A855F7 100%) !important;
     -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
     text-shadow: 0 0 40px rgba(0,212,255,0.6) !important; font-size: 3.2rem !important; }

/* Metrics - Neumorphic Glow */
[data-testid="metric-container"] { 
    background: rgba(26,31,46,0.85) !important; border: 1px solid rgba(0,212,255,0.3) !important;
    border-radius: 20px !important; padding: 2rem !important; margin: 1rem 0 !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5), 0 0 30px rgba(0,212,255,0.15) !important;
    backdrop-filter: blur(15px) !important; transition: all 0.4s cubic-bezier(0.25,0.8,0.25,1) !important; }
[data-testid="metric-container"]:hover { 
    transform: translateY(-8px) !important; box-shadow: 0 20px 60px rgba(0,212,255,0.3) !important; }
.stMetric > label { color: #A1A1AA !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1rem !important; }
.stMetric > div > div { color: #00D4FF !important; font-family: 'Orbitron', monospace !important; 
                        font-size: 2.8rem !important; text-shadow: 0 0 20px #00D4FF !important; }

/* Buttons - Holographic */
.stButton > button { height: 55px !important; border-radius: 30px !important; 
                    font-family: 'Rajdhani', sans-serif !important; font-weight: 700 !important;
                    font-size: 1.1rem !important; border: none !important; transition: all 0.3s ease !important; }
.stButton > button:first-child { 
    background: linear-gradient(135deg, #00D4FF, #7C3AED) !important; color: white !important;
    box-shadow: 0 10px 40px rgba(0,212,255,0.4) !important; }
.stButton > button:first-child:hover { 
    box-shadow: 0 15px 50px rgba(0,212,255,0.6) !important; transform: scale(1.08) !important; }
.stButton > button:last-child { 
    background: rgba(26,31,46,0.8) !important; color: #00D4FF !important; 
    border: 2px solid rgba(0,212,255,0.5) !important; backdrop-filter: blur(10px) !important; }
.stButton > button:last-child:hover { 
    background: linear-gradient(135deg, #00D4FF, #7C3AED) !important; color: white !important; }

/* Input - Glassmorphism */
.stTextInput > div > div > input { 
    background: rgba(26,31,46,0.9) !important; border: 2px solid rgba(0,212,255,0.2) !important;
    border-radius: 16px !important; color: #F1F5F9 !important; padding: 16px 20px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 1.1rem !important;
    backdrop-filter: blur(20px) !important; box-shadow: inset 0 4px 20px rgba(0,0,0,0.3) !important; }
.stTextInput > div > div > input:focus { 
    border-color: #00D4FF !important; box-shadow: 0 0 30px rgba(0,212,255,0.5) !important; }

/* DataFrames - Cyber Table */
.element-container .stDataFrame { 
    background: rgba(26,31,46,0.7) !important; border-radius: 16px !important; 
    border: 1px solid rgba(0,212,255,0.25) !important; backdrop-filter: blur(15px) !important; }
table[data-testid="dataframe"] { font-family: 'JetBrains Mono', monospace !important; color: #E2E8F0 !important; }
table[data-testid="dataframe"] th { 
    background: linear-gradient(90deg, rgba(0,212,255,0.2), rgba(124,58,237,0.2)) !important;
    color: #00D4FF !important; border: none !important; padding: 12px !important; font-weight: 600 !important; }
table[data-testid="dataframe"] tbody tr:hover { 
    background: rgba(0,212,255,0.2) !important; transform: scale(1.02) !important; }
table[data-testid="dataframe"] tbody tr:nth-child(even) { background: rgba(0,212,255,0.05) !important; }

/* Section Headers */
[data-testid="stMarkdownContainer"] h2 { 
    font-family: 'Orbitron', monospace !important; font-size: 2.2rem !important; font-weight: 700 !important;
    background: linear-gradient(135deg, #00D4FF, #A855F7) !important; 
    -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
    text-shadow: 0 0 25px rgba(0,212,255,0.4) !important; margin-bottom: 2rem !important; }

/* Final Risk - Hero Style */
[data-testid="column"] [data-testid="metric-container"]:first-child { font-size: 4rem !important; }
.stError { background: linear-gradient(135deg, rgba(239,68,68,0.2), rgba(220,38,127,0.2)) !important;
           border: 2px solid #EF4444 !important; border-radius: 16px !important; 
           box-shadow: 0 0 40px rgba(239,68,68,0.6) !important; padding: 1.5rem !important;
           animation: riskPulse 2s infinite !important; }
.stSuccess { background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(34,197,94,0.2)) !important;
            border: 2px solid #10B981 !important; border-radius: 16px !important;
            box-shadow: 0 0 40px rgba(16,185,129,0.6) !important; padding: 1.5rem !important; }

/* Dividers */
hr { height: 3px !important; background: linear-gradient(90deg, transparent, #00D4FF, #7C3AED, transparent) !important;
     border: none !important; box-shadow: 0 0 15px rgba(0,212,255,0.6) !important; margin: 4rem 0 !important; }

/* Animations */
@keyframes riskPulse { 0%, 100% { box-shadow: 0 0 20px rgba(239,68,68,0.6); }
                       50% { box-shadow: 0 0 40px rgba(239,68,68,0.9); } }
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER (UNCHANGED LOGIC)
# -------------------------
st.markdown("## 🔐 Chakra-View")
st.caption("Graph-Based UPI Mule Account Detection System (Bank-Side Demo)")

st.divider()

# -------------------------
# INPUT SECTION (UNCHANGED LOGIC)
# -------------------------
col1, col2, col3 = st.columns([6, 2, 2])

with col1:
    vpa = st.text_input("Analyze UPI / Account ID", placeholder="user_317")

with col2:
    analyze = st.button("🔍 Analyze", use_container_width=True)

with col3:
    clear = st.button("🧹 Clear", use_container_width=True)

if clear:
    st.experimental_rerun()

if not analyze or not vpa:
    st.stop()

# -------------------------
# FAN-IN (UNCHANGED LOGIC + UI)
# -------------------------
st.header("① Fan-In Analysis")

fan = requests.get(f"{BACKEND}/fan_in", params={"vpa": vpa}).json()

col1, col2 = st.columns(2)
with col1:
    st.metric("Unique Senders", fan["unique_senders"])
with col2:
    st.metric("Fan-In Risk Score", fan["risk_score"])

df_fan = pd.DataFrame(fan["rows"])
df_fan["risk_score"] = fan["risk_score"]
st.dataframe(df_fan, use_container_width=True)

st.divider()

# -------------------------
# VELOCITY (UNCHANGED)
# -------------------------
st.header("② Velocity (Money Dwell Time)")

vel = requests.get(f"{BACKEND}/velocity", params={"vpa": vpa}).json()

df_vel = pd.DataFrame(vel["rows"])

col1, col2 = st.columns([1,3])
with col1:
    st.metric("Velocity Risk Score", vel["risk_score"])
with col2:
    st.dataframe(df_vel, use_container_width=True)

st.divider()

# -------------------------
# CLUSTER (UNCHANGED)
# -------------------------
st.header("③ Network / Cluster Analysis")

clu = requests.get(f"{BACKEND}/cluster", params={"vpa": vpa}).json()

col1, col2, col3 = st.columns(3)
with col1:
    st.write(f"**In Network:** {clu['in_network']}")
with col2:
    st.write(f"**Network Size:** {clu['network_size']}")
with col3:
    st.write(f"**Cluster Risk Score:** {clu['risk_score']}")

st.divider()

# -------------------------
# FINAL SCORE (UNCHANGED)
# -------------------------
final = requests.get(f"{BACKEND}/final_score", params={"vpa": vpa}).json()

st.header("🔴 Final Risk Assessment")
st.metric("Final Risk Score", final["score"])

if final["level"] == "HIGH":
    st.error("🚨 HIGH RISK — Possible Mule Account")
else:
    st.success("✅ LOW RISK — Normal Account")
