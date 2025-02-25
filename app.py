import os
import requests
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Configurar la clave de API de OpenAI desde las variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verificación de Webhook
VERIFY_TOKEN = "afudeteam1324"

@app.route('/webhook', methods=['GET'])
def verify():
    """ Verifica el token de Facebook """
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token_sent == VERIFY_TOKEN:
        return challenge
    return "Invalid verification token", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """ Manejo de mensajes entrantes """
    data = request.get_json()

    if data and "entry" in data:
        for entry in data["entry"]:
            for message_event in entry.get("messaging", []):
                sender_id = message_event["sender"]["id"]

                if "message" in message_event:
                    message = message_event["message"]
                    if "text" in message:
                        user_message = message["text"]

                        # Generar respuesta con OpenAI GPT-4
                        bot_response = get_ai_response(user_message)

                        # Enviar la respuesta al usuario
                        send_message(sender_id, bot_response)

    return "Message processed", 200

def get_ai_response(user_message):
    """ Genera una respuesta usando OpenAI GPT-4 """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente amigable de Afudé, una empresa de insumos para tatuadores."},
                {"role": "user", "content": user_message}
            ]
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error en get_ai_response: {e}")
        return "Lo siento, hubo un problema con mi respuesta. Inténtalo de nuevo."

def send_message(recipient_id, message_text):
    """ Envía un mensaje al usuario a través de la API de Facebook """
    access_token = os.getenv("PAGE_ACCESS_TOKEN")
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={access_token}"
    headers = {"Content-Type": "application/json"}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error al enviar mensaje: {response.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)

