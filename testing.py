import streamlit as st
import pandas as pd
import pydeck as pdk
import time

# Page configuration
st.set_page_config(page_title="Global Financial Regulations Hub", layout="wide")

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Custom CSS for styling
st.markdown("""
<style>
    .feature-card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 10px;
        text-align: center;
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .pricing-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
    }
    .pricing-table th, .pricing-table td {
        padding: 15px;
        text-align: center;
        border: 1px solid #ddd;
    }
    .pricing-table th {
        background-color: #f4f4f4;
    }
    .footer {
        margin-top: 50px;
        padding: 20px;
        background-color: #f4f4f4;
        text-align: center;
    }
    /* Custom Button Styles */
    .custom-button {
        background-color: #e6a8d7; /* Light Purple */
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .custom-button:hover {
        background-color: #d291bc; /* Darker Purple on Hover */
    }
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
    /* Top Navigation Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        background-color: #4a1c61;
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .top-nav a {
        color: white;
        text-decoration: none;
        margin: 0 10px;
    }
    .top-nav a:hover {
        text-decoration: underline;
    }
    /* Rotating Updates */
    .rotating-update {
        padding: 20px;
        background-color: #f4f4f4;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sample regulatory updates
updates = [
    {"Region": "USA", "Update": "SEC Finalizes New Climate Disclosure Rules", "Date": "March 15, 2025", 
     "Image": "https://images.unsplash.com/photo-1621944190310-e3cca1564bd7?w=800&h=600&fit=crop&auto=format", 
     "Description": "The Securities and Exchange Commission has finalized rules requiring public companies to disclose climate-related financial risks."},
    
    {"Region": "EU", "Update": "ECB Updates Digital Euro Framework", "Date": "March 12, 2025", 
     "Image": "https://images.unsplash.com/photo-1580674285054-bed31e145f59?w=800&h=600&fit=crop&auto=format", 
     "Description": "The European Central Bank has released a comprehensive framework for the implementation of the Digital Euro."},
    
    {"Region": "UK", "Update": "FCA Introduces Enhanced Consumer Protection Rules", "Date": "March 10, 2025", 
     "Image": "https://images.unsplash.com/photo-1486299267070-83823f5448dd?w=800&h=600&fit=crop&auto=format", 
     "Description": "The Financial Conduct Authority has implemented new rules to strengthen consumer protection in financial services."},
    
    {"Region": "China", "Update": "PBOC Announces New Capital Requirements for Digital Banks", "Date": "March 8, 2025", 
     "Image": "https://images.unsplash.com/photo-1598257006458-087169a1f08d?w=800&h=600&fit=crop&auto=format", 
     "Description": "The People's Bank of China has established new capital requirements specifically tailored for digital banking institutions."},
    
    {"Region": "Singapore", "Update": "MAS Revises Digital Asset Licensing Framework", "Date": "March 5, 2025", 
     "Image": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800&h=600&fit=crop&auto=format", 
     "Description": "The Monetary Authority of Singapore has revised its licensing framework for digital asset service providers."},
    
    {"Region": "UAE", "Update": "DFSA Implements New FinTech Regulations", "Date": "March 3, 2025", 
     "Image": "https://images.unsplash.com/photo-1546412414-e1885e51cfa5?w=800&h=600&fit=crop&auto=format", 
     "Description": "The Dubai Financial Services Authority has implemented new regulations to support the growth of FinTech innovation."},
    
    {"Region": "Brazil", "Update": "CVM Updates Securities Regulations", "Date": "March 1, 2025", 
     "Image": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=800&h=600&fit=crop&auto=format", 
     "Description": "The Brazilian Securities Commission has updated regulations to enhance market transparency and investor protection."},
    
    {"Region": "Germany", "Update": "BaFin Introduces Stricter AML Guidelines", "Date": "February 28, 2025", 
     "Image": "https://images.unsplash.com/photo-1560969184-10fe8719e047?w=800&h=600&fit=crop&auto=format", 
     "Description": "The Federal Financial Supervisory Authority has introduced stricter anti-money laundering guidelines for financial institutions."},
    
    {"Region": "Japan", "Update": "FSA Strengthens Digital Asset Regulations", "Date": "February 25, 2025", 
     "Image": "https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=800&h=600&fit=crop&auto=format", 
     "Description": "The Financial Services Agency has strengthened regulations governing digital assets and cryptocurrency exchanges."}
]

# Top Navigation Bar
st.markdown("""
<div class="top-nav">
    <div>
        <a href="#home">Home</a>
        <a href="#latest-updates">Latest Updates</a>
        <a href="#compliance-report">Compliance Report</a>
    </div>
    <div>
        <a href="#login">Login</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Rotating Updates at the Top
if 'update_index' not in st.session_state:
    st.session_state.update_index = 0

def rotate_update():
    st.session_state.update_index = (st.session_state.update_index + 1) % len(updates)

# Display the current update
update = updates[st.session_state.update_index]
st.markdown(f"""
<div class="rotating-update">
    <h3>{update['Region']}: {update['Update']}</h3>
    <p>{update['Description']}</p>
    <p><em>Date: {update['Date']}</em></p>
</div>
""", unsafe_allow_html=True)

# Button to manually rotate updates (optional)
if st.button("Next Update"):
    rotate_update()

# Auto-rotate updates every 5 seconds using a timer
if "last_update_time" not in st.session_state:
    st.session_state.last_update_time = time.time()

current_time = time.time()
if current_time - st.session_state.last_update_time > 5:  # 5 seconds
    rotate_update()
    st.session_state.last_update_time = current_time

# Header
st.markdown("<div class='header'>🌍 Global Financial Regulations Hub</div>", unsafe_allow_html=True)

# Key Features Section
st.header("Key Features")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📰</div>
        <h3>Real-Time Regulatory Updates</h3>
        <p>Track regulatory changes globally in real-time.</p>
        <button class="custom-button">Learn More</button>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h3>AI-Driven Risk Analysis</h3>
        <p>Identify compliance gaps and fraud risks with predictive analytics.</p>
        <button class="custom-button">Learn More</button>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⚙️</div>
        <h3>Automated Audits</h3>
        <p>Ensure processes meet regulatory standards effortlessly.</p>
        <button class="custom-button">Learn More</button>
    </div>
    """, unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🕵️</div>
        <h3>Fraud Detection & AML</h3>
        <p>Detect and prevent fraudulent activities with advanced ML algorithms.</p>
        <button class="custom-button">Learn More</button>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📋</div>
        <h3>KYC Tools</h3>
        <p>Automate customer background checks for identity verification.</p>
        <button class="custom-button">Learn More</button>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔒</div>
        <h3>Cybersecurity Protection</h3>
        <p>Safeguard sensitive data from malware and cyber threats.</p>
        <button class="custom-button">Learn More</button>
    </div>
    """, unsafe_allow_html=True)

