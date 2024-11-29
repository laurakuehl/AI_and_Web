import logging
import time
import streamlit as st # type: ignore
from api import think_of_character
from util import is_similar, process_answer, process_question

# Setting up a logger to track events and errors
logger = logging.getLogger(__name__)

# Defining categories for the game
CATEGORIES = ["actor", "musician", "politician", "athlete", "superhero", "villain", "children's cartoon character"]

def guessing_page():
    st.markdown("""
        <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50; /* Bright green */
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state variables
    if "guess_count" not in st.session_state:
        st.session_state["guess_count"] = 0  # Counts the number of guesses
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "character" not in st.session_state:
        st.session_state["character"] = None
    if "category" not in st.session_state:
        st.session_state["category"] = None
    if "category_guesses" not in st.session_state:
        st.session_state["category_guesses"] = {category: [] for category in CATEGORIES}

    st.markdown('<div class="title">Who Am I?</div>', unsafe_allow_html=True)

    # Start the game
    if st.button("Let me think of a person or fictional character...", key="start_button"):
        oai_response = think_of_character(
            prompt=f"""
                i am a game master of a guessing game and you assist me. Think of a popular person or fictional character
                belonging to one of the following categories: {CATEGORIES}.
                Give me just the full name and the category in your answer (e.g., 'John Doe, actor')
            """,
            system_instruction="i am the game master of a guessing game and you help me out."
        )
        response_text = oai_response.choices[0].message.content.strip()
        name, category = response_text.split(", ", 1)
        
        logger.info(f"The character is {name}, category: {category}")
        st.session_state["character"] = name
        print(st.session_state["character"])
        st.session_state["category"] = category
        st.session_state["chat_history"] = [("bot", "I have thought of a character! Try to guess who it is!")]

    # Display chat history
    for user_or_bot, message in st.session_state["chat_history"]:
        with st.chat_message(user_or_bot):
            st.markdown(message)

    # Chat input
    if user_message := st.chat_input("Type your question or guess here"):
        # Add user question to chat history
        st.session_state["chat_history"].append(("user", user_message))
        with st.chat_message("user"):
            st.markdown(user_message)
        # Count guess
        st.session_state["guess_count"] += 1

        # Process the question or guess using the LLM
        oai_response = think_of_character(
            prompt=f"""
                The person or character that has to be guessed is: {st.session_state["character"]}.
                This is the chat history: {st.session_state["chat_history"]}.
                The contestant now asked or guessed: {user_message}.
                Give a yes/no answer and let the contestant know how close they are to figuring out who the person/character is.

                If the contestant guessed the right character or person, answer: 
                'HOORAY, you guessed right!'
            """,
            system_instruction="You are the game master of a guessing game."
        )
        response = oai_response.choices[0].message.content.strip()

        # Add LLM response to chat history
        st.session_state["chat_history"].append(("bot", response))
        with st.chat_message("bot"):
            st.markdown(response)
        
        if "hooray" in response.lower():
            st.session_state["category_guesses"][st.session_state["category"]].append(st.session_state["guess_count"])
            st.balloons()
    
    # Buttons for "Give Up" and "Hint"
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Give up and reveal character", key="reveal_button"):
            if st.session_state["character"]:
                reveal_message = f"The character was: {st.session_state['character']}. Better luck next time!"
                st.session_state["chat_history"].append(("bot", reveal_message))
                with st.chat_message("bot"):
                    st.markdown(reveal_message)

                # Reset game
                st.session_state["character"] = None
                st.session_state["category"] = None
                st.session_state["chat_history"] = []
            else:
                st.error("Please start the game first!")
    with col2:
        if st.button("Hint", key="hint_button"):
            st.session_state["show_hint"] = True

    # Display categories as a hint
    if st.session_state.get("show_hint"):
        st.info(f"Hint: The character belongs to one of these categories: {', '.join(CATEGORIES)}")