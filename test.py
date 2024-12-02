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
    send_request("togglePower", {"isOn": True})
    time.sleep(5)
    send_request("decreaseTemp", {"currentTemp": 18})
    time.sleep(20)

    send_request("changeFanSpeed", {"fanSpeed": 3})
    time.sleep(20)

    send_request("increaseTemp", {"currentTemp": 22})
    time.sleep(20)

    send_request("togglePower", {"isOn": False})
    time.sleep(15)

    send_request("togglePower", {"isOn": True})
    time.sleep(30)

    send_request("togglePower", {"isOn": False})

if __name__ == "__main__":
    main()