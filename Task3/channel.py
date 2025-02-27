## channel.py - a simple message channel
##

from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import re
import json
import requests
import datetime
import os
from better_profanity import profanity
from Task3.scenario import load_scenarios, should_send_scenario, generate_scenario

# Class-based application configuration
class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = '1234rfcdse4567ujhbvfrt67890plmn' # change to something random, no matter what

# Create Flask app
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')  # configuration
app.app_context().push()  # create an app context before initializing db

CORS(app)

# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HUB_URL = 'http://vm146.rz.uni-osnabrueck.de/hub'
HUB_AUTHKEY = 'Crr-K24d-2N'
CHANNEL_AUTHKEY = 'w34567ztfghj'
CHANNEL_NAME = "Mind Benders"
CHANNEL_ENDPOINT = "http://vm146.rz.uni-osnabrueck.de/u044/Task3/channel.wsgi" # don't forget to adjust in the bottom of the file
# Create a relative path to the file
CHANNEL_FILE = os.path.join(BASE_DIR, "messages.json")
SCENARIO_FILE = "scenarios.json"
CHANNEL_TYPE_OF_SERVICE = 'aiweb24:chat'
MAX_MESSAGES = 20

# load profanity filter
profanity.load_censor_words() # default list

# define welcome message
WELCOME_MESSAGE = {
    "content": 
        """<strong>Welcome to Mind Benders: Fun Hypotheticals & 'What If?' Scenarios.</strong><br>
        Get creative and discuss about various hypothetical scenarios!<br><br>
        <span class="green-text">Kick-off:  What if aliens landed tomorrow? What's your survival plan?</span><br><br>
        Hint: If you need a new hypothetical, type '<strong>new scenario</strong>'.
        """,
    "sender": "WhatIfBot",
    "timestamp": datetime.datetime.now().isoformat(),
    "extra": "welcome"
}

# load scenarios
SCENARIOS = load_scenarios(file=SCENARIO_FILE)

def format_message(text):
    """ Convert *word* to <i>word</i> and _word_ to <strong>word</strong> """
    if not text:
        return ""

    formatted_text = text
    formatted_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted_text)
    formatted_text = re.sub(r'_(.*?)_', r'<strong>\1</strong>', formatted_text)
    formatted_text = formatted_text.replace("\n", "<br>")  # preserve line breaks

    return formatted_text

@app.cli.command('register')
def register_command():
    global CHANNEL_AUTHKEY, CHANNEL_NAME, CHANNEL_ENDPOINT

    # send a POST request to server /channels
    response = requests.post(HUB_URL + '/channels', headers={'Authorization': 'authkey ' + HUB_AUTHKEY},
                             data=json.dumps({
                                "name": CHANNEL_NAME,
                                "endpoint": CHANNEL_ENDPOINT,
                                "authkey": CHANNEL_AUTHKEY,
                                "type_of_service": CHANNEL_TYPE_OF_SERVICE,
                             }))

    if response.status_code != 200:
        print("Error creating channel: "+str(response.status_code))
        print(response.text)
        return

def check_authorization(request):
    global CHANNEL_AUTHKEY
    # check if Authorization header is present
    if 'Authorization' not in request.headers:
        return False
    # check if authorization header is valid
    if request.headers['Authorization'] != 'authkey ' + CHANNEL_AUTHKEY:
        return False
    return True

@app.route('/health', methods=['GET'])
def health_check():
    global CHANNEL_NAME
    if not check_authorization(request):
        return "Invalid authorization", 400
    return jsonify({'name':CHANNEL_NAME}),  200

# GET: Return list of messages
@app.route('/', methods=['GET'])
def home_page():
    if not check_authorization(request):
        return "Invalid authorization", 400
    # fetch channels from server
    return jsonify(read_messages())

# POST: Send a message
@app.route('/', methods=['POST'])
def send_message():
    global SCENARIOS

    # fetch channels from server
    # check authorization header
    if not check_authorization(request):
        return "Invalid authorization", 400
    # check if message is present
    message = request.json
    if not message:
        return "No message", 400
    if not 'content' in message:
        return "No content", 400
    if not 'sender' in message:
        return "No sender", 400
    if not 'timestamp' in message:
        return "No timestamp", 400
    if not 'extra' in message:
        extra = None
    else:
        extra = message['extra']
    # add message to messages
    messages = read_messages()

    # profanity filtering
    if profanity.contains_profanity(message["content"]):
        message["content"] = profanity.censor(message["content"], censor_char='$') # replaces bad words with $$$$

    # formatting message
    message["content"] = format_message(message["content"])

    messages.append({'content': message['content'],
                     'sender': message['sender'],
                     'timestamp': message['timestamp'],
                     'extra': extra,
                     })
    
    # enforce message limit
    if len(messages) > MAX_MESSAGES:
        messages = messages[-MAX_MESSAGES:]

    # check if it's the right time to send a "What if?" scenario
    if should_send_scenario(messages):
        bot_response = generate_scenario(SCENARIOS)
        messages.append(bot_response)

    save_messages(messages)
    return "OK", 200

def read_messages():
    global CHANNEL_FILE
    try:
        f = open(CHANNEL_FILE, 'r')
    except FileNotFoundError:
        return []
    try:
        messages = json.load(f)
    except json.decoder.JSONDecodeError:
        messages = []
    f.close()

    # add welcome message
    if len(messages)==0 or messages[0].get("extra") != "welcome":
        messages.insert(0, WELCOME_MESSAGE) # insert at the beginning
        save_messages(messages)

    return messages

def save_messages(messages):
    global CHANNEL_FILE
    with open(CHANNEL_FILE, 'w') as f:
        json.dump(messages, f)

# Start development web server
# run flask --app channel.py register
# to register channel with hub

if __name__ == '__main__':
    app.run(port=5001, debug=True)
