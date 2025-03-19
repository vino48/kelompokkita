from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Konfigurasi Telegram
TELEGRAM_BOT_TOKEN = "7811698909:AAHpoXl49W5MSaxTkicIOUfv_8zJh1-QpY4"
TELEGRAM_CHAT_ID = "@kadalsace_bot"

# Ambang batas minimal
GAS_MIN_THRESHOLD = 8000
SMOKE_MIN_THRESHOLD = 8000
TEMP_MIN_THRESHOLD = 20  # Contoh ambang batas suhu minimal

# Variabel status alarm dan data sensor
alarm_status = {
    "gas": "OFF",
    "smoke": "OFF",
    "temp": "OFF",
    "humidity": "OFF",
    "wind": "OFF"
}

latest_data = {
    "gas": 0,
    "smoke": 0,
    "temp": 0,
    "humidity": 0,
    "wind_speed": 0,
    "gas_status": "Aman",
    "smoke_status": "Aman",
    "wind_status": "Aman"
}

# Fungsi untuk mengirim notifikasi ke Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{7811698909:AAHpoXl49W5MSaxTkicIOUfv_8zJh1-QpY4}/sendMessage"
    payload = {"chat_id": kadalsace_bot, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Gagal mengirim notifikasi Telegram:", e)

@app.route('/')
def index():
    return render_template('tes.html')

@app.route('/update', methods=['POST'])
def update_data():
    global latest_data
    data = request.json
    latest_data.update(data)
    
    # Cek apakah nilai berada di bawah ambang batas minimal
    if data["gas"] < GAS_MIN_THRESHOLD:
        send_telegram_message(f"⚠️ Peringatan! Gas di bawah batas aman: {data['gas']}")
    if data["smoke"] < SMOKE_MIN_THRESHOLD:
        send_telegram_message(f"⚠️ Peringatan! Smoke di bawah batas aman: {data['smoke']}")
    if data["temp"] < TEMP_MIN_THRESHOLD:
        send_telegram_message(f"⚠️ Peringatan! Suhu di bawah batas aman: {data['temp']}°C")
    
    return jsonify({"message": "Data Update Success"})

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(latest_data)

@app.route('/alarm_status', methods=['GET'])
def get_alarm_status():
    return jsonify(alarm_status)

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    global alarm_status
    data = request.json
    alarm_type = data.get("type")
    status = data.get("status")

    if alarm_type in alarm_status:
        alarm_status[alarm_type] = status
        return jsonify({"message": f"Alarm {alarm_type} set to {status}."})
    else:
        return jsonify({"error": "Invalid alarm type!"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
