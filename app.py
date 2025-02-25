import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = "afudeteam1324"  # El token que configuraste en Meta
PAGE_ACCESS_TOKEN = "TU_TOKEN_DE_PAGINA"

@app.route('/', methods=['GET'])
def home():
    return "El bot está funcionando."

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verifica el webhook con Facebook."""
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if token == VERIFY_TOKEN:
        return challenge
    return "Token de verificación incorrecto", 403

@app.route('/webhook', methods=['POST'])
def handle_message():
    """Recibe mensajes de Messenger y envía una respuesta."""
    data = request.get_json()

    if data.get("object") == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if "message" in messaging_event:
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]

                    send_message(sender_id, f"Recibí tu mensaje: {message_text}")

    return "EVENT_RECEIVED", 200

def send_message(recipient_id, text):
    """Envía un mensaje de vuelta al usuario."""
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
