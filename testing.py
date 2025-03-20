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
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
        color: #6a2c91;
    }
    .pricing-table {
        width: 100%;
        border-collapse: collapse;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 10px;
        overflow: hidden;
    }
    .pricing-table th, .pricing-table td {
        padding: 15px;
        text-align: center;
        border: 1px solid #ddd;
    }
    .pricing-table th {
        background-color: #6a2c91;
        color: white;
    }
    .pricing-table tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    .footer {
        margin-top: 50px;
        padding: 20px;
        background-color: #f4f4f4;
        text-align: center;
        border-radius: 10px;
    }
    /* Custom Button Styles */
    .custom-button {
        background-color: #6a2c91; /* Purple */
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    .custom-button:hover {
        background-color: #8a3cb1; /* Lighter Purple on Hover */
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    .header {
        background: linear-gradient(135deg, #4a1c61, #6a2c91);
        color: white;
        padding: 1rem;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .subheader {
        text-align: center;
        font-size: 1.5rem;
        color: #4a1c61;
        margin-top: 20px;
        margin-bottom: 30px;
    }
    /* Navigation Bar Styles */
    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
        background: linear-gradient(135deg, #4a1c61, #6a2c91);
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .nav-logo {
        display: flex;
        align-items: center;
    }
    .nav-logo img {
        height: 40px;
        margin-right: 10px;
        border-radius: 50%;
    }
    .nav-links {
        display: flex;
        gap: 20px;
    }
    .nav-link {
        color: white;
        text-decoration: none;
        padding: 8px 15px;
        border-radius: 5px;
        transition: background-color 0.3s ease;
    }
    .nav-link:hover, .nav-link.active {
        background-color: rgba(255, 255, 255, 0.2);
    }
    .nav-login {
        background-color: white;
        color: #6a2c91;
        padding: 8px 15px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .nav-login:hover {
        background-color: #f0f0f0;
        transform: translateY(-2px);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    /* Rotating Updates Styles */
    .update-rotator {
        background: linear-gradient(145deg, #f0f0f0, #ffffff);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        overflow: hidden;
        position: relative;
    }
    .update-image {
        width: 150px;
        height: 100px;
        object-fit: cover;
        border-radius: 8px;
        margin-right: 20px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
    .update-content {
        flex: 1;
    }
    .update-region {
        font-weight: bold;
        color: #6a2c91;
        font-size: 1.2rem;
        margin-bottom: 5px;
    }
    .update-title {
        font-size: 1.1rem;
        margin-bottom: 5px;
    }
    .update-date {
        color: #666;
        font-size: 0.9rem;
    }
    .update-indicator {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-top: 10px;
    }
    .indicator-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #ddd;
    }
    .indicator-dot.active {
        background-color: #6a2c91;
    }
    /* Animation for elements */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animated {
        animation: fadeIn 0.5s ease-out forwards;
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

# Header
st.markdown("<div class='header'>🌍 Global Financial Regulations Hub</div>", unsafe_allow_html=True)

# Top Navigation Bar
nav_html = """
<div class="nav-container">
    <div class="nav-logo">
        <img src="https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=200&h=200&fit=crop&auto=format" alt="Logo">
        <span style="color: white; font-weight: bold; font-size: 1.2rem;">FinReg Hub</span>
    </div>
    <div class="nav-links">
        <a href="#" class="nav-link {}" id="home">Home</a>
        <a href="#" class="nav-link {}" id="updates">Latest Updates</a>
        <a href="#" class="nav-link {}" id="compliance">Compliance Report</a>
    </div>
    <a href="#" class="nav-login" id="login">Login</a>
</div>
"""

# Create columns for navigation
col1, col2, col3 = st.columns([1, 3, 1])

# Use session state to track the current page
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# JavaScript for handling navigation clicks
nav_js = """
<script>
document.getElementById('home').addEventListener('click', function() {
    window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'Home'}, '*');
});
document.getElementById('updates').addEventListener('click', function() {
    window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'Latest Updates'}, '*');
});
document.getElementById('compliance').addEventListener('click', function() {
    window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'Compliance Report'}, '*');
});
document.getElementById('login').addEventListener('click', function() {
    window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'Login'}, '*');
});
</script>
"""

# Determine active page for styling
home_active = "active" if st.session_state.page == "Home" else ""
updates_active = "active" if st.session_state.page == "Latest Updates" else ""
compliance_active = "active" if st.session_state.page == "Compliance Report" else ""

# Display the navigation bar with the correct active state
st.markdown(nav_html.format(home_active, updates_active, compliance_active) + nav_js, unsafe_allow_html=True)

# Create a component to handle navigation clicks
nav_component = st.empty()
page = nav_component.text_input("", value="", label_visibility="collapsed", key="nav_input")

# Update the page state if navigation changes
if page and page != st.session_state.page:
    st.session_state.page = page
    st.experimental_rerun()

# Rotating Updates Section (only on Home page)
if st.session_state.page == "Home":
    # Create a container for the rotating updates
    update_container = st.container()
    
    # Use session state to track the current update index
    if 'update_index' not in st.session_state:
        st.session_state.update_index = 0
        st.session_state.last_update_time = time.time()
    
    # Function to display the current update
    def display_current_update():
        current_update = updates[st.session_state.update_index]
        update_html = f"""
        <div class="update-rotator animated">
            <img src="{current_update['Image']}" class="update-image" alt="{current_update['Region']}">
            <div class="update-content">
                <div class="update-region">{current_update['Region']} Regulatory Update</div>
                <div class="update-title">{current_update['Update']}</div>
                <div class="update-date">{current_update['Date']}</div>
            </div>
        </div>
        <div class="update-indicator">
            {"".join([f'<div class="indicator-dot {"active" if i == st.session_state.update_index else ""}"></div>' for i in range(len(updates))])}
        </div>
        """
        update_container.markdown(update_html, unsafe_allow_html=True)
    
    # Display the current update
    display_current_update()
    
    # Auto-rotate updates every 5 seconds
    current_time = time.time()
    if current_time - st.session_state.last_update_time > 5:
        st.session_state.update_index = (st.session_state.update_index + 1) % len(updates)
        st.session_state.last_update_time = current_time
        st.experimental_rerun()
    
    st.markdown("<div class='subheader'>Stay ahead with the latest financial regulations</div>", unsafe_allow_html=True)

    # Key Features Section
    st.header("Key Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.1s;">
            <div class="feature-icon">📰</div>
            <h3>Real-Time Regulatory Updates</h3>
            <p>Track regulatory changes globally in real-time.</p>
            <button class="custom-button">Learn More</button>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.2s;">
            <div class="feature-icon">🤖</div>
            <h3>AI-Driven Risk Analysis</h3>
            <p>Identify compliance gaps and fraud risks with predictive analytics.</p>
            <button class="custom-button">Learn More</button>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.3s;">
            <div class="feature-icon">⚙️</div>
            <h3>Automated Audits</h3>
            <p>Ensure processes meet regulatory standards effortlessly.</p>
            <button class="custom-button">Learn More</button>
        </div>
        """, unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.4s;">
            <div class="feature-icon">🕵️</div>
            <h3>Fraud Detection & AML</h3>
            <p>Detect and prevent fraudulent activities with advanced ML algorithms.</p>
            <button class="custom-button">Learn More</button>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.5s;">
            <div class="feature-icon">📋</div>
            <h3>KYC Tools</h3>
            <p>Automate customer background checks for identity verification.</p>
            <button class="custom-button">Learn More</button>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="feature-card animated" style="animation-delay: 0.6s;">
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
        {"name": "New York", "lat": 40.7128, "lon": -74.0060, "size": 50, "color": [106, 44, 145]},
        {"name": "London", "lat": 51.5074, "lon": -0.1278, "size": 45, "color": [106, 44, 145]},
        {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "size": 40, "color": [106, 44, 145]},
        {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503, "size": 42, "color": [106, 44, 145]},
        {"name": "Sydney", "lat": -33.8688, "lon": 151.2093, "size": 38, "color": [106, 44, 145]},
        {"name": "Dubai", "lat": 25.2048, "lon": 55.2708, "size": 35, "color": [106, 44, 145]},
        {"name": "Frankfurt", "lat": 50.1109, "lon": 8.6821, "size": 37, "color": [106, 44, 145]},
        {"name": "São Paulo", "lat": -23.5505, "lon": -46.6333, "size": 36, "color": [106, 44, 145]},
        {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777, "size": 34, "color": [106, 44, 145]},
        {"name": "Shanghai", "lat": 31.2304, "lon": 121.4737, "size": 39, "color": [106, 44, 145]},
    ])

    # Create the PyDeck map
    view_state = pdk.ViewState(latitude=20, longitude=0, zoom=1.5, pitch=0)

    # Create the scatterplot layer
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position=["lon", "lat"],
        get_radius="size * 10000",
        get_fill_color="color",
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
    )

    # Create the deck
    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=view_state,
        layers=[scatter_layer],
        tooltip={"text": "{name}"},
    )

    # Display the map
    st.pydeck_chart(deck)

    # Pricing Section
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
            <td>Custom solutions, dedicated support, API access</td>
            <td><button class="custom-button">Contact Us</button></td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    # Testimonials Section
    st.header("What Our Clients Say")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin: 10px; background-color: #f9f9f9;">
            <p style="font-style: italic;">"This platform has revolutionized how we manage regulatory compliance. The real-time updates have saved us countless hours of manual monitoring."</p>
            <p style="text-align: right;"><strong>- Sarah Johnson, Compliance Officer at Global Bank</strong></p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin: 10px; background-color: #f9f9f9;">
            <p style="font-style: italic;">"The AI-driven risk analysis has helped us identify potential compliance issues before they become problems. Highly recommended for any financial institution."</p>
            <p style="text-align: right;"><strong>- Michael Chen, CTO at FinTech Innovations</strong></p>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2025 Global Financial Regulations Hub. All rights reserved.</p>
        <p>Contact: info@finreghub.com | +1 (555) 123-4567</p>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.page == "Latest Updates":
    # Expanded database of regulatory updates with links to official documents
    updates = [
        {
            "Region": "USA",
            "Update": "SEC Finalizes New Climate Disclosure Rules",
            "Date": "March 15, 2025",
            "Image": "https://images.unsplash.com/photo-1621944190310-e3cca1564bd7?w=800&h=600&fit=crop&auto=format",
            "Description": "The Securities and Exchange Commission has finalized rules requiring public companies to disclose climate-related financial risks and greenhouse gas emissions data in their registration statements and annual reports.",
            "Document": "https://www.sec.gov/news/press-release/2025-climate-disclosure",
            "Sector": "Climate, Corporate Disclosure"
        },
        {
            "Region": "EU",
            "Update": "ECB Updates Digital Euro Framework",
            "Date": "March 12, 2025",
            "Image": "https://images.unsplash.com/photo-1580674285054-bed31e145f59?w=800&h=600&fit=crop&auto=format",
            "Description": "The European Central Bank has released a comprehensive framework for the implementation of the Digital Euro, outlining technical specifications, privacy protections, and distribution mechanisms for the central bank digital currency.",
            "Document": "https://www.ecb.europa.eu/press/pr/date/2025/html/ecb.pr250312_1~digital-euro-framework.en.html",
            "Sector": "Digital Currency, Banking"
        },
        {
            "Region": "UK",
            "Update": "FCA Introduces Enhanced Consumer Protection Rules",
            "Date": "March 10, 2025",
            "Image": "https://images.unsplash.com/photo-1486299267070-83823f5448dd?w=800&h=600&fit=crop&auto=format",
            "Description": "The Financial Conduct Authority has implemented new rules to strengthen consumer protection in financial services, including stricter requirements for product suitability assessments and enhanced disclosure obligations for complex financial products.",
            "Document": "https://www.fca.org.uk/news/press-releases/fca-introduces-enhanced-consumer-protection-rules-2025",
            "Sector": "Consumer Protection, Financial Services"
        },
        {
            "Region": "China",
            "Update": "PBOC Announces New Capital Requirements for Digital Banks",
            "Date": "March 8, 2025",
            "Image": "https://images.unsplash.com/photo-1598257006458-087169a1f08d?w=800&h=600&fit=crop&auto=format",
            "Description": "The People's Bank of China has established new capital requirements specifically tailored for digital banking institutions, aiming to ensure financial stability while promoting innovation in the rapidly evolving digital finance sector.",
            "Document": "http://www.pbc.gov.cn/en/3688110/3688172/4437084/index.html",
            "Sector": "Digital Banking, Capital Requirements"
        },
        {
            "Region": "Singapore",
            "Update": "MAS Revises Digital Asset Licensing Framework",
            "Date": "March 5, 2025",
            "Image": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=800&h=600&fit=crop&auto=format",
            "Description": "The Monetary Authority of Singapore has revised its licensing framework for digital asset service providers, introducing a risk-based approach that categorizes providers based on the scale and nature of their operations.",
            "Document": "https://www.mas.gov.sg/news/media-releases/2025/mas-revises-digital-asset-licensing-framework",
            "Sector": "Digital Assets, Licensing"
        },
        {
            "Region": "UAE",
            "Update": "DFSA Implements New FinTech Regulations",
            "Date": "March 3, 2025",
            "Image": "https://images.unsplash.com/photo-1546412414-e1885e51cfa5?w=800&h=600&fit=crop&auto=format",
            "Description": "The Dubai Financial Services Authority has implemented new regulations to support the growth of FinTech innovation, including a specialized regulatory sandbox for testing novel financial products and services.",
            "Document": "https://www.dfsa.ae/news/dfsa-implements-new-fintech-regulations-2025",
            "Sector": "FinTech, Innovation"
        },
        {
            "Region": "Brazil",
            "Update": "CVM Updates Securities Regulations",
            "Date": "March 1, 2025",
            "Image": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=800&h=600&fit=crop&auto=format",
            "Description": "The Brazilian Securities Commission has updated regulations to enhance market transparency and investor protection, introducing new requirements for securities issuers and intermediaries.",
            "Document": "https://www.cvm.gov.br/noticias/cvm-updates-securities-regulations-2025",
            "Sector": "Securities, Investor Protection"
        },
        {
            "Region": "Germany",
            "Update": "BaFin Introduces Stricter AML Guidelines",
            "Date": "February 28, 2025",
            "Image": "https://images.unsplash.com/photo-1560969184-10fe8719e047?w=800&h=600&fit=crop&auto=format",
            "Description": "The Federal Financial Supervisory Authority has introduced stricter anti-money laundering guidelines for financial institutions, emphasizing risk-based customer due diligence and enhanced transaction monitoring requirements.",
            "Document": "https://www.bafin.de/EN/PublikationenDaten/Pressemitteilungen/2025/pm_250228_aml_guidelines.html",
            "Sector": "AML, Compliance"
        },
        {
            "Region": "Japan",
            "Update": "FSA Strengthens Digital Asset Regulations",
            "Date": "February 25, 2025",
            "Image": "https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?w=800&h=600&fit=crop&auto=format",
            "Description": "The Financial Services Agency has strengthened regulations governing digital assets and cryptocurrency exchanges, introducing new cybersecurity requirements and consumer protection measures.",
            "Document": "https://www.fsa.go.jp/en/news/2025/20250225.html",
            "Sector": "Digital Assets, Cybersecurity"
        }
    ]

    # Convert updates to DataFrame
    data = pd.DataFrame(updates)

    # Display updates with images and links
    st.write("### Browse All Updates")
    for update in updates:
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(update['Image'], use_container_width=True)
        with col2:
            st.markdown(f"<div class='update-container'>", unsafe_allow_html=True)
            st.markdown(f"### {update['Region']}: {update['Update']}")
            st.markdown(f"**Date:** {update['Date']} | **Sector:** {update['Sector']}")
            st.markdown(f"**Description:** {update['Description']}")
            st.markdown(f"[View Official Document]({update['Document']})")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

    # Filter options
    st.sidebar.header("Filter Updates")
    selected_region = st.sidebar.multiselect("Filter by Region", options=list(set([u["Region"] for u in updates])))
    selected_sector = st.sidebar.multiselect("Filter by Sector", options=list(set([u["Sector"] for u in updates])))

    if selected_region or selected_sector:
        filtered_data = data[
            (data["Region"].isin(selected_region) if selected_region else True) &
            (data["Sector"].isin(selected_sector) if selected_sector else True)
        ]
        st.write(f"### Filtered Results ({len(filtered_data)} updates)")
        for _, row in filtered_data.iterrows():
            col1, col2 = st.columns([2, 3])
            with col1:
                st.image(row['Image'], use_container_width=True)
            with col2:
                st.markdown(f"<div class='update-container'>", unsafe_allow_html=True)
                st.markdown(f"### {row['Region']}: {row['Update']}")
                st.markdown(f"**Date:** {row['Date']} | **Sector:** {row['Sector']}")
                st.markdown(f"**Description:** {row['Description']}")
                st.markdown(f"[View Official Document]({row['Document']})")
                st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

elif st.session_state.page == "Compliance Report":
    st.header("Compliance Report Generator")
    
    # Form for generating compliance report
    with st.form("compliance_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name")
            industry = st.selectbox("Industry", ["Banking", "Insurance", "Asset Management", "Payment Services", "Cryptocurrency", "Other"])
            jurisdiction = st.multiselect("Jurisdictions", ["USA", "EU", "UK", "China", "Singapore", "UAE", "Brazil", "Germany", "Japan", "Other"])
        
        with col2:
            report_type = st.selectbox("Report Type", ["Regulatory Gap Analysis", "Risk Assessment", "Compliance Audit", "Custom"])
            time_period = st.selectbox("Time Period", ["Q1 2025", "Q2 2025", "H1 2025", "2025 Full Year"])
            include_recommendations = st.checkbox("Include Recommendations", value=True)
        
        submit_button = st.form_submit_button("Generate Report")
    
    if submit_button:
        st.success("Report generation initiated! Your compliance report will be ready shortly.")
        
        # Simulated report generation
        st.header(f"Compliance Report: {company_name}")
        st.subheader(f"{report_type} for {time_period}")
        
        # Regulatory Updates Section
        st.markdown("### Relevant Regulatory Updates")
        
        # Filter updates based on selected jurisdictions
        relevant_updates = [update for update in updates if update["Region"] in jurisdiction]
        
        if relevant_updates:
            for update in relevant_updates[:3]:  # Show top 3 most relevant
                st.markdown(f"""
                **{update['Region']} - {update['Update']}** ({update['Date']})
                
                {update['Description']}
                
                [View Official Document]({update.get('Document', '#')})
                """)
        else:
            st.write("No specific regulatory updates found for the selected jurisdictions.")
        
        # Compliance Status
        st.markdown("### Compliance Status Overview")
        
        # Generate random compliance scores for demonstration
        import random
        compliance_data = {
            "AML/KYC Procedures": random.randint(70, 100),
            "Data Protection": random.randint(70, 100),
            "Financial Reporting": random.randint(70, 100),
            "Risk Management": random.randint(70, 100),
            "Corporate Governance": random.randint(70, 100)
        }
        
        # Convert to DataFrame for visualization
        compliance_df = pd.DataFrame({
            "Category": list(compliance_data.keys()),
            "Compliance Score": list(compliance_data.values())
        })
        
        # Display as bar chart
        st.bar_chart(compliance_df.set_index("Category"))
        
        # Risk Assessment
        st.markdown("### Risk Assessment")
        
        risk_areas = [
            {"Area": "Regulatory Change", "Risk Level": "Medium", "Impact": "Moderate", "Mitigation": "Continuous monitoring of regulatory updates"},
            {"Area": "Data Breach", "Risk Level": "High", "Impact": "Severe", "Mitigation": "Enhanced cybersecurity measures"},
            {"Area": "Financial Crime", "Risk Level": "Medium", "Impact": "Significant", "Mitigation": "Improved transaction monitoring"},
            {"Area": "Operational Failure", "Risk Level": "Low", "Impact": "Moderate", "Mitigation": "Robust business continuity planning"}
        ]
        
        # Display risk assessment table
        risk_df = pd.DataFrame(risk_areas)
        st.table(risk_df)
        
        # Recommendations if requested
        if include_recommendations:
            st.markdown("### Recommendations")
            
            recommendations = [
                "Implement automated regulatory change management system",
                "Enhance staff training on new regulatory requirements",
                "Upgrade transaction monitoring systems to detect emerging financial crime patterns",
                "Conduct quarterly compliance reviews to identify and address gaps",
                "Establish a dedicated regulatory liaison team for each major jurisdiction"
            ]
            
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
        
        # Download button (simulated)
        st.download_button(
            label="Download Full Report (PDF)",
            data="This would be a PDF report in a real implementation",
            file_name=f"{company_name}_Compliance_Report_{time_period}.pdf",
            mime="application/pdf"
        )

elif st.session_state.page == "Login":
    st.header("Login to Your Account")
    
    # Create login form
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); background-color: #f9f9f9;">
            <h3 style="color: #6a2c91; margin-bottom: 20px;">User Login</h3>
            <form>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Email Address</label>
                    <input type="email" placeholder="Enter your email" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold;">Password</label>
                    <input type="password" placeholder="Enter your password" style="width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ddd;">
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <div>
                        <input type="checkbox" id="remember">
                        <label for="remember">Remember me</label>
                    </div>
                    <a href="#" style="color: #6a2c91; text-decoration: none;">Forgot Password?</a>
                </div>
                <button class="custom-button" style="width: 100%;">Login</button>
            </form>
            <p style="text-align: center; margin-top: 15px;">Don't have an account? <a href="#" style="color: #6a2c91; text-decoration: none;">Sign Up</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="padding: 20px; height: 100%;">
            <h3 style="color: #6a2c91; margin-bottom: 20px;">Benefits of Registration</h3>
            <ul style="list-style-type: none; padding: 0;">
                <li style="margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="color: #6a2c91; font-size: 1.5rem; margin-right: 10px;">✓</span>
                    <span>Access to premium regulatory content</span>
                </li>
                <li style="margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="color: #6a2c91; font-size: 1.5rem; margin-right: 10px;">✓</span>
                    <span>Personalized compliance dashboard</span>
                </li>
                <li style="margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="color: #6a2c91; font-size: 1.5rem; margin-right: 10px;">✓</span>
                    <span>Regulatory update notifications</span>
                </li>
                <li style="margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="color: #6a2c91; font-size: 1.5rem; margin-right: 10px;">✓</span>
                    <span>Compliance report generation</span>
                </li>
                <li style="margin-bottom: 10px; display: flex; align-items: center;">
                    <span style="color: #6a2c91; font-size: 1.5rem; margin-right: 10px;">✓</span>
                    <span>Access to expert support</span>
                </li>
            </ul>
            <div style="margin-top: 20px;">
                <h4 style="color: #6a2c91;">Admin Access</h4>
                <p>If you're an administrator, please use your admin credentials to access the management console.</p>
                <button class="custom-button">Admin Login</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Admin section (simulated)
    st.markdown("---")
    admin_expander = st.expander("Admin Panel (Demo Only)")
    
    with admin_expander:
        st.write("### Admin Dashboard")
        st.write("Here you can manage regulatory updates and system settings.")
        
        # Add tabs for different admin functions
        admin_tab1, admin_tab2, admin_tab3 = st.tabs(["Add Update", "Edit Updates", "System Settings"])
        
        with admin_tab1:
            st.write("### Add New Regulatory Update")
            region = st.selectbox("Region", ["USA", "EU", "UK", "China", "Singapore", "UAE", "Brazil", "Germany", "Japan", "Other"])
            title = st.text_input("Update Title")
            description = st.text_area("Description")
            date = st.date_input("Date")
            
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
            st.checkbox("Enable Email Notifications", value=True)
            st.checkbox("Enable Two-Factor Authentication", value=True)
            st.slider("Session Timeout (minutes)", min_value=5, max_value=60, value=30)
            
            if st.button("Save Settings"):
                st.success("Settings saved successfully! (Simulated)")
