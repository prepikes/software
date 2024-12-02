let currentTemp = 25;
let fanSpeed = 1; // 0 代表关闭，1,2,3 代表低中高风速
let isOn = false;

// 添加服务器地址配置
const SERVER_URL = "http://127.0.0.1:8000/"; // 这里需要替换为您的Django服务器地址

// 添加 API 对象定义
const api = {
  async postSetTemperature(data) {
    const response = await fetch(SERVER_URL + "api/temperature/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        currentTemp: data.temperature,
      }),
    });
    return response.json();
  },

  async postTurnOn(data) {
    const response = await fetch(SERVER_URL + "api/power/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        isOn: true,
      }),
    });
    return response.json();
  },

  async postTurnOff(data) {
    const response = await fetch(SERVER_URL + "api/power/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        isOn: false,
      }),
    });
    return response.json();
  },

  async postSetSpeed(data) {
    const response = await fetch(SERVER_URL + "api/fan-speed/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        fanSpeed: data.speed,
      }),
    });
    return response.json();
  },
};

// 添加错误处理函数
function showError(message) {
  alert(message);
}

// 修改 sendToServer 函数
async function sendToServer(action, data) {
  try {
    let response;
    switch (action) {
      case "tempSlider":
        response = await api.postSetTemperature({
          temperature: data.temperature,
        });
        break;
      case "togglePower":
        response = data.isOn
          ? await api.postTurnOn(data)
          : await api.postTurnOff(data);
        break;
      case "changeFanSpeed":
        response = await api.postSetSpeed({
          speed: data.speed,
        });
        break;
    }

    if (response && response.status === "error") {
      showError(response.message);
    }
  } catch (error) {
    console.error("发送请求失败:", error);
    showError("连接服务器失败，请检查网络连接");
  }
}

function setTemperature() {
  if (!isOn) return;

  const tempInput = document.getElementById("temp-input");
  const newTemp = parseInt(tempInput.value);

  if (newTemp < 18 || newTemp > 30) {
    alert("温度必须在18-30度之间");
    tempInput.value = currentTemp;
    return;
  }

  sendToServer("tempSlider", { temperature: newTemp });
  currentTemp = newTemp;
  updateDisplayTemp();
}

function togglePower() {
  isOn = !isOn;
  const tempInput = document.getElementById("temp-input");
  const setTempButton = tempInput.nextElementSibling;

  if (isOn) {
    document.getElementById("ac-temp").value = currentTemp;
    tempInput.disabled = false;
    setTempButton.disabled = false;
    updateDisplayTemp();
  } else {
    document.getElementById("display-temp").textContent = "关";
    tempInput.disabled = true;
    setTempButton.disabled = true;
    tempInput.value = "";
  }
  sendToServer("togglePower", { isOn: isOn });
}

function changeFanSpeed() {
  if (isOn) {
    fanSpeed = fanSpeed + 1;
    if (fanSpeed > 3) {
      fanSpeed = 0;
    }
    updateFanSpeedIcon();
    if (fanSpeed > 0) {
      sendToServer("changeFanSpeed", { speed: fanSpeed });
    }
  }
}

function updateDisplayTemp() {
  if (isOn) {
    const tempElement = document.getElementById("display-temp");
    tempElement.textContent = `${currentTemp}°`;
    document.getElementById("ac-temp").value = currentTemp;
    document.getElementById("temp-input").value = currentTemp;
  }
}

function updateFanSpeedIcon() {
  const iconElement = document.getElementById("fan-speed-icon");

  // 始终创建三个档位条，不论是否为0档
  let bars = "";
  for (let i = 1; i <= 3; i++) {
    bars += `<span class="speed-bar${i <= fanSpeed ? " active" : ""}"></span>`;
  }
  iconElement.innerHTML = bars;
}

// 滑动条变化时更新显示温度
document.getElementById("ac-temp").addEventListener("input", function () {
  if (isOn) {
    currentTemp = parseInt(this.value, 10);
    updateDisplayTemp();
    sendToServer("tempSlider", { temperature: currentTemp });
  }
});

// 更新初始化部分
document.addEventListener("DOMContentLoaded", () => {
  const tempInput = document.getElementById("temp-input");
  const setTempButton = tempInput.nextElementSibling;

  // 初始状态为关机，禁用输入框和按钮
  tempInput.disabled = true;
  setTempButton.disabled = true;
  tempInput.value = ""; // 清空输入框
  document.getElementById("display-temp").textContent = "关";

  // 确保风速图标显示
  const iconElement = document.getElementById("fan-speed-icon");
  if (iconElement) {
    // 添加检查确保元素存在
    let bars = "";
    for (let i = 1; i <= 3; i++) {
      bars += `<span class="speed-bar${
        i <= fanSpeed ? " active" : ""
      }"></span>`;
    }
    iconElement.innerHTML = bars;
  }
});
