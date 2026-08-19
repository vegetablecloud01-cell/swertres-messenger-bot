import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Environment Variables (Set these in Render Dashboard)
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "MY_SECURE_TOKEN_123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
# Replace with your actual public repository raw JSON link
GITHUB_JSON_URL = "https://raw.githubusercontent.com/vegetablecloud01-cell/swertres-messenger-bot/refs/heads/main/results.json"

@app.route('/', methods=['GET'])
def verify():
    # Webhook verification step for Meta for Developers setup
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification token mismatch", 403
    return "Hello World", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]
                message = messaging_event.get("message", {})
                text = message.get("text", "").lower()
                
                # Check for trigger keywords
                keywords = ["swertres", "result", "resulta", "3d", "hearing"]
                if any(keyword in text for keyword in keywords):
                    send_lotto_results(sender_id)
                    
    return "EVENT_RECEIVED", 200

def send_lotto_results(recipient_id):
    # Fetch latest data from GitHub static raw storage
    try:
        response = requests.get(GITHUB_JSON_URL, timeout=5)
        lotto_data = response.json()
        
        reply_text = (
    f"🎯 Swertres (3D Lotto) Results today:\n\n"
    f"🕒 2:00 PM: {lotto_data.get('2pm', 'No result')}\n"
    f"🕒 5:00 PM: {lotto_data.get('5pm', 'No result')}\n"
    f"🕒 9:00 PM: {lotto_data.get('9pm', 'No result')}\n\n"
    f"Disclaimer: Always cross-verify combinations with official PCSO channels."
)

    except Exception:
        reply_text = "Sorry, I am temporarily unable to fetch the live lotto results. Please try again later!"

    # Send message back via Meta Graph API
    url = f"https://facebook.com{PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": reply_text}
    }
    headers = {"Content-Type": "application/json"}
    requests.post(url, json=payload, headers=headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
