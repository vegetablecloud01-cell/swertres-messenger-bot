import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Environment Variables (Managed inside Render Dashboard)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "MY_SECURE_TOKEN_123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
# ⚠️ REPLACE THIS with your actual public repository raw JSON link!
GITHUB_JSON_URL = "https://raw.githubusercontent.com/vegetablecloud01-cell/swertres-messenger-bot/refs/heads/main/results.json"

@app.route('/', methods=['GET'])
def verify():
    # Webhook verification step for Meta Developer Dashboard
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification token mismatch", 403
    return "Bot Server Online", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("--- INCOMING FACEBOOK PACKET ---")
    print(json.dumps(data))
    
    # Flexible parser to extract messaging text events safely
    try:
        if data and "entry" in data:
            for entry in data["entry"]:
                if "messaging" in entry:
                    for messaging_event in entry["messaging"]:
                        sender_id = messaging_event["sender"]["id"]
                        
                        # Verify the packet contains a text string
                        if "message" in messaging_event and "text" in messaging_event["message"]:
                            user_text = messaging_event["message"]["text"].lower()
                            print(f"Captured text from {sender_id}: '{user_text}'")
                            
                            # Standard Philippine Lotto search triggers
                            keywords = ["swertres", "result", "resulta", "3d", "hearing", "nakatama"]
                            if any(k in user_text for k in keywords):
                                print("--> Match found! Dispatching numbers...")
                                send_lotto_results(sender_id)
                            else:
                                print("--> No keyword triggers matched.")
    except Exception as e:
        print(f"Packet parsing exception skipped: {e}")
        
    return "EVENT_RECEIVED", 200

