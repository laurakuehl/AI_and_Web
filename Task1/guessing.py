import logging
import time
import streamlit as st
from api import think_of_character
from util import is_similar, process_answer, process_question

# Setting up a logger to track events and errors
logger = logging.getLogger(__name__)

# Defining categories for the game
CATEGORIES = ["actor", "musician", "politician", "athlete", "superhero", "villain", "children's cartoon character"]

def guessing_page():
    """
    This function renders the main page of the guessing game.
    It manages the game flow, handles user inputs, and interacts with the AI model.
    """
    
    # Adding custom styling for the Streamlit page using CSS
    st.markdown("""
        <style>
        .css-1d391kg * {
            color: #333333 !important;
        }

        .title {
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            margin-bottom: 20px;
        }

        .button {
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }

        .chat-history {
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
        }

        .chat-entry {
            font-family: 'Courier New', Courier, monospace;
            margin-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    
    # Initialize session state variables if not already present
    if "inputs" not in st.session_state:
        st.session_state["inputs"] = []  # Stores user's questions or guesses
    if "responses" not in st.session_state:
        st.session_state["responses"] = []  # Stores AI's responses
    if "guess_count" not in st.session_state:
        st.session_state["guess_count"] = 0  # Counts the number of guesses
    if "enter_question" not in st.session_state:
        st.session_state["enter_question"] = False  # Flag to track if a question is being processed
    if "enter_answer" not in st.session_state:
        st.session_state["enter_answer"] = False  # Flag to track if a final answer is being processed


    st.markdown('<div class="title">Who Am I?</div>', unsafe_allow_html=True)

    # Button to start the game and generate a character
    if st.button("Think of a person or fictional character!", key="start_button"):
        # Sending a prompt to the AI to generate a character
        oai_response = think_of_character(
            prompt=f"""
                i am a game master of a guessing game and you assist me. Think of a popular person or fictional character
                belonging to one of the following categories: {CATEGORIES}.
                Give me just the full name in your answer
            """,
            system_instruction="i am the game master of a guessing game and you help me out."
        )
        #logger and session states to store information during a session
        logger.info(f"The character is {oai_response.choices[0].message.content}")
        st.session_state["character"] = oai_response.choices[0].message.content
        print(st.session_state.character)
        st.session_state["guess_count"] = 0  
        st.session_state["inputs"] = []  
        st.session_state["responses"] = []
        st.write("I have thought of a character!") #Notify user

    
    user_input = st.text_input("Ask a yes/no question or guess the character!", on_change=process_question)

    # Processing user's questions
    if st.session_state.enter_question:
        if "character" in st.session_state:
            if user_input:
                st.session_state["inputs"].append(user_input)
                st.session_state["guess_count"] += 1  
                with st.spinner("Processing your guess..."):
                    time.sleep(2) # Simulate processing delay

            # Sending the user's input to the AI and receiving a response
            oai_response = think_of_character(
                prompt=f"""
                    The person or character that has to be guessed is: {st.session_state["character"]}.
                    The contestant asked or guessed: {st.session_state["inputs"][-1]}.
                    Give a yes/ no answer and let the contestant know how close they are to figuring out who the person/ character is.
                """,
                system_instruction="You are the game master of a guessing game."
            )
            
            # Logging and storing the AI's response
            logger.info(f"OpenAI's response: {oai_response.choices[0].message.content}")
            st.session_state["responses"].append(oai_response.choices[0].message.content)
            st.success(f"Response: {oai_response.choices[0].message.content}") # Display the response
            # Reset
            st.session_state.enter_question = False
        else:
              st.error("Please generate a character first.") # Error if no character is generated
              # Reset
              st.session_state.enter_question = False
    
    # Input field for the user to submit their final answer
    answer_input = st.text_input("Put in your final guess here:", on_change=process_answer)

    # Processing user's final answer
    if st.session_state.enter_answer:
        if is_similar(answer_input, st.session_state.character):
            st.balloons()
            st.session_state.enter_answer = False
        else:
            st.error("Your guess is incorrect!")
            st.session_state.enter_answer = False

    # Display the guess counter
    st.info(f"Guesses so far: {st.session_state['guess_count']}")
    # Create placeholders for outputs
    output_placeholder = st.empty()
    
    # Display previous inputs and responses
    with output_placeholder.container():
        if st.session_state["inputs"]:
            st.markdown('<div class="chat-history">Chat History:</div>', unsafe_allow_html=True)
            #create list of past questions and responses and print it
            chatlist = []
            for i, input_text in enumerate(st.session_state["inputs"]):
                if i >= len(st.session_state["responses"]):
                    st.session_state["responses"].append("No response yet.")
                response = st.session_state["responses"][i]
                
                chatlist.insert(0, f"{i+1}: GUESS: {input_text}")
                chatlist.insert(0, f"{i+1}: RESPONSE: {response}")
                chatlist.insert(0, "")

            # Displaying the chat history
            for t in chatlist:
                st.write(t)

    # Button to reveal the character and reset the game
    if st.button("Give up and reveal character"):
        if "character" in st.session_state:
            st.warning(f"The character was: {st.session_state['character']}")
            # Clear session state for a new game
            st.session_state["inputs"] = []
            st.session_state["responses"] = []
            # Clear the output placeholder
            output_placeholder.empty()
        else:
            st.error("Generate character first!") # Error if no character exists
