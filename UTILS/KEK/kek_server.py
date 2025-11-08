from flask import Flask, jsonify, request
from cryptography.fernet import Fernet
from pathlib import Path
import os

app = Flask(__name__)

KEY_FILE = Path("kek_store.key")
AUTH_NAME = "SECRET_AUTH"
AUTH_TOKEN = os.getenv(AUTH_NAME)

if KEY_FILE.exists():
    kek = KEY_FILE.read_bytes()
else:
    kek = Fernet.generate_key()
    KEY_FILE.write_bytes(kek)

# kek_served = False

@app.route("/get_kek", methods=["GET"])
def get_kek():
    # global kek_served
    token = request.headers.get("Authorization", "")
    if token != f"Bearer {AUTH_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    # if kek_served:
    #     return jsonify({"error": "KEK already accessed"}), 403

    # kek_served = True
    if KEY_FILE.exists():
        KEY_FILE.unlink()
    if AUTH_NAME in os.environ:
        del os.environ[AUTH_NAME]

    return jsonify({"kek": kek.decode()})

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)