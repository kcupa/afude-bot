from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get('hub.verify_token')
        if token == 'afudeteam1324':  # Reemplaza con tu token de verificación
            return request.args.get('hub.challenge'), 200
        else:
            return "Token de verificación inválido", 403
    # Aquí maneja los mensajes POST
    return "Webhook recibido", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
