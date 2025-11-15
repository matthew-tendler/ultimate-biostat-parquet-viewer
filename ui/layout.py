import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="Ultimate Biostat Parquet Viewer",
        layout="wide"
    )

def render_sidebar():
    st.sidebar.title("Navigation")
    st.sidebar.write("More modules coming soon.")
