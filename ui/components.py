import streamlit as st

def nav_bar(items: list[str]) -> str:
    return st.sidebar.radio("Navigation", items)
