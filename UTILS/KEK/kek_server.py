from flask import Flask, jsonify, request
from cryptography.fernet import Fernet
from pathlib import Path
import os, time, threading, requests

app = Flask(__name__)

KEY_FILE = Path("kek_store.key")
AUTH_NAME = "SECRET_AUTH"
AUTH_TOKEN = os.getenv(AUTH_NAME)
BACKEND_URL = os.getenv("BACKEND_URL", "https://backend:8000/update-kek")
BACKEND_SECRET = os.getenv("BACKEND_SECRET", "super_secret_shared_token")
kek_lock = threading.Lock()

def load_or_generate_kek():
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()
    else:
        new_kek = Fernet.generate_key()
        KEY_FILE.write_bytes(new_kek)
        return new_kek

kek = load_or_generate_kek()

def notify_backend(new_kek: bytes):
    """Send the new KEK to the backend securely."""
    try:
        headers = {"X-Auth-Token": BACKEND_SECRET}
        response = requests.post(
            BACKEND_URL,
            json={"kek": new_kek.decode()},
            headers=headers,
            timeout=5,
            verify=False  # CHANGE
        )
        print(f"[*] Notified backend: {response.status_code}")
    except Exception as e:
        print("[!] Failed to notify backend:", e)

def rotate_kek_periodically():
    global kek
    while True:
        time.sleep(3600)
        with kek_lock:
            kek = Fernet.generate_key()
            KEY_FILE.write_bytes(kek)
            print("[*] KEK rotated.")
            notify_backend(kek)
        with open("KEK_HOST_FILE.key", "w") as f:
            f.write(f"{time.time()} : {kek.decode()}")

threading.Thread(target=rotate_kek_periodically, daemon=True).start()

@app.route("/get_kek", methods=["GET"])
def get_kek():
    token = request.headers.get("Authorization", "")
    if token != f"Bearer {AUTH_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    with kek_lock:
        current_kek = kek

    return jsonify({"kek": current_kek.decode()})

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, ssl_context=("cert.pem", "key.pem"))
