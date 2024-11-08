import streamlit as st

def statistics():
        
    st.title("Statistik über deine Eingaben")

    total_inputs = len(st.session_state["inputs"])
    unique_inputs = len(set(st.session_state["inputs"]))

    st.write(f"Anzahl der Eingaben: {total_inputs}")
    st.write(f"Anzahl der einzigartigen Eingaben: {unique_inputs}")

    st.write("Alle gespeicherten Eingaben:")
    st.write(st.session_state["inputs"])