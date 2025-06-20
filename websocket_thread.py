import websocket
import json
import time
import ssl
import requests

# === BIẾN TOÀN CỤC ===
id_phien = None
API_URL = "https://taixiu-api-ws.onrender.com/api/taixiu"

# === DANH SÁCH TIN NHẮN GỬI ===
messages_to_send = [
    [1, "MiniGame", "saoban", "ere2234", {
        "info": "{\"ipAddress\":\"125.235.239.187\",\"userId\":\"2ef4335a-6562-4c64-b012-46ef83a25800\",\"username\":\"S8_saoban\",\"timestamp\":1749643344994,\"refreshToken\":\"e790adfa529e42639552261c7a7d206b.51b6327dccb94fe1b4a96040d5ded732\"}",
        "signature": "20399D67A1EC9E78B287200DE26F206FFEBB01C545C52EDAC0F0C347CF26A7900FB5AD74BC2DC9A35634C0E9F45BF799B3D8696052D5392CFB9BE0F4CF086BE8F50699C542C7693722B4EE68ECDCF72EB887B91A46FC662087E233EE7C10FED14505920B6687F5B9E30B4FF6EACBF1305FDB9A5DC4ED010DBA3C3AB3DAE5AC14"
    }],
    [6, "MiniGame", "taixiuUnbalancedPlugin", {"cmd": 2000}],
]

def on_message(ws, message):
    global id_phien

    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        print("❌ Không thể parse JSON")
        return

    if isinstance(data, list) and len(data) >= 2 and isinstance(data[1], dict):
        payload = data[1]
        cmd = payload.get("cmd")

        if cmd == 2007:
            sid = payload.get("sid")
            if sid and sid != id_phien:
                id_phien = sid
                print(f"🎮 Phiên mới: {id_phien}")

        elif cmd == 1003 or ("d1" in payload and "d2" in payload and "d3" in payload):
            d1 = payload.get("d1")
            d2 = payload.get("d2")
            d3 = payload.get("d3")

            if d1 is not None and d2 is not None and d3 is not None:
                total = d1 + d2 + d3
                outcome = "Tài" if total > 10 else "Xỉu"
                print(f"🎲 {d1}, {d2}, {d3} → Tổng: {total} → Kết quả: {outcome}")

                try:
                    requests.post(API_URL, json={
                        "Phien": id_phien,
                        "Tong": total,
                        "Ket_qua": outcome,
                        "Xuc_xac_1": d1,
                        "Xuc_xac_2": d2,
                        "Xuc_xac_3": d3,
                        "id": "Wanglin"
                    })
                    print("✅ Đã gửi kết quả về API")
                except Exception as e:
                    print("❌ Gửi API lỗi:", e)

def on_error(ws, error):
    print(f"❌ Lỗi WebSocket: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"🔌 Đã ngắt kết nối: {close_status_code} - {close_msg}")

def on_open(ws):
    print("✅ WebSocket kết nối thành công")
    for msg in messages_to_send:
        ws.send(json.dumps(msg))
        time.sleep(1)

def run_websocket():
    header = [
        "Host: websocket.atpman.net",
        "Origin: https://789club.sx",
        "User-Agent: Mozilla/5.0"
    ]

    while True:
        try:
            ws = websocket.WebSocketApp(
                "wss://websocket.atpman.net/websocket",
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
                on_open=on_open,
                header=header
            )
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, ping_interval=10, ping_timeout=5)
        except Exception as e:
            print(f"🔁 Mất kết nối WebSocket: {e}")
            time.sleep(5)
