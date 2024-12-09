import requests
import json
import time

SERVER_URL = "http://127.0.0.1:8000/api/"  # Django 服务器地址

def send_request(action, data=None):
    """模拟 JS 函数 sendToServer，向后端发送请求"""
    endpoints = {
        "increaseTemp": "temperature/",
        "decreaseTemp": "temperature/",
        "togglePower": "power/",
        "changeFanSpeed": "fan-speed/",
        "test": "test/",
    }

    endpoint = endpoints.get(action)
    if not endpoint:
        print(f"Error: Unknown action '{action}'")
        return

    url = f"{SERVER_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    payload = {"action": action}
    if data:
        payload.update(data)

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # 抛出 HTTP 错误 (4xx 或 5xx)
        result = response.json()
        if result.get('status') == 'success':
            print(f"Request '{action}' successful.")
        else:
            print(f"Request '{action}' failed: {result}")
    except requests.exceptions.RequestException as e:
        print(f"Request '{action}' failed: {e}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON response: {e}")

def main():
    # 定时操作序列
    # send_request("togglePower", { "isOn": True, "room_id": 1})
    # time.sleep(0.1)
    # send_request("togglePower", { "isOn": True, "room_id": 2})
    # time.sleep(0.1)
    # send_request("togglePower", { "isOn": True, "room_id": 3})
    # time.sleep(0.1)
    # send_request("togglePower", { "isOn": True, "room_id": 4})
    # time.sleep(0.1)
    # send_request("decreaseTemp", { "targetTemp": 21.5, "room_id": 1})
    # send_request("test")
    # time.sleep(0.1)
    # send_request("decreaseTemp", { "targetTemp": 21.5, "room_id": 2})
    # time.sleep(10)
    # send_request("changeFanSpeed", { "fanSpeed": 3, "room_id": 1})
    # time.sleep(0.1)
    # send_request("changeFanSpeed", { "fanSpeed": 2, "room_id": 2})
    # time.sleep(0.1)
    # send_request("changeFanSpeed", { "fanSpeed": 2, "room_id": 3})
    # time.sleep(0.1)
    # send_request("togglePower", { "isOn": False, "room_id": 4})
    send_request("test")

if __name__ == "__main__":
    main()