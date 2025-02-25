from flask import Flask, request
import requests

app = Flask(__name__)

# Token de verificación para el webhook
VERIFY_TOKEN = 'afudeteam1324'  # Cambia esto por tu token de verificación
ACCESS_TOKEN = 'TU_TOKEN_DE_ACCESO'  # Reemplaza esto con tu token de acceso de Facebook

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificación del token de Facebook
        token = request.args.get('hub.verify_token')
        if token == VERIFY_TOKEN:
            return request.args.get('hub.challenge'), 200
        else:
            return "Token de verificación inválido", 403
    elif request.method == "POST":
        # Manejo de mensajes entrantes
        data = request.json
        process_message(data)
    return "Webhook recibido", 200

def process_message(data):
    # Verifica que el mensaje sea válido
    if "object" in data and data["object"] == "page":
        for entry in data["entry"]:
            messaging_events = entry.get("messaging", [])
            for event in messaging_events:
                sender_id = event["sender"]["id"]
                message_text = event["message"]["text"]
                respond_to_message(sender_id, message_text)

def respond_to_message(sender_id, message_text):
    # Lógica para generar una respuesta
    response_text = generate_response(message_text)  # Llama a la función para generar respuesta
    send_message(sender_id, response_text)

def generate_response(message_text):
    # Aquí puedes implementar lógica para personalizar la respuesta
    # Por ahora, devolveremos una respuesta genérica
    return "Gracias por tu mensaje. Aquí está la información que necesitaras."

def send_message(sender_id, response_text):
    # Envía un mensaje de vuelta al usuario
    url = f'https://graph.facebook.com/v12.0/me/messages?access_token={ACCESS_TOKEN}'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'recipient': {'id': sender_id},
        'message': {'text': response_text}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)