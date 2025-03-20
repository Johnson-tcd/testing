import streamlit as st
import pandas as pd
import pydeck as pdk
import time

# Page configuration
st.set_page_config(page_title="Global Financial Regulations Hub", layout="wide")

# Custom CSS for top navigation and styling
st.markdown("""
<style>
    .topnav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background: linear-gradient(135deg, #4a1c61, #6a2c91);
        color: white;
        font-size: 1.2rem;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 1000;
    }
    .nav-links a {
        margin: 0 15px;
        color: white;
        text-decoration: none;
        font-weight: bold;
    }
    .login-button {
        background: #e6a8d7;
        padding: 8px 15px;
        border-radius: 5px;
        cursor: pointer;
    }
    .update-banner {
        text-align: center;
        font-size: 1.5rem;
        color: white;
        background: #6a2c91;
        padding: 10px;
        border-radius: 10px;
        margin-top: 60px;
    }
    .feature-card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 10px;
        background: white;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Bar at the Top
st.markdown("""
<div class='topnav'>
    <div class='nav-links'>
        <a href='#home'>Home</a>
        <a href='#updates'>Latest Updates</a>
        <a href='#compliance'>Compliance Report</a>
    </div>
    <div class='login-button'>Login</div>
</div>
""", unsafe_allow_html=True)

# Sample Updates Data
updates = [
    {"Region": "USA", "Update": "SEC Finalizes New Climate Rules"},
    {"Region": "EU", "Update": "ECB Releases Digital Euro Framework"},
    {"Region": "UK", "Update": "FCA Enhances Consumer Protection"},
    {"Region": "China", "Update": "PBOC Updates Digital Bank Requirements"},
]

# Rotating Banner for Latest Updates
def rotating_banner():
    for update in updates:
        st.markdown(f"""
        <div class='update-banner'>
            🌍 {update['Region']}: {update['Update']}
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2)

tab1, tab2, tab3 = st.tabs(["Home", "Latest Updates", "Compliance Report"])

with tab1:
    st.markdown("<h1 id='home'>🌍 Welcome to Global Financial Regulations Hub</h1>", unsafe_allow_html=True)
    rotating_banner()
    
    st.header("🌟 Key Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Real-Time Updates</h3>
            <p>Get the latest regulatory updates globally.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI-Powered Compliance</h3>
            <p>Identify compliance gaps with AI-driven insights.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>⚖️ Automated Legal Audits</h3>
            <p>Ensure regulatory compliance effortlessly.</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("<h1 id='updates'>📢 Latest Regulatory Updates</h1>", unsafe_allow_html=True)
    for update in updates:
        st.write(f"**{update['Region']}**: {update['Update']}")

with tab3:
    st.markdown("<h1 id='compliance'>✅ Compliance Reports</h1>", unsafe_allow_html=True)
    st.write("Generate compliance reports for different industries.")
