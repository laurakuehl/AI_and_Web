import logging
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
    if "category_guesses" not in st.session_state:
        st.session_state["category_guesses"] = {category: [] for category in CATEGORIES}
    if "category" not in st.session_state:
        st.session_state["category"] = None
    if "character" not in st.session_state:
        st.session_state["character"] = None  

    st.title("Who Am I?")

    # Initialisierung des Button-Textes und Session-State
    if 'character' not in st.session_state:  # Wenn der Charakter noch nicht gesetzt wurde
        button_text = "Let me think of a person or fictional character..."
    else:
        button_text = "I have thought of a character!"
    
    if st.button("Let me think of a person or fictional character..."):
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
        st.session_state["guess_count"] = 0  
        st.session_state["inputs"] = []  
        st.session_state["responses"] = []  
        st.session_state.button_pressed = True 
    if 'button_pressed' in st.session_state and st.session_state.button_pressed:
        st.write("I have thought of a character!")

    
    user_input = st.text_input("Ask a yes/no question or guess the character!")

    if st.button("Speichern"):
        if user_input:
            st.session_state["inputs"].append(user_input)
            st.success("Input saved!")
            st.session_state["guess_count"] += 1  # Increment guess counter
            st.session_state["category_guesses"][st.session_state["category"]].append(user_input)
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

    if st.button("Give up and reveal character"):
        st.markdown(
            f"""
            <p style='font-size: 24px; font-weight: bold;'>
                I was thinking of 
                <span style='color: red; font-weight: bold;'>{st.session_state['character']}</span>
            </p>
            """,
            unsafe_allow_html=True
        )

    # Display the guess counter
    st.markdown(
        f"""
        <p style='font-size: 20px; font-weight: bold;'>
            <span style='color: blue;'>Guesses so far: {st.session_state['guess_count']}</span>
        </p>
        """,
        unsafe_allow_html=True
    )

    # Display previous inputs and responses
    if st.session_state["inputs"]:
        st.write("") 
        st.markdown(
            f"""
            <p style='font-size: 22px; font-weight: bold;'>
                <span style='color: black; font-weight: bold;'>Previous entries and answers:</span>
            </p>
            """,
            unsafe_allow_html=True
        )
        for i, input_text in enumerate(st.session_state["inputs"]):
            response = st.session_state["responses"][i]
            st.write(f"{i+1}: GUESS: {input_text}")
            st.write(f"{i+1}: RESPONSE: {response}")
            st.write("")
        


"""
TO DOs:
- Wenn ein neuer Charakter charakter generiert wird soll die Ausgabe von bisherigen Guesses und Responses zurückgesetzt werden.
- Wenn der name erraten wird (auch in minimal anderer rechtschreibung oder so), soll klar gesagt werden dass es richtig war, bis jetzt 
    er meistens nur dass es very close ist
- erst guesses annehmen wenn der character genereiert wurde (mit aufforderung dem button zu klicken oder so), ansosnten kommt es nach dem ersten guess zu komischen fehlermeldungen
- den button in ein textfeld ändern(Dennis)


Idee
- wenn wir zählen wie viele guesses eine Person in den Kategorien braucht. Benennen in welcher Kategorie man besser ist.
-


Meeting 22 Nov:
stats:
- guesses per category Dennis
- durchschnitt guesses übergreifend Dennis

guessing:
- erst guesses annehmen wenn der character genereiert wurde (mit aufforderung dem button zu klicken oder so) Konstantin
- Wenn ein neuer Charakter charakter generiert wird soll die Ausgabe von bisherigen Guesses und Responses zurückgesetzt werden Konstantin
- check if guess is correct (auch bei falscher rechtschreibung): baloons Laura
- save button in enter umändern Laura
- liste der guesses umdrehen Konstantin
- prompt engineering: Qualität der Antworten verbessern Laura
- ausprobieren, ob das Einfügen der ganzen Konversation in den Prompt hilft
- spezifizieren wie die Rückmeldung sein soll (entweder durch genauere Beschreibung oder durch Beispiele von Antwortmöglichkeiten)
"""