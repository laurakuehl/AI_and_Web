import streamlit as st

def guessing_page():
    if "inputs" not in st.session_state:
        st.session_state["inputs"] = []

    st.title("Lustiges Ratespiel")
    user_input = st.text_input("Gib deinen Text hier ein:")

    if st.button("Speichern"):
        if user_input:
            st.session_state["inputs"].append(user_input)
            st.success("Eingabe gespeichert!")

    st.write("Bisherige Eingaben:")
    st.write(st.session_state["inputs"])

    
    
