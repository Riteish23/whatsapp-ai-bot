from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.environ.get("WHATSAPP_TOKEN")
PHONE_ID = os.environ.get("PHONE_NUMBER_ID")
VERIFY_TOKEN = "ninelab123"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "verification failed", 403

    if request.method == "POST":
        data = request.json

        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            phone = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]

            reply = "Hello from your WhatsApp bot"

            url = f"https://graph.facebook.com/v18.0/{PHONE_ID}/messages"

            headers = {
                "Authorization": f"Bearer {TOKEN}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": phone,
                "text": {"body": reply}
            }

            requests.post(url, headers=headers, json=payload)

        except:
            pass

        return "ok", 200


@app.route("/")
def home():
    return "Bot running"
