from flask import Flask, request, jsonify
import threading
from websocket_thread import run_websocket  # Đúng tên hàm

app = Flask(__name__)

@app.route('/api/taixiu', methods=['POST'])
def nhan_ket_qua():
    data = request.get_json()
    print("📥 Nhận dữ liệu:", data)
    return jsonify({"message": "OK", "data": data})

if __name__ == '__main__':
    # Chạy websocket song song
    threading.Thread(target=run_websocket, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
