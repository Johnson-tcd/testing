import streamlit as st
import pandas as pd
import pydeck as pdk
import time

# Page configuration
st.set_page_config(page_title="Global Financial Regulations Hub", layout="wide")

# Header
st.markdown("""
    <style>
        .header {
            background: linear-gradient(135deg, #4a1c61, #6a2c91);
            color: white;
            padding: 1rem;
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
        }
    </style>
    <div class='header'>Global Financial Regulations Hub</div>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Latest Updates", "Regulation Map", "Login"])

if page == "Home":
    st.write("### Your Global Financial Regulation Center")
    st.write("Stay updated with the latest financial regulations and policy changes across major economic regions.")
    
    # Sample regulatory updates
    updates = [
        {"Region": "USA", "Update": "SEC Finalizes New Climate Disclosure Rules", "Date": "March 15, 2025"},
        {"Region": "EU", "Update": "ECB Updates Digital Euro Framework", "Date": "March 12, 2025"},
        {"Region": "UK", "Update": "FCA Introduces Enhanced Consumer Protection Rules", "Date": "March 10, 2025"},
        {"Region": "China", "Update": "PBOC Announces New Capital Requirements for Digital Banks", "Date": "March 8, 2025"},
        {"Region": "Singapore", "Update": "MAS Revises Digital Asset Licensing Framework", "Date": "March 5, 2025"},
        {"Region": "UAE", "Update": "DFSA Implements New FinTech Regulations", "Date": "March 3, 2025"},
        {"Region": "South America", "Update": "Brazil Updates Securities Regulations", "Date": "March 1, 2025"},
        {"Region": "Germany", "Update": "BaFin Introduces Stricter AML Guidelines", "Date": "February 28, 2025"},
        {"Region": "France", "Update": "AMF Strengthens Digital Asset Regulations", "Date": "February 25, 2025"}
    ]
    
    # Rotating latest updates
    placeholder = st.empty()
    for _ in range(5):
        for update in updates:
            with placeholder.container():
                st.write(f"#### {update['Region']}")
                st.write(f"**{update['Update']}**")
                st.write(f"📅 {update['Date']}")
                time.sleep(3)

elif page == "Latest Updates":
    data = pd.DataFrame(updates)
    st.write("### Latest Regulation Updates")
    st.dataframe(data, hide_index=True)

elif page == "Regulation Map":
    st.write("### Explore Global Regulations")
    map_data = pd.DataFrame({
        'lat': [40.0, 50.0, 55.0, 35.0, 1.3, 25.2, -10.0, 51.1, 48.9],
        'lon': [-100.0, 10.0, -2.0, 105.0, 103.8, 55.3, -55.0, 10.4, 2.4],
        'region': ['USA', 'EU', 'UK', 'China', 'Singapore', 'UAE', 'South America', 'Germany', 'France']
    })

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=20,
            longitude=0,
            zoom=2
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[lon, lat]',
                get_color='[255, 0, 0, 160]',
                get_radius=500000,
            )
        ]
    ))

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