# Global Reach Section
st.header("Global Reach")
st.subheader("Compliance Without Borders")
st.write(
    "Our platform supports regulatory requirements across 100+ jurisdictions, ensuring you stay compliant no matter where you operate.")

# Define map data for PyDeck with more accurate coordinates and information
map_data = pd.DataFrame([
    {"lat": 38.9, "lon": -77.0, "name": "USA", "size": 100, "color": [76, 28, 97]},
    {"lat": 50.8, "lon": 4.4, "name": "EU", "size": 100, "color": [0, 51, 153]},
    {"lat": 51.5, "lon": -0.1, "name": "UK", "size": 100, "color": [204, 0, 0]},
    {"lat": 39.9, "lon": 116.4, "name": "China", "size": 100, "color": [204, 0, 0]},
    {"lat": 1.3, "lon": 103.8, "name": "Singapore", "size": 100, "color": [204, 0, 0]},
    {"lat": 25.2, "lon": 55.3, "name": "UAE", "size": 100, "color": [0, 102, 0]},
    {"lat": -15.8, "lon": -47.9, "name": "Brazil", "size": 100, "color": [0, 153, 0]},
    {"lat": 52.5, "lon": 13.4, "name": "Germany", "size": 100, "color": [0, 0, 0]},
    {"lat": 35.7, "lon": 139.8, "name": "Japan", "size": 100, "color": [204, 0, 0]}
])

# Create the map
view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1.5,
    pitch=40,
    bearing=0
)

