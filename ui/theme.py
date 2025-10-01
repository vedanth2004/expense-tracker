import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        .stButton>button { border-radius: 8px; }
        </style>
    """, unsafe_allow_html=True)
