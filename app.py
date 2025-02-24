from flask import Flask, request

app = Flask(__name__)

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
