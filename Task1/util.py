import difflib 
import streamlit as st

def is_similar(user_input, correct_answer, threshold=0.8):
    similarity = difflib.SequenceMatcher(None, user_input, correct_answer).ratio()
    return similarity >= threshold

def process_question():
    # Set the state to True when Enter is pressed
    st.session_state.enter_question = True

def process_answer():
    # Set the state to True when Enter is pressed
    st.session_state.enter_answer = True
