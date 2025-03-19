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

# Sample regulatory updates - moved to global scope
updates = [
    {"Region": "USA", "Update": "SEC Finalizes New Climate Disclosure Rules", "Date": "March 15, 2025", "Image": "https://placehold.co/600x400/purple/white?text=USA+Regulations"},
    {"Region": "EU", "Update": "ECB Updates Digital Euro Framework", "Date": "March 12, 2025", "Image": "https://placehold.co/600x400/blue/white?text=EU+Regulations"},
    {"Region": "UK", "Update": "FCA Introduces Enhanced Consumer Protection Rules", "Date": "March 10, 2025", "Image": "https://placehold.co/600x400/red/white?text=UK+Regulations"},
    {"Region": "China", "Update": "PBOC Announces New Capital Requirements for Digital Banks", "Date": "March 8, 2025", "Image": "https://placehold.co/600x400/gold/black?text=China+Regulations"},
    {"Region": "Singapore", "Update": "MAS Revises Digital Asset Licensing Framework", "Date": "March 5, 2025", "Image": "https://placehold.co/600x400/red/white?text=Singapore+Regulations"},
    {"Region": "UAE", "Update": "DFSA Implements New FinTech Regulations", "Date": "March 3, 2025", "Image": "https://placehold.co/600x400/green/white?text=UAE+Regulations"},
    {"Region": "South America", "Update": "Brazil Updates Securities Regulations", "Date": "March 1, 2025", "Image": "https://placehold.co/600x400/green/yellow?text=Brazil+Regulations"},
    {"Region": "Germany", "Update": "BaFin Introduces Stricter AML Guidelines", "Date": "February 28, 2025", "Image": "https://placehold.co/600x400/black/gold?text=Germany+Regulations"},
    {"Region": "France", "Update": "AMF Strengthens Digital Asset Regulations", "Date": "February 25, 2025", "Image": "https://placehold.co/600x400/blue/white?text=France+Regulations"}
]

# Sidebar for navigation
st.sidebar.image("https://placehold.co/200x200/purple/white?text=Financial+Hub", width=100)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Latest Updates", "Regulation Map", "Login"])

if page == "Home":
    st.markdown("<div class='subheader'>Stay ahead with the latest financial regulations</div>", unsafe_allow_html=True)
    
    # Only show first update by default
    if 'update_index' not in st.session_state:
        st.session_state.update_index = 0
    
    # Auto-rotate updates if desired
    auto_rotate = st.checkbox("Auto-rotate updates", value=False)
    
    if auto_rotate:
        placeholder = st.empty()
        for i in range(len(updates)):
            with placeholder.container():
                update = updates[i]
                st.image(update['Image'], use_column_width=True)
                st.info(f"#### {update['Region']}\n**{update['Update']}**\n📅 {update['Date']}")
                time.sleep(3)
    else:
        # Manual navigation
        update = updates[st.session_state.update_index]
        st.image(update['Image'], use_column_width=True)
        st.info(f"#### {update['Region']}\n**{update['Update']}**\n📅 {update['Date']}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Previous") and st.session_state.update_index > 0:
                st.session_state.update_index -= 1
                st.rerun()
        with col2:
            if st.button("Next") and st.session_state.update_index < len(updates) - 1:
                st.session_state.update_index += 1
                st.rerun()

elif page == "Latest Updates":
    st.write("### Latest Regulation Updates")
    # Convert updates to DataFrame
    data = pd.DataFrame(updates)
    # Display only relevant columns
    st.dataframe(data[["Region", "Update", "Date"]], hide_index=True)

elif page == "Regulation Map":
    st.write("### Explore Global Regulations - Interactive Map")
    
    # Define map data for PyDeck
    map_data = pd.DataFrame([
        {"lat": 40.0, "lon": -100.0, "name": "USA", "size": 100},
        {"lat": 50.0, "lon": 10.0, "name": "EU", "size": 100},
        {"lat": 55.0, "lon": -2.0, "name": "UK", "size": 100},
        {"lat": 35.0, "lon": 105.0, "name": "China", "size": 100},
        {"lat": 1.3, "lon": 103.8, "name": "Singapore", "size": 100},
        {"lat": 25.2, "lon": 55.3, "name": "UAE", "size": 100},
        {"lat": -10.0, "lon": -55.0, "name": "South America", "size": 100},
        {"lat": 51.1, "lon": 10.4, "name": "Germany", "size": 100},
        {"lat": 48.9, "lon": 2.4, "name": "France", "size": 100}
    ])
    
    # Create the map
    view_state = pdk.ViewState(
        latitude=20,
        longitude=0,
        zoom=1,
        pitch=0
    )
    
    # Create the scatter plot layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position=["lon", "lat"],
        get_radius="size",
        get_fill_color=[100, 30, 150, 160],  # Purple color with transparency
        pickable=True,
        auto_highlight=True
    )
    
    # Create the tooltip
    tooltip = {
        "html": "<b>{name}</b>",
        "style": {"background": "rgba(74, 28, 97, 0.8)", "color": "white", "font-family": "sans-serif"}
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
            st.write(f"### {update['Region']} Regulations")
            st.write(f"**Latest Update:** {update['Update']}")
            st.write(f"**Date:** {update['Date']}")
            break

elif page == "Login":
    st.write("### User Login")
    
    # Use more secure approach for authentication
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Store valid users in a separate dictionary (in a real app, use a database)
    valid_users = {
        "admin": "secure_password_123",
        "user": "user_password_456"
    }
    
    if st.button("Login"):
        if username in valid_users and password == valid_users[username]:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.write("Welcome to the Financial Regulations Hub admin panel!")
        else:
            st.error("Invalid credentials. Please try again.")
            st.session_state.logged_in = False
    
    # Show additional info only if logged in
    if st.session_state.get('logged_in', False):
        st.write("### Admin Panel")
        st.write("Here you can manage regulatory updates and system settings.")
        
        # Example admin functionality
        if st.button("Download Regulatory Reports"):
            st.info("Reports would download here in a real application.")

# Footer
st.write("""
    ---
    *© 2025 Global Financial Regulations Hub. All rights reserved.*
""")
