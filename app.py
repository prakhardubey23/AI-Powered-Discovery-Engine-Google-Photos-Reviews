import os
import re
import base64
import streamlit as st

# Configure Streamlit Page
st.set_page_config(
    page_title="Google Photos Feedback Discovery Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS overrides for full viewport layout
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
        iframe.dashboard-iframe {
            border: none;
            width: 100% !important;
            min-height: 2500px !important;
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

    # Replace stylesheet link with inline CSS
    html_content = re.sub(
        r'<link rel="stylesheet" href="index\.css[^"]*">',
        lambda m: f'<style>\n{css_content}\n</style>',
        html_content
    )

    # Replace data.js script tag with inline data.js
    html_content = re.sub(
        r'<script src="data\.js[^"]*"></script>',
        lambda m: f'<script>\n{data_content}\n</script>',
        html_content
    )

    # Replace app.js script tag with inline app.js
    html_content = re.sub(
        r'<script src="app\.js[^"]*"></script>',
        lambda m: f'<script>\n{app_content}\n</script>',
        html_content
    )

    return html_content

standalone_html = load_standalone_html()
b64_html = base64.b64encode(standalone_html.encode('utf-8')).decode('utf-8')

# Render as native base64 data URI iframe directly in st.markdown
st.markdown(
    f'<iframe class="dashboard-iframe" src="data:text/html;charset=utf-8;base64,{b64_html}"></iframe>',
    unsafe_allow_html=True
)
