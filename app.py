import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "MY_SECURE_TOKEN_123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
# ⚠️ Ensure your real raw JSON link from your previous message is pasted here!
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
    print("--- INCOMING FACEBOOK PACKET ---")
    print(json.dumps(data))
    
    try:
        if data and "entry" in data:
            for entry in data["entry"]:
                if "messaging" in entry:
                    for messaging_event in entry["messaging"]:
                        sender_id = messaging_event["sender"]["id"]
                        
                        if "message" in messaging_event and "text" in messaging_event["message"]:
                            user_text = messaging_event["message"]["text"].lower()
                            print(f"Captured text from {sender_id}: '{user_text}'")
                            
                            keywords = ["swertres", "result", "resulta", "3d", "hearing", "nakatama"]
                            if any(k in user_text for k in keywords):
                                print("--> Match found! Dispatching numbers...")
                                send_lotto_results(sender_id)
    except Exception as e:
        print(f"Packet parsing exception: {e}")
        
    return "EVENT_RECEIVED", 200

def send_lotto_results(recipient_id):
    try:
        response = requests.get(GITHUB_JSON_URL, timeout=5)
        lotto_data = response.json()
        
        # FIXED: Uses .get() with fallback values so it NEVER crashes if a time slot is missing
        p2_result = lotto_data.get('2pm', lotto_data.get('11am', 'No result'))
        p5_result = lotto_data.get('5pm', lotto_data.get('4pm', 'No result'))
        p9_result = lotto_data.get('9pm', 'No result')
        updated_time = lotto_data.get('updated', 'N/A')
        
        reply_text = (
            f"🎯 PCSO Swertres Results Today:\n\n"
            f"🕒 2:00 PM: {p2_result}\n"
            f"🕒 5:00 PM: {p5_result}\n"
            f"🕒 9:00 PM: {p9_result}\n\n"
            f"Updated as of: {updated_time}\n\n"
            f"Disclaimer: Always cross-verify combinations with official PCSO channels."
        )
    except Exception as e:
        print(f"GitHub JSON Retrieval Error: {e}")
        reply_text = "Pasensya na, unable to fetch the live lotto results right now. Please try again later!"

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
