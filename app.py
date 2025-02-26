from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Token de verificación (debe coincidir con el de Facebook Developer)
VERIFY_TOKEN = "AfudeTeam1234"

# Token de acceso de la página (debes obtenerlo desde Facebook Developer)
PAGE_ACCESS_TOKEN = os.getenv("EAANlJsKDZCwYBO6mpkMXMu4jXYXCMOvim9xRFygiuEXICJNxI7GZBK9RLNZC0zxiZBwagR6cEjYb1TwmxMH7n5Vb8P5GBeX9lE3exUvZAFJsbtLHQAnpSeJZAI9xcvmUZADP4IYCaakVNEiys5PxWXrpIq74NzbWENi84xcUABnjzizzlKhwNz5lFRGFty5nGrs1aM0IXJLZCCMW3joawZAhzcV6sA65ZAEfh3MQZDZD")

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    """
    Verifica el webhook con Facebook.
    """
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Maneja los mensajes entrantes.
    """
    data = request.get_json()
    print("Datos recibidos:", data)  # Agrega esta línea para depurar
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_psid = messaging_event["sender"]["id"]
                if messaging_event.get("message"):
                    handle_message(sender_psid, messaging_event["message"])
    return "ok", 200

def handle_message(sender_psid, received_message):
    """
    Procesa el mensaje recibido y envía una respuesta.
    """
    message_text = received_message.get("text", "")
    if message_text:
        response_message = "Hola, soy un bot"
        call_send_api(sender_psid, response_message)
    else:
        call_send_api(sender_psid, "Solo puedo responder a mensajes de texto.")

def call_send_api(sender_psid, message):
    """
    Envía un mensaje al usuario usando la API de Messenger.
    """
    request_body = {
        "recipient": {"id": sender_psid},
        "message": {"text": message}
    }
    headers = {
        "Content-Type": "application/json"
    }
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    response = requests.post(url, json=request_body, headers=headers)
    if response.status_code != 200:
        print(f"No se pudo enviar el mensaje: {response.status_code} - {response.text}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Usa el puerto de la variable de entorno o 5000 por defecto
    app.run(host="0.0.0.0", port=port)