import logging
import time
import streamlit as st # type: ignore
from api import think_of_character
from util import is_similar, process_answer, process_question

logger = logging.getLogger(__name__)

CATEGORIES = ["actor", "musician", "politician", "athlete", "superhero", "villain", "children's cartoon character"]

def guessing_page():
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
        st.session_state["inputs"] = []
    if "responses" not in st.session_state:
        st.session_state["responses"] = []
    if "guess_count" not in st.session_state:
        st.session_state["guess_count"] = 0
    if "enter_question" not in st.session_state:
        st.session_state["enter_question"] = False
    if "enter_answer" not in st.session_state:
        st.session_state["enter_answer"] = False
    if "category_guesses" not in st.session_state:
        st.session_state["category_guesses"] = {category: [] for category in CATEGORIES}
    if "category" not in st.session_state:
        st.session_state["category"] = None
    if "character" not in st.session_state:
        st.session_state["character"] = None


    st.markdown('<div class="title">Who Am I?</div>', unsafe_allow_html=True)

    # Initialize button text and session-state

    
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
        st.session_state["category"] = category 
        print(st.session_state.character)
        st.session_state["guess_count"] = 0  
        st.session_state["inputs"] = []  
        st.session_state["responses"] = []
        st.write("I have thought of a character!")

    
    user_input = st.text_input("Ask a yes/no question or guess the character!", on_change=process_question)

    if st.session_state.enter_question:
        if "character" in st.session_state:
            if user_input:
                st.session_state["inputs"].append(user_input)
                st.session_state["guess_count"] += 1  
                with st.spinner("Processing your guess..."):
                    time.sleep(2)

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
            st.success(f"Response: {oai_response.choices[0].message.content}")
            # Reset
            st.session_state.enter_question = False
        else:
              st.error("Please generate a character first.")
              # Reset
              st.session_state.enter_question = False
    

    answer_input = st.text_input("Put in your final guess here:", on_change=process_answer)

    if st.session_state.enter_answer:
        if is_similar(answer_input, st.session_state.character):
            st.session_state["category_guesses"][st.session_state["category"]].append(st.session_state["guess_count"])
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

            for t in chatlist:
                st.write(t)


    if st.button("Give up and reveal character"):
        if "character" in st.session_state:
            st.session_state["category_guesses"][st.session_state["category"]].append(st.session_state["guess_count"])
            st.warning(f"The character was: {st.session_state['character']}")
            # Clear session state
            st.session_state["inputs"] = []
            st.session_state["responses"] = []
            # Clear the output placeholder
            output_placeholder.empty()
        else:
            st.error("Generate character first!")
