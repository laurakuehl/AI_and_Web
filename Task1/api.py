import os
import logging

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

logger = logging.getLogger(__name__)

load_dotenv()
CLIENT = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY", ""),
    organization=os.environ.get("OPENAI_ORG_ID", ""),
)

DEFAULT_OPENAI_SETTINGS = {
    "model":"gpt-4",
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
    """
    logger.info(
        f"""Generating text from prompt: {prompt},
        system_instruction: {system_instruction},
        model: {open_ai_settings["model"]}.
        Settings are max_tokens: {open_ai_settings["max_tokens"]},
        temperature: {open_ai_settings["temperature"]},
        top_p: {open_ai_settings["top_p"]},
        stop: {open_ai_settings["stop"]}."""
    )
    response = CLIENT.chat.completions.create(
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

    logger.info(f"Received response from OpenAI: {response}")
    return response
