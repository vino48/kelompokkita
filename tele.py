from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Konfigurasi Telegram
TELEGRAM_BOT_TOKEN = "7811698909:AAHpoXl49W5MSaxTkicIOUfv_8zJh1-QpY4"
TELEGRAM_CHAT_ID = "@kadalsace_bot"


# Fungsi untuk mengirim notifikasi ke Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        response = requests.post(url, json=payload)
        return response.json()  # Return response dari Telegram API
    except Exception as e:
        return {"error": str(e)}


# Endpoint untuk mengirim pesan ke Telegram
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Pesan tidak boleh kosong!"}), 400

    response = send_telegram_message(message)
    return jsonify(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
