from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Token de verificación (debe coincidir con el de Facebook Developer)
VERIFY_TOKEN = "AfudeTeam1234"

# Token de acceso de la página (debes obtenerlo desde Facebook Developer)
PAGE_ACCESS_TOKEN = os.getenv("EAANlJsKDZCwYBO1VLcjXVqXAJbm2AcsEKjds5BD5uBvVWZCixZAizRXJnfJZCk0c8OljooQJ0LpdXjDX08wI8fPzMZA3OpXqCNUk7ZBWDPbqeFUOOlLk5LLitvs0zwUWs0JXzzlpDo3qZAbbZCdMJQ41lylpOKMwu5gZC7gYiWxNqp6AbENIMwPWKQf7e7X3VZBXx3y03JnRWdZBbMz8KEZD")

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
    print("Solicitud POST recibida en /webhook")  # Confirma que la solicitud llega
    data = request.get_json()
    print("Datos recibidos:", data)  # Imprime el JSON recibido
    if data["object"] == "page":
        print("El objeto es 'page'")  # Confirma que el objeto es 'page'
        for entry in data["entry"]:
            print("Procesando entrada:", entry)  # Imprime cada entrada
            for messaging_event in entry["messaging"]:
                print("Procesando evento de mensajería:", messaging_event)  # Imprime cada evento
                sender_psid = messaging_event["sender"]["id"]
                print("Sender PSID:", sender_psid)  # Imprime el ID del remitente
                if messaging_event.get("message"):
                    print("Mensaje recibido:", messaging_event["message"])  # Imprime el mensaje
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
    app.run(host="0.0.0.0", port=port, debug=True)  # Activa el modo de depuración