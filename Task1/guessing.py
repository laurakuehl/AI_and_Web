import logging
import streamlit as st
from api import think_of_character

logger = logging.getLogger(__name__)

CATEGORIES = ["actor", "musician", "politician", "athlete", "superhero", "villain", "children's cartoon character"]

def guessing_page():
    if "inputs" not in st.session_state:
        st.session_state["inputs"] = []

    st.title("Who Am I?")

    # Initialisierung des Button-Textes und Session-State
    if 'character' not in st.session_state:  # Wenn der Charakter noch nicht gesetzt wurde
        button_text = "Let me think of a person or fictional character..."
    else:
        button_text = "I have thought of a character!"
    
    if st.button("Let me think of a person or fictional character..."):
        oai_response = think_of_character(
            prompt= f"""
                Think of a popular person or fictional character
                belonging to one of the following categpries: {CATEGORIES}.
                Give me just the full name.
            """,
            system_instruction="You are the game master of a guessing game."
        )
        logger.info(f"The character is {oai_response.choices[0].message.content}")
        st.session_state["character"] = oai_response.choices[0].message.content
        st.session_state.button_pressed = True 
    if 'button_pressed' in st.session_state and st.session_state.button_pressed:
        st.button("I have thought of a character!")

    
    user_input = st.text_input("Ask a yes/no question or guess the character!")

    if st.button("Speichern"):
        if user_input:
            st.session_state["inputs"].append(user_input)
            st.success("Input saved!")
        
        oai_response = think_of_character(
            prompt= f"""
                The person or character that has to be guessed is: {st.session_state["character"]}.
                The contestant asked or guessed: {st.session_state["inputs"][-1]}.
                Give a yes/ no answer and let the contestant know how close they are to figuring out who the person/ character is.
            """,
            system_instruction="You are the game master of a guessing game."
        )
        logger.info(f"OpenAI's response: {oai_response.choices[0].message.content}")
        st.write(oai_response.choices[0].message.content)

    if st.session_state["inputs"]:
        st.write("Bisherige Eingaben:")
        st.write(st.session_state["inputs"])

    
    
