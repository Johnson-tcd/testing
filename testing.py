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
            margin-bottom: 20px;
        }
        .subheader {
            text-align: center;
            font-size: 1.5rem;
            color: #4a1c61;
            margin-top: 20px;
        }
        .update-container {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .update-header {
            font-size: 1.3rem;
            font-weight: bold;
            color: #4a1c61;
        }
        .update-date {
            font-style: italic;
            color: #666;
        }
        .top-nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .nav-items {
            display: flex;
            gap: 20px;
        }
        .nav-item {
            padding: 8px 15px;
            text-decoration: none;
            color: #4a1c61;
            font-weight: bold;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .nav-item:hover, .nav-item.active {
            background-color: #e9ecef;
        }
        .login-button {
            background-color: #6a2c91;
            color: white !important;
            padding: 8px 20px;
            border-radius: 5px;
            font-weight: bold;
            text-decoration: none;
            transition: background-color 0.3s;
        }
        .login-button:hover {
            background-color: #4a1c61;
        }
    </style>
""", unsafe_allow_html=True)

# Sample regulatory updates - moved to global scope with representative images
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

# Initialize session state for login status if it doesn't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Initialize page in session state if it doesn't exist
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Top navigation bar
def create_top_navigation():
    # Using a container to create the navigation bar
    nav_container = st.container()
    
    with nav_container:
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.image("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=200&h=200&fit=crop&auto=format", width=80)
            
        with col2:
            # Create horizontal navigation with buttons instead of HTML links
            pages = ["Home", "Latest Updates", "Regulation Map"]
            
            cols = st.columns(len(pages))
            for i, p in enumerate(pages):
                with cols[i]:
                    if st.button(p, key=f"nav_{p}", use_container_width=True):
                        st.session_state.page = p
                        st.experimental_rerun()
            
        with col3:
            if not st.session_state.logged_in:
                if st.button("Login", key="top_login", use_container_width=True):
                    st.session_state.page = "Login"
                    st.experimental_rerun()
            else:
                st.write("Welcome, Admin")
                if st.button("Logout", key="top_logout", use_container_width=True):
                    st.session_state.logged_in = False
                    st.session_state.page = "Home"
                    st.experimental_rerun()

# Create the horizontal navigation bar
create_top_navigation()

# Header
st.markdown("<div class='header'>🌍 Global Financial Regulations Hub</div>", unsafe_allow_html=True)

# Sidebar for secondary navigation
with st.sidebar:
    st.title("Navigation")
    sidebar_page = st.radio("Go to", ["Home", "Latest Updates", "Regulation Map", "Login"], label_visibility="collapsed")
    if sidebar_page != st.session_state.page:
        st.session_state.page = sidebar_page
        st.experimental_rerun()

# Use the page from session state
page = st.session_state.page

if page == "Home":
    st.markdown("<div class='subheader'>Stay ahead with the latest financial regulations</div>", unsafe_allow_html=True)
    
    # Initialize session state for auto-rotation
    if 'update_index' not in st.session_state:
        st.session_state.update_index = 0
        st.session_state.last_update_time = time.time()
    
    # Function to display a specific update
    def display_update(update):
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(update['Image'], use_container_width=True)
        with col2:
            st.markdown(f"<div class='update-container'>", unsafe_allow_html=True)
            st.markdown(f"<div class='update-header'>{update['Region']}: {update['Update']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='update-date'>📅 {update['Date']}</div>", unsafe_allow_html=True)
            st.write(update['Description'])
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Create tabs for viewing options
    tab1, tab2 = st.tabs(["Auto-Rotating Updates", "Browse All Updates"])
    
    with tab1:
        # Auto-rotating updates
        placeholder = st.empty()
        
        # Automatically advance to next update every 5 seconds
        current_time = time.time()
        if current_time - st.session_state.last_update_time > 5:
            st.session_state.update_index = (st.session_state.update_index + 1) % len(updates)
            st.session_state.last_update_time = current_time
        
        # Display current update
        with placeholder.container():
            display_update(updates[st.session_state.update_index])
            st.progress((st.session_state.update_index + 1) / len(updates))
            st.caption(f"Showing update {st.session_state.update_index + 1} of {len(updates)}")
    
    with tab2:
        # Manual browsing of all updates
        for update in updates:
            display_update(update)
            st.markdown("---")

elif page == "Latest Updates":
    st.write("### Latest Regulation Updates")
    # Convert updates to DataFrame with additional Description column
    data = pd.DataFrame(updates)
    # Display relevant columns
    st.dataframe(data[["Region", "Update", "Date", "Description"]], hide_index=True, use_container_width=True)
    
    # Add filter options
    st.write("### Filter Updates")
    col1, col2 = st.columns(2)
    with col1:
        selected_region = st.multiselect("Filter by Region", options=list(set([u["Region"] for u in updates])))
    with col2:
        date_range = st.date_input("Date Range", value=[])
    
    if selected_region:
        filtered_data = data[data["Region"].isin(selected_region)]
        st.write(f"### Filtered Results ({len(filtered_data)} updates)")
        st.dataframe(filtered_data[["Region", "Update", "Date", "Description"]], hide_index=True, use_container_width=True)

elif page == "Regulation Map":
    st.write("### Explore Global Regulations - Interactive Map")
    
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
        "style": {"background": "rgba(74, 28, 97, 0.8)", "color": "white", "font-family": "sans-serif", "padding": "10px"}
    }
    
    # Render the map
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tooltip
    ))

    # Display regulatory info when a region is selected
    region_col1, region_col2 = st.columns([1, 2])
    with region_col1:
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

elif page == "Login":
    login_cols = st.columns([1, 2, 1])
    with login_cols[1]:
        st.write("### User Login")
        st.markdown("<div class='update-container'>", unsafe_allow_html=True)
        
        # Use more secure approach for authentication
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        # Store valid users in a separate dictionary (in a real app, use a database)
        valid_users = {
            "admin": "secure_password_123",
            "user": "user_password_456"
        }
        
        login_button_col1, login_button_col2, login_button_col3 = st.columns([1, 1, 1])
        with login_button_col2:
            if st.button("Login", use_container_width=True):
                if username in valid_users and password == valid_users[username]:
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.write("Welcome to the Financial Regulations Hub admin panel!")
                else:
                    st.error("Invalid credentials. Please try again.")
                    st.session_state.logged_in = False
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Show additional info only if logged in
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
