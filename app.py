import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "MY_SECURE_TOKEN_123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
GITHUB_JSON_URL = "https://githubusercontent.com"

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
    print(f"--- NEW INCOMING MESSAGING EVENT ---")
    print(json.dumps(data, indent=2))  # This prints the raw Facebook message to your logs
    
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                message = messaging_event.get("message", {})
                text = message.get("text", "").lower()
                
                print(f"User {sender_id} sent text: '{text}'")
                
                # Check keywords
                keywords = ["swertres", "result", "resulta", "3d", "hearing"]
                if any(keyword in text for keyword in keywords):
                    print("--> Keyword matched! Triggering send_lotto_results...")
                    send_lotto_results(sender_id)
                else:
                    print("--> Message did not contain any trigger keywords.")
                    
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
            f"Disclaimer: Always cross-verify combinations with official PCSO channels."
        )
    except Exception as e:
        print(f"ERROR: Failed to read results.json from GitHub: {e}")
        reply_text = "Pasensya na, unable to fetch results right now."

    url = "https://facebook.com"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": reply_text}
    }
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    
    print(f"Sending reply payload to user {recipient_id}...")
    fb_response = requests.post(url, json=payload, params=params, headers=headers)
    
    # This logs exactly what Facebook says back to us
    print(f"Facebook API Status Code: {fb_response.status_code}")
    print(f"Facebook API Response Body: {fb_response.text}")
