from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Servidor funcionando", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Aquí verificamos el token de verificación
        token = request.args.get('hub.verify_token')
        if token == 'afudeteam1234':
            return request.args.get('hub.challenge'), 200
        else:
            return "Token de verificación inválido", 403
    # Manejo de mensajes POST va aquí



