import streamlit as st
import sys
import os
import requests

# Add the parent directory to the path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logo_title import logo_title

# Page configuration
st.set_page_config(
    page_title="AutogenStudio Designer",
    page_icon="🎨",
    layout="wide"
)

# Minimize padding between sidebar and main content
st.markdown("""
<style>
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: none;
    }
    .stApp > div:first-child {
        margin: 0;
        padding: 0;
    }
    iframe {
        border: none;
        margin: 0;
        padding: 0;
    }
</style>
""", unsafe_allow_html=True)

# Embed the AutogenStudio Designer directly
designer_url = "http://127.0.0.1:8080"

# Check if the designer server is running on port 8080
try:
    response = requests.get(designer_url, timeout=2)
    server_active = response.status_code == 200 or response.status_code == 404
except Exception:
    server_active = False

if server_active:
    # Use iframe to embed the designer with full width and height
    st.components.v1.iframe(
        src=designer_url,
        width=None,  # Full width
        height=800,  # Full height
        scrolling=True
    )
else:
    st.warning("AutogenStudio is not running on port 8080. Please start the server and try again.")