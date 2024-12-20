from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import threading
from assistente import ouvir_assistente, parar_assistente, esta_ouvindo

# Instância do Flask
app = Flask(__name__)
CORS(app)

# Variável de controle
lock = threading.Lock()

def build_cors_preflight_response():
    response = make_response("")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    response.status_code = 200
    return response

@app.route("/")
def home():
    return "Servidor Flask está funcionando!"

@app.route('/processar_comando', methods=['POST', 'OPTIONS'])
def processar_comando():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()
    data = request.json  # Captura o JSON enviado
    comando = data.get('comando', '')  # Captura o comando enviado
    print(f"Comando recebido: {comando}")
    return jsonify({'message': f"Comando '{comando}' processado com sucesso!"}), 200

@app.route("/assistente/ativar", methods=["POST", "OPTIONS"])
def ativar_assistente():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()
    with lock:
        if not esta_ouvindo():
            ouvir_assistente()
            return jsonify({"message": "Assistente ativada!"}), 200
        return jsonify({"message": "Assistente já está ativa!"}), 400

@app.route("/assistente/parar", methods=["POST", "OPTIONS"])
def parar_assistente_api():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()
    with lock:
        if esta_ouvindo():
            parar_assistente()
            return jsonify({"message": "Assistente desativada!"}), 200
        return jsonify({"message": "Assistente já está desativada!"}), 400

@app.route("/status", methods=["GET", "OPTIONS"])
def status():
    if request.method == 'OPTIONS':
        return build_cors_preflight_response()
    if esta_ouvindo():
        return jsonify({"status": "ativa"}), 200
    return jsonify({"status": "desativada"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
