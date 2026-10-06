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

# Custom CSS overrides for Streamlit container padding
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
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")

def load_standalone_html():
    html_path = os.path.join(WEB_DIR, "index.html")
    css_path = os.path.join(WEB_DIR, "index.css")
    data_path = os.path.join(WEB_DIR, "data.js")
    app_path = os.path.join(WEB_DIR, "app.js")

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    with open(data_path, "r", encoding="utf-8") as f:
        data_content = f.read()

    with open(app_path, "r", encoding="utf-8") as f:
        app_content = f.read()

    # Inline CSS & JS into standalone HTML using lambda replacements to avoid escape sequence errors
    import re

    html_content = re.sub(
        r'<link rel="stylesheet" href="index\.css[^"]*">',
        lambda m: f'<style>\n{css_content}\n</style>',
        html_content
    )

    html_content = re.sub(
        r'<script src="data\.js[^"]*"></script>',
        lambda m: f'<script>\n{data_content}\n</script>',
        html_content
    )

    html_content = re.sub(
        r'<script src="app\.js[^"]*"></script>',
        lambda m: f'<script>\n{app_content}\n</script>',
        html_content
    )

    return html_content

standalone_html = load_standalone_html()

# Render component cleanly
components.html(standalone_html, height=2800, scrolling=True)
