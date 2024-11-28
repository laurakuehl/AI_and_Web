import os
import logging

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

# Create a logger instance to log messages
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()
CLIENT = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", ""),
)

# settings for the OpenAI chat completion API
DEFAULT_OPENAI_SETTINGS = {
    "model":"gpt-4o-mini",
    "max_tokens":None,
    "temperature":0.8,
    "top_p":0.8,
    "stop":None,
}


def think_of_character(prompt: str,
    system_instruction: str,
    open_ai_settings: dict = DEFAULT_OPENAI_SETTINGS
) -> ChatCompletion:
    """
    Generates text using OpenAIs chat completion model
    
    Args:
        prompt (str): User input or the main content to process.
        system_instruction (str): Instructions to guide the model's behavior.
        open_ai_settings (dict): OpenAI settings, with default values provided.

    Returns:
        ChatCompletion: The response from the OpenAI API.
    """
    
    # Log the details of the request
    logger.info(
        f"""Generating text from prompt: {prompt},
        system_instruction: {system_instruction},
        model: {open_ai_settings["model"]}.
        Settings are max_tokens: {open_ai_settings["max_tokens"]},
        temperature: {open_ai_settings["temperature"]},
        top_p: {open_ai_settings["top_p"]},
        stop: {open_ai_settings["stop"]}."""
    )
    
    # Send a request to OpenAI
    response = CLIENT.chat.completions.create(
        # settings for the request
        model=open_ai_settings["model"],
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt},
        ],
        max_tokens=open_ai_settings["max_tokens"],
        temperature=open_ai_settings["temperature"],
        top_p=open_ai_settings["top_p"],
        stop=open_ai_settings["stop"],
    )
    # save response in logger 
    logger.info(f"Received response from OpenAI: {response}")
    return response
