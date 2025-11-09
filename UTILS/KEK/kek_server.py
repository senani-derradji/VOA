from flask import Flask, jsonify, request
from cryptography.fernet import Fernet
from pathlib import Path
import os, time, threading

app = Flask(__name__)

KEY_FILE = Path("kek_store.key")
AUTH_NAME = "SECRET_AUTH"
AUTH_TOKEN = os.getenv(AUTH_NAME)
kek_lock = threading.Lock()

def load_or_generate_kek():
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()
    else:
        new_kek = Fernet.generate_key()
        KEY_FILE.write_bytes(new_kek)
        return new_kek

kek = load_or_generate_kek()

def rotate_kek_periodically():
    global kek
    while True:
        time.sleep(3600)
        with kek_lock:
            kek = Fernet.generate_key()
            KEY_FILE.write_bytes(kek)
            print("[*] KEK rotated.")
        # FOR TESTING
        with open("KEK_HOST_FILE.key", "w") as f: f.write(f"{time.time()} : {kek.decode()}")

threading.Thread(target=rotate_kek_periodically, daemon=True).start()

@app.route("/get_kek", methods=["GET"])
def get_kek():
    token = request.headers.get("Authorization", "")
    if token != f"Bearer {AUTH_TOKEN}": return jsonify({"error": "Unauthorized"}), 401

    with kek_lock: current_kek = kek

    return jsonify({"kek": current_kek.decode()})

@app.route("/health", methods=["GET"])
def health_check(): return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, ssl_context=("cert.pem", "key.pem"))