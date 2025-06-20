from flask import Flask, request, jsonify
import threading
from websocket_thread import run_websocket

app = Flask(__name__)

# Route chính để kiểm tra
@app.route('/', methods=['GET'])
def home():
    return "✅ API Tài/Xỉu đang hoạt động"

# Nhận kết quả tài/xỉu từ WebSocket
@app.route('/api/taixiu', methods=['POST'])
def nhan_ket_qua():
    data = request.get_json()
    print("📥 Nhận dữ liệu:", data)
    return jsonify({"message": "OK", "data": data})

if __name__ == '__main__':
    threading.Thread(target=run_websocket, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
