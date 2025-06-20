from flask import Flask, request, jsonify
import threading
import os
from websocket_thread import run_websocket

app = Flask(__name__)

# Route trang chủ
@app.route('/', methods=['GET'])
def home():
    return "✅ API Tài/Xỉu đang hoạt động"

# Route GET để tránh lỗi 405
@app.route('/api/taixiu', methods=['GET'])
def taixiu_test():
    return "✅ Đây là API nhận POST kết quả Tài/Xỉu"

# Route chính nhận kết quả POST
@app.route('/api/taixiu', methods=['POST'])
def nhan_ket_qua():
    data = request.get_json()
    print("📥 Nhận dữ liệu:", data)
    return jsonify({"message": "OK", "data": data})

if __name__ == '__main__':
    print("🚀 Khởi động Flask + WebSocket")
    threading.Thread(target=run_websocket, daemon=True).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
