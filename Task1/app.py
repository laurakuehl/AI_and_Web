import streamlit as st
from guessing import guessing_page 
from stats import statistics


page = st.sidebar.selectbox("Choose a page", ["main page", "statistics"])

if "inputs" not in st.session_state:
    st.session_state["inputs"] = []

if page == "main page":
    guessing_page()
    
elif page == "statistics":
    statistics()