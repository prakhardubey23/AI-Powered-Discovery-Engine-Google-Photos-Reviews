import os
import streamlit as st
import streamlit.components.v1 as components

# Configure Streamlit Page
st.set_page_config(
    page_title="Google Photos Feedback Discovery Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS overrides for full-viewport canvas
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
        iframe {
            border: none;
            width: 100% !important;
            height: 100vh !important;
            min-height: 900px !important;
        }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")

# Declare custom component serving the web directory statically
# This serves index.html, index.css, data.js, and app.js as HTTP assets
# completely avoiding WebSocket payload size limits or blank page issues.
_discovery_dashboard = components.declare_component(
    "discovery_dashboard",
    path=WEB_DIR
)

# Render component
_discovery_dashboard()