def send_lotto_results(recipient_id):
    try:
        # Fetch the real-time combinations tracked by your scraper
        response = requests.get(GITHUB_JSON_URL, timeout=5)
        lotto_data = response.json()
        
        reply_text = (
            f"🎯 PCSO Swertres Results Today:\n\n"
            f"🕒 2:00 PM: {lotto_data.get('2pm', 'No result')}\n"
            f"🕒 5:00 PM: {lotto_data.get('5pm', 'No result')}\n"
            f"🕒 9:00 PM: {lotto_data.get('9pm', 'No result')}\n\n"
            f"Updated as of: {lotto_data.get('updated', 'N/A')}\n\n"
            f"Disclaimer: Always cross-verify combinations with official PCSO channels."
        )
    except Exception as e:
        print(f"GitHub JSON Retrieval Error: {e}")
        reply_text = "Pasensya na, unable to fetch the live lotto results right now. Please try again later!"

    # Corrected Graph API endpoint structure passing the access token as a param string
    url = "https://facebook.com"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": reply_text}
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    
    print(f"Sending response payload to user {recipient_id}...")
    res = requests.post(url, json=payload, params=params, headers=headers)
    print(f"Meta Server Response Status: {res.status_code}")
    print(f"Meta Server Response Body: {res.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Environment Variables (Managed inside Render Dashboard)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "MY_SECURE_TOKEN_123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
# ⚠️ REPLACE THIS with your actual public repository raw JSON link!
GITHUB_JSON_URL = "https://githubusercontent.com"

@app.route('/', methods=['GET'])
def verify():
    # Webhook verification step for Meta Developer Dashboard
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification token mismatch", 403
    return "Bot Server Online", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("--- INCOMING FACEBOOK PACKET ---")
    print(json.dumps(data))
    
    # Flexible parser to extract messaging text events safely
    try:
        if data and "entry" in data:
            for entry in data["entry"]:
                if "messaging" in entry:
                    for messaging_event in entry["messaging"]:
                        sender_id = messaging_event["sender"]["id"]
                        
                        # Verify the packet contains a text string
                        if "message" in messaging_event and "text" in messaging_event["message"]:
                            user_text = messaging_event["message"]["text"].lower()
                            print(f"Captured text from {sender_id}: '{user_text}'")
                            
                            # Standard Philippine Lotto search triggers
                            keywords = ["swertres", "result", "resulta", "3d", "hearing", "nakatama"]
                            if any(k in user_text for k in keywords):
                                print("--> Match found! Dispatching numbers...")
                                send_lotto_results(sender_id)
                            else:
                                print("--> No keyword triggers matched.")
    except Exception as e:
        print(f"Packet parsing exception skipped: {e}")
        
    return "EVENT_RECEIVED", 200

def send_lotto_results(recipient_id):
    try:
        # Fetch the real-time combinations tracked by your scraper
        response = requests.get(GITHUB_JSON_URL, timeout=5)
        lotto_data = response.json()
        
        reply_text = (
            f"🎯 PCSO Swertres Results Today:\n\n"
            f"🕒 2:00 PM: {lotto_data.get('2pm', 'No result')}\n"
            f"🕒 5:00 PM: {lotto_data.get('5pm', 'No result')}\n"
            f"🕒 9:00 PM: {lotto_data.get('9pm', 'No result')}\n\n"
            f"Updated as of: {lotto_data.get('updated', 'N/A')}\n\n"
            f"Disclaimer: Always cross-verify combinations with official PCSO channels."
        )
    except Exception as e:
        print(f"GitHub JSON Retrieval Error: {e}")
        reply_text = "Pasensya na, unable to fetch the live lotto results right now. Please try again later!"

    # Corrected Graph API endpoint structure passing the access token as a param string
    url = "https://facebook.com"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": reply_text}
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    
    print(f"Sending response payload to user {recipient_id}...")
    res = requests.post(url, json=payload, params=params, headers=headers)
    print(f"Meta Server Response Status: {res.status_code}")
    print(f"Meta Server Response Body: {res.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "MY_SECURE_TOKEN_123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
# Make sure your real raw GitHub data link is placed below!
GITHUB_JSON_URL = "https://raw.githubusercontent.com/vegetablecloud01-cell/swertres-messenger-bot/refs/heads/main/results.json"

@app.route('/', methods=['GET'])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification token mismatch", 403
    return "Bot Server Online", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("--- INCOMING FACEBOOK PACKET ---")
    print(json.dumps(data))
    
    # Super flexible parser - extracts message regardless of nesting structure
    try:
        if data and "entry" in data:
            for entry in data["entry"]:
                if "messaging" in entry:
                    for messaging_event in entry["messaging"]:
                        sender_id = messaging_event["sender"]["id"]
                        
                        # Verify it's a real text message event
                        if "message" in messaging_event and "text" in messaging_event["message"]:
                            user_text = messaging_event["message"]["text"].lower()
                            print(f"Captured text from {sender_id}: {user_text}")
                            
                            # Trigger phrases
                            keywords = ["swertres", "result", "resulta", "3d", "hearing", "nakatama"]
                            if any(k in user_text for k in keywords):
                                send_lotto_results(sender_id)
    except Exception as e:
        print(f"Parsing skip error: {e}")
        
    return "EVENT_RECEIVED", 200

def send_lotto_results(recipient_id):
    try:
        response = requests.get(GITHUB_JSON_URL, timeout=5)
        lotto_data = response.json()
        
        reply_text = (
            f"🎯 PCSO Swertres Results Today:\n\n"
            f"🕒 2:00 PM: {lotto_data.get('2pm', 'No result')}\n"
            f"🕒 5:00 PM: {lotto_data.get('5pm', 'No result')}\n"
            f"🕒 9:00 PM: {lotto_data.get('9pm', 'No result')}\n\n"
            f"Updated as of: {lotto_data.get('updated', 'N/A')}\n\n"
            f"Disclaimer: Always cross-verify combinations with official PCSO channels."
        )
    except Exception as e:
        print(f"GitHub Fetch Error: {e}")
        reply_text = "Pasensya na, unable to fetch the live lotto results right now."

    # Meta Graph Messaging endpoint
    url = f"https://facebook.com"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": reply_text}
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    
    print(f"Sending request packet to Meta...")
    res = requests.post(url, json=payload, params=params, headers=headers)
    print(f"Meta Response Code: {res.status_code}")
    print(f"Meta Server Text: {res.text}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
