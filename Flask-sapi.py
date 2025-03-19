from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)

# File untuk menyimpan data sementara
DATA_FILE = "data.json"

# Pastikan file JSON ada
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# API untuk menerima data dari Raspberry Pi Pico W
@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        print("Data diterima:", data)

        # Simpan ke file JSON
        with open(DATA_FILE, "r+") as f:
            existing_data = json.load(f)
            existing_data.append(data)  # Tambah data baru
            f.seek(0)
            json.dump(existing_data, f, indent=4)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# API untuk mengirim data ke dashboard
@app.route('/api/get_data', methods=['GET'])
def get_data():
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

# Dashboard HTML
@app.route('/')
def dashboard():
    return render_template("home-sapi.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
