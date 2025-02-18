import json
import datetime
import random

# load "What if?" scenarios
def load_scenarios(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []
    
def should_send_scenario(messages, n_messages=10, keywords=["what should we discuss now?", "new hypothetical", "new scenario"]):
    """
    Determines if the bot should send a 'What if?' question.
    Conditions:
    1. If the last few messages (e.g., last 10) are not from the bot.
    2. If a trigger keyword appears in the chat.
    """
    if len(messages) < 2:
        return False  # Not enough messages to trigger a scenario

    # last 10 messages are from users (not the bot)
    last_senders = [msg['sender'] for msg in messages[-n_messages:]]
    if all(sender != "WhatIfBot" for sender in last_senders):
        return True

    # find the index of the last bot message
    last_bot_index = None
    for i in range(len(messages) - 1, -1, -1):  # Iterate backwards
        if messages[i]['sender'] == "WhatIfBot":
            last_bot_index = i
            break
    
    # extract messages sent after the last bot response
    user_messages_since_bot = messages[last_bot_index + 1:]

    # keyword trigger
    for msg in user_messages_since_bot:
        if any(keyword in msg['content'].lower() for keyword in keywords):
            return True

    return False

def generate_scenario(scenarios):
    """ Picks a random 'What if?' question and formats it as a bot response. """
    if not scenarios:
        return {
            "content": "Oops! I have no more scenarios left. Someone forgot to feed me more ideas!",
            "sender": "WhatIfBot",
            "timestamp": datetime.datetime.now().isoformat(),
            "extra": "bot"
        }

    scenario = random.choice(scenarios)
    return {
        "content": scenario,
        "sender": "WhatIfBot",
        "timestamp": datetime.datetime.now().isoformat(),
        "extra": "bot"
    }