# Create the scatter plot layer with custom colors
layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    get_position=["lon", "lat"],
    get_radius="size",
    get_fill_color="color",
    pickable=True,
    auto_highlight=True,
    opacity=0.8
)

# Create the tooltip
tooltip = {
    "html": "<b>{name}</b>",
    "style": {"background": "rgba(74, 28, 97, 0.8)", "color": "white", "font-family": "sans-serif",
              "padding": "10px"}
}

# Render the map
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=view_state,
    layers=[layer],
    tooltip=tooltip
))

# Display regulatory info when a region is selected
selected_region = st.selectbox("Select region for detailed regulations",
                               options=[update["Region"] for update in updates])

# Show the selected region's update
for update in updates:
    if update["Region"] == selected_region:
        st.markdown(f"<div class='update-container'>", unsafe_allow_html=True)
        st.markdown(f"### {update['Region']} Regulations")
        st.image(update['Image'], width=400)
        st.write(f"**Latest Update:** {update['Update']}")
        st.write(f"**Date:** {update['Date']}")
        st.write(update['Description'])
        st.markdown("</div>", unsafe_allow_html=True)
        break

# Pricing or Subscription Plans
st.header("Pricing Plans")
st.markdown("""
<table class="pricing-table">
    <tr>
        <th>Plan</th>
        <th>Features</th>
        <th>Action</th>
    </tr>
    <tr>
        <td><strong>Basic</strong></td>
        <td>Real-time regulatory updates, basic risk analysis</td>
        <td><button class="custom-button">Sign Up</button></td>
    </tr>
    <tr>
        <td><strong>Pro</strong></td>
        <td>Advanced fraud detection, AML tools, automated audits</td>
        <td><button class="custom-button">Sign Up</button></td>
    </tr>
    <tr>
        <td><strong>Enterprise</strong></td>
        <td>Custom compliance reports, consulting services, priority support</td>
        <td><button class="custom-button">Contact Us</button></td>
    </tr>
</table>
""", unsafe_allow_html=True)

# Footer with Key Links
st.markdown("""
<div class="footer">
    <p><strong>Global Compliance Hub:</strong> Your One-Stop Solution for Real-Time Regulatory Compliance.</p>
    <p>
        <a href="#features">Features</a> | 
        <a href="#pricing">Pricing</a> | 
        <a href="#about">About Us</a> | 
        <a href="#contact">Contact Us</a> | 
        <a href="#blog">Blog/Resources</a>
    </p>
    <p>
        <a href="https://linkedin.com">LinkedIn</a> | 
        <a href="https://twitter.com">Twitter</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Login Section
if st.session_state.get('logged_in', False):
    st.write("### Admin Panel")
    st.write("Here you can manage regulatory updates and system settings.")
    
    # Add tabs for different admin functions
    admin_tab1, admin_tab2, admin_tab3 = st.tabs(["Add Update", "Edit Updates", "System Settings"])
    
    with admin_tab1:
        st.write("### Add New Regulatory Update")
        new_region = st.selectbox("Region", options=["USA", "EU", "UK", "China", "Singapore", "UAE", "Brazil", "Germany", "Japan", "Other"])
        new_update = st.text_input("Update Title")
        new_description = st.text_area("Description")
        new_date = st.date_input("Date")
        
        if st.button("Add Update"):
            st.success("Update added successfully! (Simulated)")
    
    with admin_tab2:
        st.write("### Edit Existing Updates")
        edit_update = st.selectbox("Select Update to Edit", options=[f"{u['Region']}: {u['Update']}" for u in updates])
        
        if edit_update:
            st.text_area("Edit Description", value=next((u["Description"] for u in updates if f"{u['Region']}: {u['Update']}" == edit_update), ""))
            if st.button("Save Changes"):
                st.success("Changes saved successfully! (Simulated)")
    
    with admin_tab3:
        st.write("### System Settings")
        st.checkbox("Enable email notifications")
        st.checkbox("Enable API access")
        st.slider("Data retention period (days)", 30, 365, 180)
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully! (Simulated)")

# Footer
st.write("""
    ---
    *© 2025 Global Financial Regulations Hub. All rights reserved.*
""")
