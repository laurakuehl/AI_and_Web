import streamlit as st # type: ignore
from guessing_chat import guessing_page 
from stats import statistics

# Adding a sidebar with a page selection dropdown
page = st.sidebar.selectbox("Choose a page", ["main page", "statistics"])

# Initializing a session state variable to store inputs if it doesn't already exist
if "inputs" not in st.session_state:
    st.session_state["inputs"] = []
    
# Display the corresponding page 
if page == "main page":
    guessing_page()
elif page == "statistics":
    statistics()