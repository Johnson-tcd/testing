import streamlit as st
import pandas as pd
import pydeck as pdk
import time

# Page configuration
st.set_page_config(page_title="Global Financial Regulations Hub", layout="wide")

# Custom CSS
st.markdown("""
    <style>
        .header {
            background: linear-gradient(135deg, #4a1c61, #6a2c91);
            color: white;
            padding: 1rem;
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            border-radius: 10px;
        }
        .subheader {
            text-align: center;
            font-size: 1.5rem;
            color: #4a1c61;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='header'>🌍 Global Financial Regulations Hub</div>", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/8/84/Financial_Growth_Icon.png", width=100)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Latest Updates", "Regulation Map", "Login"])

if page == "Home":
    st.markdown("<div class='subheader'>Stay ahead with the latest financial regulations</div>", unsafe_allow_html=True)
    
    # Sample regulatory updates with images
    updates = [
        {"Region": "USA", "Update": "SEC Finalizes New Climate Disclosure Rules", "Date": "March 15, 2025", "Image": "https://example.com/usa.jpg"},
        {"Region": "EU", "Update": "ECB Updates Digital Euro Framework", "Date": "March 12, 2025", "Image": "https://example.com/eu.jpg"},
        {"Region": "UK", "Update": "FCA Introduces Enhanced Consumer Protection Rules", "Date": "March 10, 2025", "Image": "https://example.com/uk.jpg"},
        {"Region": "China", "Update": "PBOC Announces New Capital Requirements for Digital Banks", "Date": "March 8, 2025", "Image": "https://example.com/china.jpg"},
        {"Region": "Singapore", "Update": "MAS Revises Digital Asset Licensing Framework", "Date": "March 5, 2025", "Image": "https://example.com/singapore.jpg"},
        {"Region": "UAE", "Update": "DFSA Implements New FinTech Regulations", "Date": "March 3, 2025", "Image": "https://example.com/uae.jpg"},
        {"Region": "South America", "Update": "Brazil Updates Securities Regulations", "Date": "March 1, 2025", "Image": "https://example.com/brazil.jpg"},
        {"Region": "Germany", "Update": "BaFin Introduces Stricter AML Guidelines", "Date": "February 28, 2025", "Image": "https://example.com/germany.jpg"},
        {"Region": "France", "Update": "AMF Strengthens Digital Asset Regulations", "Date": "February 25, 2025", "Image": "https://example.com/france.jpg"}
    ]
    
    # Rotating latest updates
    placeholder = st.empty()
    for _ in range(3):
        for update in updates:
            with placeholder.container():
                st.image(update['Image'], use_column_width=True)
                st.info(f"#### {update['Region']}\n**{update['Update']}**\n📅 {update['Date']}")
                time.sleep(3)

elif page == "Latest Updates":
    data = pd.DataFrame(updates)
    st.write("### Latest Regulation Updates")
    st.dataframe(data, hide_index=True)

elif page == "Regulation Map":
    st.write("### Explore Global Regulations - Interactive Rotating Globe")
    st.components.v1.html(
        """
        <iframe src="https://earth.nullschool.net" width="100%" height="500px" style="border:none;"></iframe>
        <script>
            const points = [
                {lat: 40.0, lon: -100.0, label: "USA"},
                {lat: 50.0, lon: 10.0, label: "EU"},
                {lat: 55.0, lon: -2.0, label: "UK"},
                {lat: 35.0, lon: 105.0, label: "China"},
                {lat: 1.3, lon: 103.8, label: "Singapore"},
                {lat: 25.2, lon: 55.3, label: "UAE"},
                {lat: -10.0, lon: -55.0, label: "South America"},
                {lat: 51.1, lon: 10.4, label: "Germany"},
                {lat: 48.9, lon: 2.4, label: "France"}
            ];
            // Add code to display markers on the globe here.
        </script>
        """,
        height=500
    )

elif page == "Login":
    st.write("### User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "password":
            st.success("Login successful!")
        else:
            st.error("Invalid credentials. Please try again.")

# Footer
st.write("""
    ---
    *© 2025 Global Financial Regulations Hub. All rights reserved.*
""")
