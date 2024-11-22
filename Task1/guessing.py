import logging
import time
import streamlit as st
from api import think_of_character

logger = logging.getLogger(__name__)

CATEGORIES = ["actor", "musician", "politician", "athlete", "superhero", "villain", "children's cartoon character"]

def guessing_page():
    # Initialize session state variables if not already present
    if "inputs" not in st.session_state:
        st.session_state["inputs"] = []
    if "responses" not in st.session_state:
        st.session_state["responses"] = []
    if "guess_count" not in st.session_state:
        st.session_state["guess_count"] = 0
    if "enter_pressed" not in st.session_state:
        st.session_state["enter_pressed"] = False

    st.title("Who Am I?")

    # Initialize button text and session-state
    if st.button("Let me think of a person or fictional character..."):
        oai_response = think_of_character(
            prompt=f"""
                i am a game master of a guessing game and you assist me. Think of a popular person or fictional character
                belonging to one of the following categories: {CATEGORIES}.
                Give me just the full name in your answer
            """,
            system_instruction="i am the game master of a guessing game and you help me out."
        )
        logger.info(f"The character is {oai_response.choices[0].message.content}")
        st.session_state["character"] = oai_response.choices[0].message.content
        st.session_state["guess_count"] = 0  
        st.session_state["inputs"] = []  
        st.session_state["responses"] = []  
        st.session_state.button_pressed = True 
    if 'button_pressed' in st.session_state and st.session_state.button_pressed:
        st.write("I have thought of a character!")

    
    user_input = st.text_input("Ask a yes/no question or guess the character!")
    # Trigger action only once when Enter is pressed
    if user_input and not st.session_state.enter_pressed:
        st.session_state.enter_pressed = True

    if st.session_state.enter_pressed:
        if "character" in st.session_state:
            if user_input:
                st.session_state["inputs"].append(user_input)
                st.session_state["guess_count"] += 1  # Increment guess counter
                # create a sucess message that dissapears after a few seconds
                # so that it can reappear after pressing enter again
                placeholder = st.empty()
                with placeholder:
                    st.success("Your guess will be processed...")
                time.sleep(3)
                placeholder.empty()

            oai_response = think_of_character(
                prompt=f"""
                    The person or character that has to be guessed is: {st.session_state["character"]}.
                    The contestant asked or guessed: {st.session_state["inputs"][-1]}.
                    Give a yes/ no answer and let the contestant know how close they are to figuring out who the person/ character is.
                """,
                system_instruction="You are the game master of a guessing game."
            )
            logger.info(f"OpenAI's response: {oai_response.choices[0].message.content}")
            st.session_state["responses"].append(oai_response.choices[0].message.content)
            st.write(oai_response.choices[0].message.content)
        else:
              st.write("Generate character first!")

    # Display the guess counter
    st.write(f"Guesses so far: {st.session_state['guess_count']}")

    # Display previous inputs and responses
    if st.session_state["inputs"]:
        st.write("") 
        st.write(f"Previous entries and answers:")
        for i, input_text in enumerate(st.session_state["inputs"]):
            response = st.session_state["responses"][i]
            st.write(f"{i+1}: GUESS: {input_text}")
            st.write(f"{i+1}: RESPONSE: {response}")
            st.write("")
    
    if st.button("Give up and reveal character"):
        if "character" in st.session_state:
            st.write(f"{st.session_state['character']}")
        else:
            st.write("Generate character first!")
        