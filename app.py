from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Servidor funcionando", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
